Strategies and Tactics for working with Coding Agents
2025/10/12
llms,software engineering,popular

For the last 6 months, I've been building an AI-powered tutor for teaching advanced chemistry. The codebase is roughly 98% AI-generated, but 98% is a highly misleading number. Yes, it's true that if you look at the authorship by lines of code, Claude wrote 98%. But there has been so much human intervention that it would be more accurate to say that my codebase is 250% AI-generated, with my contribution totalling +2%/-152%.

Here are some of the ways in which simple vibecoding has failed me, and how I've coevolved with AI coding assistants over the last six months.

# Strategy

## Information Architecture should be handwritten

Every single "no-code platform for non-coders" has run into this issue sooner or later: the person using the platform doesn't actually know how to communicate what they want to have built. (Let's pretend it's a communication issue.)

The answer to "what do you want to build?" is the information architecture (IA), also called the data model. From this IA, everything else flows. Information Architecture (IA) constitutes the following things:

- Who "owns" an object? (both in the sense of who is authorized to take various actions, as well as any parent entities whose lifecycle is linked to this object.)
- What uniquely identifies an object?
- Where is the source of truth / what is merely a clone or derived value?
- What type of relationship (`1:1, 1:n, n:m`) does this object have with other objects?
- What is the lifecycle of this object? Who/what triggers creation, what operations happen during its lifetime, is the object ever considered "complete/dead/deleted"?

The reason I say these should be handwritten is not because AI is incapable of thinking about these things. It can, in fact, contribute to the development of the IA, and if you can answer the above questions in plain English, AI can even translate this into the appropriate database models/APIs/etc.. But in the end, you must have answered the above questions, because the IA is the nucleus of the software, the DNA from which the rest of the app derives.

In practice, "handwriting an IA" to me, means sitting down and writing the Pydantic/SQLAlchemy models by hand. It usually takes just 10-50 lines of code, and this is precisely the 2% of my codebase that is handwritten.

If you do not design your IA, AI will intentionlessly design it for you.

