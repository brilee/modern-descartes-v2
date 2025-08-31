Claude as Pipeline Orchestrator
2025/08/23
software engineering,llms

I've been using LLMs to scrape PDFs of chemistry exams while retaining chemical equation formatting, images, and test structure. This has been a far harder task than I anticipated, and I've run into many limitations with the current generation of multimodal LLMs.

I wrote a [separate essay](/essays/blind_llms/) on these limitations, but in this essay I want to talk about pipeline orchestration and design. I started with traditional software-based pipeline, but due the limitations mentioned above, I started drowning in fault-tolerance complications -- retries, progress saving, resumption, error-correction, etc.. I tried using Claude as a pipeline orchestrator and was very pleasantly surprised at how well it worked.

I believe that wrapping your subroutines in MCP servers and then using Claude as your orchestrator should be a strong default option for writing pipelines. When you work this way, you get a pipeline with **rich ad-hoc logging/debugging/recovery features** for free.

# Struggles of a traditional software pipeline

Heavily simplified, here's what my traditional software pipeline looked like.

```python
# orchestrator.py

def process_file(pdf_path):
    # A first pass into markdown makes subsequent steps much more reliable.
    # This step emits image tags inline with text, preserving positional semantics.
    # It also generates a description of each image ID.
    markdown_txt = transcribe_pdf(pdf_path)

    parsed_problems: list[Problem] = []
    current_problem: int = 0
    # LLM can only reliably parse a few problems at a time
    # They also need context reminders for what problem they're up to
    while (problem_batch := parse_problems(markdown_txt, current_problem, num_to_process=5)):
        parsed_problems.extend(problem_batch)
        # What happens in the LLM skips a problem? Or it just decides to
        # re-parse the same problems repeatedly, despite being told it's on #17 now?
        current_problem = max(current_problem, *(p.number for p in problem_batch))

    image_manifest: dict[str, str] = []
    for p in parsed_problems:
        image_manifest.update(**p.images)

    # At first, I tried getting the LLM to tell me what page the image was on.
    # It just hallucinated page numbers. 
    # So instead, I loop over pages, asking the LLM to play image search.
    images: list[PIL.Image] = []
    for page in pdf:
        images.extend(image_search(page, image_manifest))
    
    image_id_map: dict[str, str] = upload_all_images(images)

    parsed_problems = [replace_image_references(p, image_id_map) for p in parsed_problems]
    return parsed_problems
```

This is a pretty typical processing pipeline. It was difficult to debug for many reasons.

- LLMs hard fail all the time -- whether it's because of not emitting parseable JSON, text escaping/encoding errors, my OpenRouter credits running out, output token limit reached, rate limit reached, etc..
- LLMs also soft fail -- for example, not respecting the "current_problem_number" hint.
- All of my subroutines -- `transcribe_pdf`, `parse_problems`, `image_search` -- were themselves LLM calls with tool calling/structured responses to do work. I had to co-design the pipeline to accept and return operational metadata. For example, `parse_problems` parsed problems, but it also had a way to inject the `current_problem_number` into the system prompt.  to say "Please parse up to 5 problems, starting from problem {current_problem}. If there are no more problems to parse, set `problems_remaining=False`" and return an empty list."

I started to build in idempotency, resumability, progress-saving utilities, etc. etc., but in the end, it was too annoying to iterate on this pipeline.

# Claude-orchestrated version

First, I extracted the step that transcribed the PDF into markdown. 

Then, I drastically simplified the parse_problems code. Now, it basically consists of the Pydantic spec and documentation for what a single problem should look like. No manual batching, no operational data channels, no LLM calls. (Claude calls me, rather than me calling the LLM.)

Finally, I added an MCP server to the `claude` CLI tool exposing the `register_problem` tool. I wrote the following plaintext instructions:

    Upload the problems contained in the given file by using the
    create_problem_source, register_problem MCP tools, in that order.

    # Step 1: Create Problem Source

    This step registers a problem source, so that all uploaded
    problems can be grouped together in the database.

    # Step 2: Register problems

    This step uploads the problems to the database. 

    ... detailed instructions on how to transcribe problems,
    instructions on how to use LaTeX and mhchem to transcribe
    chemical reactions, transcribe [[image_001]] tags verbatim...

