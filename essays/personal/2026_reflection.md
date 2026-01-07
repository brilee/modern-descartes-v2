New year reflections
2026/1/7
personal,llms

Reflecting on this past year, I feel grateful and lucky for everything that's happened to me, both personally and professionally.

I'm writing this from a remote town in Switzerland, where I train-hopped my way from Rome over the course of 3 days. My return journey is being pushed indeterminately due to cascading flight cancellations from Amsterdam winter storms. I have no hotel/travel sketched out past tomorrow. Each new day brings new experiences, new scenery, new weather, new cuisines, new cultures, and the discomfort of adjusting to yet another bed. I'm enjoying my travel, but I'm also looking forward to coming back home, whenever that ends up being.

My Eurotrip, intended to be a breather before my new job, has unintentionally become a metaphor for my professional life over the last 3 years.

# Corporate ronin

My situation at Google became unstable when Osmo spun out from Google in June 2022. Instead of simply joining an existing team, I'd been trying to pitch a new project in Climate+ML, ableit unsuccessfully: "your project is credible at 10 megatons of $\ce{CO2}$ offset (\$100M equivalent), but that still isn't big enough. 100 megatons or bust", they told me. Defeated, I spent my paternity leave thinking deeply about the [incentive structures driving Google Research](/essays/why_brain/).

A week before I was scheduled to return from leave, I was laid off. I bounced in between ideas and opportunities, trying to decide what [new mountain](/essays/new_mountains/) I wanted to climb. I ruled out drug discovery + ML. I tried getting into management consulting but nobody was hiring. I tried a self-driving car startup but found the startup incurably dysfunctional (they had 30% layoff a few months after I left). Finally, I thought I'd found a home with Lilac, a LLM data tooling startup run by two former coworkers from Google Research. Alas, it was not to be.