See [Your Data Model is Your Destiny](https://notes.mtb.xyz/p/your-data-model-is-your-destiny) for a great compilation of the ways in which IA are fundamental to a product.

## Useless features should be removed

When AI-coding, you should take [YAGNI](https://martinfowler.com/bliki/Yagni.html) to its extreme. This is for two reasons:

1. AI coding makes it absolutely trivial to add new features later on if you do need it.
2. Useless features propagate like a cancer. It's far easier to remove them before they metastasize.

Here's an illustration of how useless features can spread.

I wanted to build a set of chemistry lectures, and I had the not so brilliant idea that I'd just take the AP Chemistry Teacher's Manual and transform this PDF into a curriculum via AI. I transcribed and transformed the entire PDF, and the result was a complete mess. The Teacher's Manual was full of useless text that I will generously interpret as "bureaucratic ass-covering". For example, each lesson teaches a "Skill", like `Mathematical Routines (5.D) - Identify information presented graphically to solve a problem.`. Very important skill. Later, when I asked Claude to write practice problems for each lesson, it would try to incorporate these useless annotations. The generated practice problems would contain problems like, "Explain how you interpreted this diagram graphically to answer part (a)". Eventually, I realized that it was far easier to handwrite every single lesson plan in a roughly 50-word sketch - and from this, everything flowed so much more smoothly. Less was more.

A similar thing happens in your codebase. This very same curriculum data has at least six representations in my codebase:

1. raw YAML files. (This is what gets checked into source control.)
2. publication API/client/script so that I can push curriculum updates to the live site.
3. postgres table, with various foreign keys and indices.
4. templated into an AI's system prompt when a new lesson is started.
5. API on-the-wire representation that the frontend uses to query available lessons and to start/interact with lessons.
6. Frontend representation, to display various metadata to the user about which lesson they're currently taking.

This is just the straight-line from the raw data that I hand-edit, to the lesson that users interact with. It does not include, e.g. cross-links between curriculum and test questions, or the MCP server I built to let Claude manipulate the curriculum.

Every useless feature is amplified by its many representations throughout the system, bloating the context window and distracting the AI. The AI has no awareness on which of these features is actually important, and so it will default to building a solution that ensures everything is handled and passed through. Sometimes, the presence of one useless feature induces the AI to build another useless feature, which itself becomes useless fluff that amplifies throughout your codebase.

Fluff is less important to trim on the frontend, because it is at the very tip of this amplification chain. On the other hand, useless features in the core data models **must** be trimmed. It is so much easier to trim these features before they grow tendrils into other parts of your codebase.

## Consistent naming is important

One of the big breakthroughs this year in coding assistants is tool usage, and specifically, `grep`. I think it is quite reasonable to say that Claude Code's ability to productively use `grep` was what let Claude vault across the moat of Cursor's extensive investments into codebase indexing and RAG patterns. I remember seeing Cursor's increasingly panicked emails to me after I'd canceled my Cursor subscription for a Claude one -- all because Claude knew how to use grep.

Your codebase will be most greppable when each concept has a distinct, consistently used, greppable name. Then, when you ask Claude, "hey can you add X feature to Y system", Claude will grep for Y, and immediately come up with a giant list of files that must be touched in order to build top-to-bottom support for your new feature X. Yes, you could curate a CLAUDE.md file that lays out all this system architecture, but why not just build it into your codebase? This tip is related to the "think about your IA" tip.

## Set up frameworks for success.

AI is very good at following existing patterns in your codebase.

I've been using Svelte 5/Sveltekit for my startup's frontend code. The first month was painful, because neither I nor the LLM knew how to write Svelte 5 code. Everyone else was talking about how React/Next would become the LLM frontend dialect/framework of choice, and I wondered if I should switch over. But over the next 2 months, I learned frontend; I thought about how I wanted my frontend code structured, and spent a lot of time figuring out how to handwrite a few components/data stores in the way I wanted to organize the codebase. Claude can then look at these files for inspiration/templates for how to design new components and data stores. (I also rely heavily on OpenAPI codegen for client code, and Claude also knows this.)

Since then, I have basically vibecoded every single frontend feature, and I really do mean vibecode -- I barely glance at the svelte code before checking it in and deploying it. Every so often I double-check the code to make sure it looks roughly correct, and other than the [unnecessary try-catch blocks that LLMs can't stop writing](https://x.com/karpathy/status/1976077806443569355), the AI basically wrote the code that I would have written myself.

Now, this has led to a number of hilarious failures, which I have progressively introduced more structure/frameworks to fix.

For example, I noticed one day that the specific shade of blue wasn't quite right on one page. I realized then that Claude had been vibing new RGB hex codes every time it needed to style a component, and that they were all slightly different. So I then had to introduce color variables and create a color scheme. Another time, I noticed that all of my pages had slightly different widths -- 1200px, 1000px, 960px, 1024px, etc. Same issue. I believe I'll have to go through at some point and convert my entire site to using Tailwind CSS, and actually learn how div nesting works in CSS. A third related issue which I haven't fixed yet: click areas vary because Claude sometimes uses flexbox / gap to space elements, and othertimes margin/padding, and no two pages really have consistent spacing. I'm sure that there are more issues that I haven't noticed yet, as a frontend noob.

# Tactics

## Lean on AI to do integrations

One area in which I've found coding agents an absolute godsend is in third-party integrations. I really, really, do not want to learn how each vendor's API works - I want a simple module that wraps and quarantines each vendor's nonsense, presenting a simple interface that exposes just the one or two things that I need that vendor to actually do. Then, there's all of the one-off setup / installation nonsense that needs to happen for each vendor. I have found that Claude is shockingly good at navigating these vendor integrations. Any time I touched GCP, for example, would inevitably have been an hours-long slog of figuring out which IAMs I have to grant myself/my service account, figure out why some bucket was misconfigured, what the _names_ of the relevant IAMs even are, etc. etc.. Now I just tell Claude what outcome I want, and it turns out to basically know the `gcloud` CLI by heart. If it doesn't know the CLI invocations, it can do the web research to look up the right documentation.

## Run all one-off setup through Claude

A related tip is to run all one-off setup through Claude. I actually have stopped using commands like `uv add X`, in favor of asking Claude, "can you install X library". Claude _usually_ runs `uv add X`, but there are a variety of instances where the name of the python import does not line up with the package name, or where there is some `[option]` that I'm supposed to specify when installing the package. Same goes for frontend libraries. I _especially_ do this when I have to install a ruby-based tool, and I have to invoke some incantation of rbenv and ruby and gem and bundler, none of which are tools I know much about. Claude knows about all of these tools. It roughly knows "best practices" for using environment/package managers, and can grok error messages and hammer away until the installation works. I am 100% happy to let Claude do this work.

This probably horrifies some subset of you, especially those of you who actually know how package managers work and/or work in security. But the truth is that figuring out installation/dependency hell is by far my least favorite part of coding. I used to volunteer to help teach Python to beginners, but you know what? 99% of my time was actually spent unfucking people's Python installations, not actually answering Python questions. I assure you that for the vast majority of people/scenarios/use cases, Claude is far more likely to install something correctly, with the right level of sudo or global installation or system, env manager, package manager, etc. than someone who is trying to do it manually without knowing what they're doing.

## Help build the debug tooling

Many times, I've thought -- "if only I could just edit the database into the appropriate test configuration, this would be so much easier". Usually, this simply involves firing up pgAdmin or some other GUI-based database interface. But Claude can do it better.

In one scenario involving my consulting client, it was a mysql database running in docker, with a complicated database+table+foreign key structure that I didn't care to understand deeply. I didn't know mySQL syntax, nor did I have a mysql GUI installed, nor did I want to learn or install any new tools. The goal was to find a lesson that had a quiz that contained a problem that had a certain type of LaTeX syntax to be present, in addition to having multiple choice options that were themselves image attachments, to see if my prompt templating was handling it all correctly in the live app.

I started by setting up Claude with a bash utility:

    > can you compose a single bash command that will create a docker bash shell, start a mysql 
    shell, and run SQL? I'm currently using `docker-compose exec db sh` and then mysql 
    --user=root --password=root 

    ⏺ docker-compose exec db mysql --user=root --password=root -e "DESCRIBE table_name;"

    Or for an interactive mysql shell:

    docker-compose exec db mysql --user=root --password=root

    Or to run multiple SQL statements:

    docker-compose exec db mysql --user=root --password=root <<EOF
    DESCRIBE table_name;
    SELECT * FROM another_table LIMIT 5;
    EOF

    > /clear 
    ⎿  (no content)

Then, I cleared the context and asked Claude to 1. find an example of a problem that had an attachment as well as the appropriate LaTeX syntax in it, using ILIKE "%%" to search the problem.prompt_text field and then 2. figure out the lesson module URL where I could see this problem in the app. I passed in the above instructions on how to execute arbitrary SQL in my specific configuration.

Claude then utilized a combination of DESCRIBE sql queries and grepping through the codebase to guide its search and understanding of the schema, and then finally reported that while there were problems with the right LaTeX syntax and problems with image attachments, there were not problems with both. So I then asked Claude to finagle the attachment_id foreign keys to construct the desired example -- which it was able to do cleanly. Finally, I was able to load up this mutant example in my dev instance, and then iterate on my code until it worked properly.

P.S. Despite Claude's wizardry, I was watching like a hawk while Claude did its thing. I still don't trust it not to reset my database.

## LLMs are blind

I elaborate on this point in [Multimodal LLMs are Blind](/essays/blind_llms/), but the TL;DR is: LLMs are currently actually blind, and they present the illusion of having vision capabilities by using what are essentially screenreaders / captioning tools.

Do _not_ expect LLMs to be able to do more than copy/figure out the rough page structure based on a screenshot.

A half-fix for this issue is Playwright MCP, which lets the LLM interact directly with the compiled/rendered version of an app at the browser engine level. Through Playwright, an LLM can precisely grab color hex codes or CSS properties, or copy div nesting structure. It can even sort of understand global page layout through the screenshot API. But because LLMs are currently blind, you will not be able to use LLMs to fine-tune visual alignment and other types of size/shape matching.

In between Figma/Adobe working on this problem, and improvements in the base LLMs, I do expect this problem to go away on the 1-2 year timescale.

# Conclusion

Overall, working with an AI coding assistant is much like being the tech lead for a project. Many of my tips would be equally applicable five or ten years ago, with junior engineers as the beneficiaries, rather than coding assistants. Today, I think the big difference between juniors and coding assistants is the ability to introspect about "why does this codebase feel so frustrating to code in?", and to figure out how to improve the situation. In part, it's this introspection process that produces senior engineers. We'll see whether LLMs can learn to develop [taste](/essays/taste/) - that's when humans will really be in trouble!