Then, I opened up the `claude` CLI and said, "please process @markdown_file according to @instructions".

And it basically just worked! Claude seamlessly figured out how many problems were in the markdown file, that it should create a TODO list to track progress, and then it chugged away until it was done.

On top of that, I now had the following benefits

- Pausability (just hit escape)
- A persistent session, so that if the processing stopped for whatever reason, I could literally just tell Claude, "hey I just topped off my openrouter credits, resume from problem 17", and it would just pick up at the correct location.
- A text interface debugger, so that I could literally ask Claude to print out various things to help me debug where something was breaking.
- Status updates on what exactly Claude was working on at any given moment
- A built-in debugging interface to inspect the specific MCP calls being made, so that I could hunt down where exactly a double-escaping issue got introduced.
- A text interface to tell Claude, "hey, just upload the first 10 problems" for quick debugging/iteration.
- My LLM costs are folded into my Claude Pro subscription. 😈

## "Agent" vs. "Claude"

I've mentioned Claude by name several times here, instead of writing "agent". This is because most of these benefits are not actually due to the agentic nature of Claude. Instead, it's the utility features that the Claude CLI comes with: automatic logging, persistent sessions, an interactive CLI to communicate with Claude, and so on.

To Anthropic's credit, Claude also seems generally good at the agentic orchestration thing, on top of all the developer experience niceness. I haven't tried the equivalent Gemini/OpenAI interfaces, so they may be just as good.

# You should never write a software pipeline. Ever. Again.

Okay, that's a bit of an overstatement.

But seriously. Each of these debugging/logging/concurrency/resumability features is something that a real production pipeline needs to build at some point. Usually, you get to that point by building the simple pipeline first. Then, you have to manually debug it. Then, after you ship it to production, you build debugging/logging features and fix a long tail of breakages over the next three months as you discover new ways for the pipeline to fail. This is easily _months_ of work, and you get it for free by letting Claude be your orchestrator.

## The Fine Print

Here are some gotchas:

- Claude cannot reliably transcribe long IDs into function calls. As a result, images were referred to with short tags `image_001`; problems were referred to by source number `problem 17`, and so on.
- Claude has a context limit of ~200K tokens.
- Claude gives up on waiting for subroutines after 2 minutes (not yet configurable).
- Nondeterministic failure. The typical LLM weirdnesses.

The first two issues are essentially data-plane vs. control-plane issues. In a traditional control plane/data plane separation, the orchestrator (control plane, often Python) issues commands that take place on many processes/machines (often written in a faster language than Python). You can't pass large amounts of data through the control plane, and you can't do much computation either, since the control plane would quickly become a bottleneck. So the control plane must be careful to only touch or deal with a small fraction of the overall work. It can shuttle UUIDs around in order to keep track of which work items are being assigned to which machine, but it can't do the work itself.

With Claude as orchestrator, you follow the same control/data plane separation philosophy. Its "memory" is equivalent to a mere ~1MB (should be enough for anybody, right?), and has a weird flavor of compute limitation (IDs and other "exact" values have to be simple enough for an LLM to transcribe).

# Conclusion

For my PDF transcription task, the task was small enough that I could basically merge the data and control planes - the same Claude agent was responsible for handling the parsing and reformatting of all PDF contents, as well as making all the tool calls to render the entries to my database. This made my pipeline orchestration experience particularly pleasant.

To get around these scaling limitations, I can think of two obvious tactics. One is Claude's subagents feature, which can help with the context window limitations. The second is having Claude just open up an interactive Python shell and run Python commands (e.g. it would run your pipeline by calling functions in a persistent interpreter, rather than by invoking MCP servers). This way, it could use Python variables instead of transcribing UUID, and its effective memory would be gigabytes, not single-digit megabytes in size. I'm reading through Armin Ronacher's [latest blog post on replacing MCPs with code](https://lucumr.pocoo.org/2025/8/18/code-mcps/) with great interest.

In the very, very near future, somebody will likely figure out how to tie together Claude and a Python interpreter in a way that will complete the vision of Claude as orchestrator, without the context window/copy accuracy limitations.