Six months after I'd joined Lilac, we got acquired by Databricks, which seemed like a logical home for the team at the time. I thought that Databricks might become my new long-term home, but 9 months in, the verdict was in: I wasn't fitting into Databricks culture. I found myself checking the calendar, thinking, "just a few more months till my vesting cliff", and started seeing myself in this [short story](https://www.scottsmitelli.com/articles/ideal-candidate/). The vesting cliff passed and I left for greener pastures. Databricks and the Lilac founders treated me super respectfully through the whole process, so there's no ill will on my end. I was unlucky, Databricks was unlucky, and we all parted ways agreeably. The 6 months at Lilac were engrossing and I'm super grateful to the founders for letting me join their adventure.

My solo startup, Cartesian Tutor, was the next six months of my life, and it's the most fun I've had since I last took a sabbatical to teach myself ML in 2016. In retrospect, I wasn't being entirely honest with myself about why I was doing it - I had vague hopes about making some money, but ultimately I wanted to learn about LLMs, and just not have a boss for a while. That, I accomplished in spades -- what I learned in six months would probably have taken me or anyone else two years to learn in the context of a normal job. My recent [job search](/essays/2025_job_search/) would not have been anywhere as successful if I'd jumped right into it after Databricks.

# Finding employer-employee fit

Empirically, employer-employee fit (let's call this EEF) has been tough to find. Over the past 3 years, only Lilac has been an EEF.

I wondered at times if it was a "me" problem. Many people seemed capable of doing what needed to be done in a corporate setting; why couldn't I do the same? If we're being honest, it's because I'm too opinionated and confident in my own skills and judgment to take marching orders from someone whose skills and judgment I don't respect. Perhaps I'm overconfident, but I don't think it's a problem - most people are systematically underconfident and that tends to stop them from taking action. So then, the alternate solution is to find a job where I have the agency to find and solve the problems I think are important, at a company whose management I respect.

EEF, for me, is finding a company that 1. needs cutting-edge research 2. believes they need cutting edge research 3. has a culture of enabling researchers to solve problems.

Many companies that believe they need cutting edge research don't actually need cutting edge research, and when reality comes knocking, they fold their research bets, reorging their researchers into the corporate machine. A few need cutting edge research but are structurally incapable of believing it due to [innovator's dilemna](https://en.wikipedia.org/wiki/The_Innovator%27s_Dilemma). And some that need it and know they need it, can't help but stick their fingers into the cake while it's being made, leading to mutual dissatisfaction.

Jane Street needs agents, believe they need agents, and have a culture that has been lovingly described as an anarchist commune. I did a lot more due diligence on culture fit this time around, compared to the very short time I had to think through the Databricks-Lilac acquisition, so I'm optimistic and hopeful that this will be a good EEF.

# Feeling lucky

Throughout my journey, I've been humbled and honored by my friends, classmates, and colleagues who have helped me in my search. I also feel lucky that every time I've been thrown into uncertainty, I've emerged stronger. I've lived long enough now to witness several of my classmates' lives and careers derailed by a variety of issues self-inflicted (pessimism), unlucky (long COVID), and horrifying (murdered someone). There is a strong survivor bias to the success stories you read online, and I'm grateful that I am one of those stories.

# Obligatory AI section

2025 was the year coding agents got good enough for just about _everyone_ to boost their productivity by roughly 2x, whereas in previous years they were not at that breakeven point yet. I personally estimate my productivity boost at 2-4x, depending on the project. I am grateful that my departure from Databricks was fortuitously timed with the release of Sonnet 3.5. 

I am in agreement with Andrej that it is [possible to get to 10x](https://x.com/karpathy/status/2004607146781278521) with just the models we have today, if we just refactor/refine our workflows and interactions with the agents.

If you still haven't at least tried coding agents, you are either living under a rock or suffering from some sort of cognitive dissonance.

That being said, claims of coding agent progress are confounded by multiple factors:

1. People who do insufficient verification of Claude's output and are impressed that it is 90% correct. (The last 10% takes exactly as long as it did, pre-coding agents, because it is no longer a coding problem, it is a task specification problem.)
2. People are trying coding agents for the first time, and they ascribe their "wow" moment to specific incremental improvements in Opus 4.5, rather than to the cumulative progress made over the past few years, leading to perpetual headlines of "$LATEST_MODEL represents another phase change in coding".
3. The most impressive demonstrations come from incredibly experienced engineers, the kind who could probably implement the whole thing from scratch in a week if you cleared their calendars. Their demos tend to be in areas they are deeply familiar with, if not an outright copy of something they've built before (and can anticipate all the pitfalls).
4. Some of the strongest proponents of coding agents are clearly in some sort of LLM psychosis. (looking at you, [Steve Yegge](https://steve-yegge.medium.com/welcome-to-gas-town-4f25ee16dd04)) And yet, I can't stop reading their ravings, for they are an endless pool of fresh ideas that I can mix into my entropy stream.
5. Almost all of these demos are _solo_ projects. In team settings, the main bottleneck is actually ensuring that the team has a shared, accurate mental model of the problem domain and the solution.

Inverting each of these points, we arrive at a roadmap for getting to 10x productivity.

1. If task specification is the bottleneck, then the fundamental iteration loop to be optimized is allowing the user to interact with the generated artifact and decide which parts of it they want to change. The coding agent should be able to interact with the generated artifact in the same way to verify correctness.
2. There is currently no substitute for hands-on experience in understanding what these agents are capable of and what they tend to be good or bad at.
3. If you want to maximally harness the power of coding agents, you will need to at least learn the basics of your application domain, to the point where you can speak the [shibboleths](/essays/llm_shibboleths/). I myself did not reach full productivity on Cartesian Tutor's web app until I had spent a ~month learning web fundamentals.
4. Stay skeptical of Steves. But definitely read his blog and try his slop for flavor. I absolutely agree with his push towards reinventing workflow technologies, like issue trackers, in text-based, agent-friendly forms.
5. Not sure, but one starting point is to have regular team meetings where the latest updates to the [information architecture](/essays/ai_codebase/#information-architecture-should-be-handwritten) are reviewed. 

Progress in building software is no longer about writing code. It is about reaching a full understanding of the problem, along with a full specification for a solution. For the vast majority of software products, iteration on a working product is the fastest way to discover unknown unknowns and resolve ambiguities. Once a fully specified solution (including information architecture) is available, then coding agents can build your codebase from scratch, without the messy iteration history that tends to muck up codebases with tech debt.
