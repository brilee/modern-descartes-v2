The AI Infra War: Winners and losers
2025/2/14
strategy,llms

Competition is brutal in the world of LLMs. In March 2024, Databricks released [DBRX](https://www.databricks.com/blog/introducing-dbrx-new-state-art-open-llm), an open-weights, MoE-style LLM that was at the top of all the leaderboards for a grand total of 3 weeks. It was overtaken by Meta's [Llama 3](https://ai.meta.com/blog/meta-llama-3/), a series of LLMs that probably cost 100M+ to build, and was released... for free. You don't even remember DBRX. I only remember because I work at Databricks.

The early adopter community races to download and vibe-check each new release. Yet, it's becoming increasingly clear that foundation models are becoming commoditized. Over the next 5-10 years, a few companies will specialize in serving foundation models at scale with thin margins, while the real winners will be a diverse ecosystem of vertical businesses that own the relationship with the user. Teams that balance the rapid pace of change with rigorous evals will be able to move fast and rearchitect their systems when necessary.

# A small number of companies will serve LLMs

Empirically over the last 3-4 years, LLM price @ constant quality has improved at [triple speed compared to Moore's law](https://a16z.com/llmflation-llm-inference-cost/) (2x reduction every six months, compared to Moore's 2x reduction every 18 months). In 2024, improvements were actually quadruple speed thanks to a giant VC funding glut and price wars, but I expect 2025-2030 to see "merely" triple or double Moore speeds. These improvements come from a mix of hardware improvements, engineering optimizations, and scientific breakthroughs. All three legs favor the centralization of effort in a small number of companies.

On the hardware front, there's the original [Moore's law](https://en.wikipedia.org/wiki/Moore%27s_law) with a 1.5x improvement year over year. A menagerie of companies are either developing accelerators to compete with NVidia's GPUs (AWS, Google, Cerebras, Grok, and I suppose AMD) or partnering with one who has such accelerators (Anthropic->AWS). The large capital expenditures and fixed overhead of chip design naturally point towards centralization.

On the engineering front, scale justifies the engineering investment needed to continuously eke out 10-20% efficiency gains in places like optimal KV-caching, optimal GPU fleet sizing, Pareto-optimal throughput vs. latency, load balancing/queueing algorithms and so on.

On the scientific front, look no further than the [DeepSeek v3 paper](https://arxiv.org/abs/2412.19437), a tour de force of hardware-software-research synergies. Mixed precision inference, speculative decoding, mixture of expert models, multi-token prediction, and latent attention are just the beginning.

Overall, maintaining pace with this brutal 4x year over year improvement requires all three legs to succeed, and LLM companies that don't take advantage of all three legs will find themselves being outcompeted by companies that do. For everyone else, there will be hosted LLM APIs at a reasonable price.

# Simple agents will win over complex frameworks

In the 1990s and 2000s, when Moore's law was in its heyday, it made sense to repurchase a brand new PC every 2-3 years or so, because each upgrade got you a 3-4x improvement in computing speed. A similar dynamic played out in smartphones over the 2010s. Of course, this didn't actually mean that your experience got 4x better; an increasing level of software bloat has meant that a simple calculator GUI application today consumes ~ 1,000 times more computing resources than the same command-line calculator application did 30 years ago.

The reason for this bloat is simple: a team writing in a high-level language like Python or Javascript could deliver innovative software experiences to market several times faster than a competitor using C/Java could, and even if the competitor could deliver a product that was 10x more efficient with computing resources, that advantage would be gone within a few years. The rapid iteration speeds possible in high-level languages resulted in _continuously compounding_ product improvements, whereas using C/Java resulted in a one-shot speed improvement whose magnitude did not increase over time.

Companies that embrace the LLM improvement treadmill will outcompete companies that ossify themselves in an overcomplicated software framework. As of this essay's publication time, it's already cheap and effective to just let an [LLM run OCR on a screenshot of your PDF](https://www.sergey.fyi/articles/gemini-flash-2), rather than investing in software that "does it right" by parsing the PDF binary contents.

The relentless pace of LLM improvements implies that if you merely migrate to the latest LLMs every 6-12 months, this alone will give you amazing quality/cost improvements. I say "merely", but migration requires investment into trustworthy evaluation suites. These suites will also pay off when generational improvements in the base LLM allow the developer to confidently rearchitect and remove software components from their system.

# Bifurcation of do-it-yourself vs. AI-as-a-Service

Overall, I expect the LLM industry to follow the software industry. Despite the wide availability of excellent free-to-use OSS software, managed services and infrastructure companies are collectively worth trillions of dollars today.

Sure, you can self-host a Postgres database on a Docker container on a VPS for $100/year. I wager that if you are capable of doing this, you already have a job in tech that pays well over $100,000/year. For a non-tech business, $10,000/year for a managed Postgres database is a bargain, even at 100x the cost of the underlying compute. It is simply impossible to compete for expertise when SaaS companies can offer triple the salary to build and offer the same services to thousands of companies.

The DIY alternative here is not Postgres, but Microsoft Excel, which I would guess powers something like ~1-10 trillion USD in small business GDP. Excel is a very intuitive, approachable database solution that is so simple that most "serious programmers" don't even think of it as a database. But if you think about Excel's functional role in many small companies' business processes, it absolutely is a database.

Spreadsheet software took twenty years to become ubiquitous, and it also took twenty years for Google Search to become ubiquitous. Over the next twenty years, humans and LLMs will coevolve a prompting language that everybody will just know as the "right" way to instruct an LLM to do some useful work. As knowledge and ease of LLM prompting improve over time, an "Excel for LLMs" will take off, enabling people with low tech literacy to DIY their own workflows and software.

# Cost per query will span many orders of magnitude

A few years ago, LLMs came in sizes ranging from the barely useful 1B parameter sizes, to the (still) mind-bogglingly large 175B parameters of GPT3. They only took plain text in and out, roughly 10-1000 tokens on either end. Nobody actually thought you could serve a GPT3-sized model to end-users, and such work was seen as pushing scientific frontiers rather than for any practical purpose.

Today, LLMs range in size over 2-3 orders of magnitude - from the surprisingly competent mini 1B parameter sizes, to the 671B-parameter DeepSeek R1 - and R1 is actually being served to end users today. Additionally, LLMs can take plain text as input in a chat context (10-1000 input tokens), or they can take massive PDFs, images, audio, and other multimedia inputs (1,000-10,000 input tokens). Finally, their output can be a simple 10-100 tokens for a straight response, 100-1,000 tokens for a prompt that explicitly asks the LLM to perform chain-of-thought, or 1,000+ tokens for reasoning models.

For context, a human speaking continuously can generate 10,000 tokens an hour and speed-read 50,000 tokens an hour, while today's frontier LLMs (~100B params) cost about $10/million tokens. In other words, it would cost <10 cents an hour to replace a call center operator, and <50 cents an hour to service a chat window. Realistically, since humans aren't continuously reading or talking, the cost will be one tenth of the above numbers. Reasoning models, assuming the human only reads the final output, are 10-100x more expensive. Human I/O is far more expensive than LLMs these days - even the reasoning LLM variants.

In the future, I anticipate models as small as 100M parameters will become surprisingly useful for a variety of tasks. Google Translate on my phone downloads a ~50MB "language pack" per language to be able to translate offline; if you can translate a pair of languages for 50MB, I bet there are many other surprisingly useful things you can do at that size. On the upper end, 1T parameter models are likely to start showing up within one or two generations of Nvidia hardware refreshes, and when you pile reasoning / thought tokens on top of that, we're looking at something like 6-7 orders of magnitude range in cost between tiny and gigantic reasoning LLMs.

# Value per query will span many orders of magnitude

While the cost per query will vary dramatically based on model size and complexity, the economic value generated by these queries will vary even more dramatically, creating interesting arbitrage opportunities.

Since the Industrial Age, civilization has worked to automate as much labor as possible, while utilizing human flexibility to fill in the hard parts with human labor. The "hard" stuff is often not what you think it is. In an Amazon warehouse, inventory management is a tremendously difficult intellectual problem, handled mostly by software, while packing varied items into boxes turns out to be a tremendously difficult physical problem, handled mostly by humans.

Similarly, LLMs are very good at some things while being very bad at others. There is not necessarily any correlation between "LLM strengths" and "economic value", leading to new arbitrage opportunities between human and LLM effort. Here's a few areas I see being big opportunities:

- Information propagation: Jensen Huang has 60 direct reports and runs large group meetings, because he's a madman and he wants to maximize information throughput to/from his company. You could approximate this by removing half your middle managers ($1000-10000/hour) and letting an LLM monitor your chat messages and answer easier questions on your behalf (say, $10/hour for the highest quality reasoning models).
- Tutoring: This currently costs $50-200/hour, but it could be done competently at $0.01/hour by an LLM for all topics up through high school. Relatedly, therapists are essentially emotional tutors.
- Call centers: This currently costs $10/hour at outsourced rates, but it could be done competently at $0.01/hour by an LLM.
- Translation: This currently costs $10-100/hour for professional translations, but it could be done at $0.01/hour for good-enough translations.

Another type of LLM value is their scalability and flexibility. Imagine the effort that goes into ramping up humans to deal with anticipated one-off spikes in demand, let alone unanticipated spikes in demand. We can summon and then dismiss many copies of the same agent for tasks of all shapes and sizes, at any time of your choosing. There is no need to deal with the headaches of outsourcing - timezones, cultural nuances, accents, international business operations. You can have 24/7 coverage with uniform response quality, instant global rollout of policy changes or other improvements in agent quality. That level of consistency is typically paid for in Enterprise "Call us!" levels of pricing, but can now be had for the price of an on-demand GPU.

# Conclusion

A simple extrapolations of trends that I think have robust foundations, with a dash of history. And yet the conclusions are surprising. The world of 2030 will be as unrecognizable to us as the world of cellphones today was in 2010, and as the world of the connected Internet was in 2000.
