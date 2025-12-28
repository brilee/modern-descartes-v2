Interviewing for ML/AI Engineers
2025/12/22
software engineering,strategy,machine learning,popular

In my [recent job search for an ML/AI engineering position](/essays/2025_job_search/), I talked to ~15 companies, made it to onsites for ~10 companies and received 7 offers. I did ~70 separate interviews, not counting recruiter/team match calls.

My favorite interview by far was the one with Espresso AI's CTO, where we commiserated about how much the ML system design interview format sucked. And that made me wonder - who ever thought these were a good idea?

In this essay, I'd like to explain why you should probably be replacing the ML system design interview with something else.

# ML system design failure modes

Here is a brief list, all from personal experience, roughly in order of how commonly I encountered them. These failure modes are not mutually exclusive!

## System Design question in ML clothing

Many "ML systems" are actually regular systems interviews where you have to say some ML words along the way. I find this type of interview useless, because the ML questions aren't detailed enough to exclude smooth talkers, and there's less time to dive deep on the system design front.

If your interview can be passed by reciting "I would take the dataset, train a neural network on it using a softmax/cross-entropy loss, and then optimize hyperparameters while monitoring FP/FN rates. Class imbalance. Data missingness. Label noise. Overfitting." then it is a bad interview. 

## Cog In A Machine

Sometimes, the interviewer is inexperienced, and has only worked on a small corner of the overall system. They start asking really detailed and specific questions about the experience they have, like data prep, evals, production scaling, etc. while glossing over other parts of the system. They don't know how to think about or evaluate the big picture. They may also expect answers that were correct for the specific project they worked on, but not correct or relevant in general.

## Lack of scenariocrafting

Some questions are just so hopelessly vague that there's nothing to discuss. A good scenario invites good questions from good candidates, and creates specific hooks to start making design decisions around.

- Good scenario: "Our bank's customers are being scammed, and they are losing their life savings. Find a way to prevent this from happening."
- Bad scenario: "Design a fraud detection system for a banking application" 

The good scenario naturally invites good questions: "what are the downsides to preventing legitimate attempts at withdrawing large amounts in cash?" "what is the appropriate detection and intervention point?" "what levels of human discretion/override/fallback should be allowed?".

- Good scenario: "Build a Slack bot for a volunteer-run help channel that automatically @tags people who might be able to answer a question"
- Bad scenario: "Automatically route JIRA tickets to the right subteam"

The good scenario, again, naturally invites good questions: "are all messages to the slack channel necessarily questions that need routing?" "how annoyed would people be if they're @tagged on a question they can't answer?" "can we @tag anyone in the company, or do we need an opt-in/opt-out mechanism?" "what if the same person gets too many @tags?" "how much slack history do we have from the channel?" "what supplementary data do we have on org chart, tenure, team affiliations for everyone?"

When you craft detail into a scenario, you should do due dilligence: can you find industry reports/papers/blog posts detailing the peculiarities and customization needed for that scenario?

## Outdated problem

Sometimes, interview problems go stale due to advancements in ML.

In one such interview, the interviewer gave me a text content classification problem and was seemingly looking for an approach involving some flavor of embedding + classifier training. I asked how many classes needed to be distinguished, and how ambiguous those classes might be (to a human), and then suggested that a small off-the-shelf LLM with system prompting would be quick to implement and do very well. They rejected on the basis that it was "too expensive", and I ended up sketching out the tokenomics and estimated a very reasonable unit price for the task, which they accepted. But then the rest of the interview was sort of a bust because there was little left to talk about - the interviewer didn't know enough about LLMs to ask good follow-up questions to my approach.

In another interview, I was asked to design a RAG-based chatbot for technical manual lookup chatbot. I explained the weaknesses of a fixed context-injection system and explained how I would design an agentic search system instead (with vector similarity search included as a "fuzzy_lookup" tool). The interviewer seemed to have been expecting a discussion on chunking and scaling vector search. That interview was a failure on multiple fronts -- outdated question, lack of scenariocrafting, system design in ML clothing. My responses to this question are also highly likely to be stale if you're reading this essay in 2027 or beyond - it has to be understood in the context of a giant RAG popularity wave in 2024, which was already obsolete by 2025.

These interviews are often quite informative -- in the reverse direction! As a candidate, when you get one of these questions, it suggests that the company's engineers aren't keeping up to date with the rapidly changing ML field.

## Too much "rederive major algorithmic advances from scratch"

One interview problem I got was "Design a data deduplication pipeline for a large web crawl dataset". The answer is the [MinHash algorithm](https://en.wikipedia.org/wiki/MinHash) and its variants -- and no, you will not rederive this algorithm in the course of 45 minutes if you hadn't already studied it in depth previous to the interview.

Rather than testing for prior knowledge of MinHash, you should test for the ability to learn and implement MinHash in a day or two.

I would do this by requesting a position-relevant project deep dive. Perhaps that project deep dive is a data deduplication pipeline for a large web crawl dataset. Perhaps it's something else that is equally technically impressive and relevant. Either way, let the candidate choose, rather than ambushing them.

# Redesigning the ML interview loop

If we examine the requirements of an ML engineer interview loop, we can see that an ML system design interview can be swapped out in almost all cases.

A good interview loop measures the candidate's abilities and growth potential, while rejecting talkers who can't do the work. A great interview loop will also identify factors that might prevent candidate from realizing their potential, like cultural mismatches, poor fit for remote work, misalignment in type of work, etc.

## Job requirements

An ML engineer is someone who is basically otherwise qualified/capable of being a regular software engineer, but also has the ability to reason about the statistical and distributional nature of data.

Some companies need ML engineers who could rederive backprop on the spot, and others need ML engineers who can scale up GPU clusters. Some companies don't actually need ML engineers, but call their software engineer positions ML engineer, as part of a mutually self-serving title inflation game.

The skillsets below are the specific things we should be measuring with our interview loop.

### SWE skillsets

- write maintainable, bug-free, performant code (in Python, C++, or CUDA).
- implement and analyze algorithms and data structures.
- understand distributed systems and feedback loops (useful for building reinforcement learning systems).
- design, deploy, monitor, and debug production systems (useful for ML infra engineers).

### ML skillsets

- write maintainable, bug-free, performant ML code (in array languages/DSLs).
- implement and analyze ML methods (via statistics, calculus, and linear algebra.)
- do exploratory data analysis to understand e.g., what is the generating process producing this data, what missingness/quality issues does it have, what distributional skews does it have, how might it be transformed into something an ML technique can process?
- design, deploy and monitor ML systems, and diagnose data-related issues like schema/data drift.

These ML skillsets are relevant for structured data (numbers and categoricals), and unstructured data (images, text, pdf, etc.)

# Interview types

## Coding/algorithms

What: Code a solution to a LeetCode-style problem. Indexing/search/graph/tree/heap flavored leetcode-ish problems are most appropriate for ML engineers, because that's what often shows up in actual day-to-day work. Compiler-flavored problems are also great overall for software fundamentals because they typically allow for deep elegant solutions while also being approachable in a practical way for those not steeped in compiler lore.

Why: Evaluate the ability to write good code and analyze algorithms.

Comments: I've seen ML-flavored coding problems, such as implementing a transformer layer or debugging a buggy transformer implementation. I find these relatively low-signal because 80% of the complexity lies in the obscurity of numpy-flavored indexing/broadcasting, and this complexity is entirely invisible and in the candidate's head.

## Data modeling

What: Improve an existing modeling scaffold on a dataset/task in a live environment by fixing bugs, doing EDA to figure out there is a class imbalance, by changing the NN architecture, by changing the training methodology, etc.. One or more intentional bugs may be present. To spice up things, you can ask the candidate to explain why they think an improvement will work, introduce artificial constraints like a max number of NN weights, or have intentional quirks in the dataset.

Why: Evaluate the ability to write good code in Python/numpy/pandas/pytorch, analyze datasets, and analyze/implement ML methods.

Comments: This type of interview requires a lot of preparation and test-solving for a good dataset, modeling problem, and live coding environment, but I found it to be very rewarding as an interviewee and high-signal.

## Math quiz

What: Answer short, factual, math/statistics/ML questions on, e.g., computing a Bayesian update by hand, computing the derivative of the softmax function, explaining covariance matrices, or explaining why/how [KL-divergence](https://en.wikipedia.org/wiki/Kullback%E2%80%93Leibler_divergence) is asymmetric.

Why: IQ test + measures the candidate's ability to reason about math and statistics.

Comments: These quizzes are popular with finance companies and companies in the U.K. It's a different culture, and this interview style works well with a population that grew up on the [Tripos](https://en.wikipedia.org/wiki/Tripos) or any of the math/computing olympiads. However, these questions have high false negative rates on anybody outside of these cultures, so I would generally steer away from them. If you do them anyway, I would use a mix of question types (theoretical, calculation, explanation) and levels of sophistication (no math degree, undergrad degree, grad level topics) to offer maximum chance of success.

## System Design

What: Design a system that is one or more of ( large | scalable | distributed | high-throughput | low-latency | resilient ). Pick a system that exhibits the challenges that you expect to see in your day-to-day work!

Why: Tests ability to design and analyze production system, experience working with such systems. ML systems, due to their data-intensive nature, benefit from system design skills.

Comments: Most systems design interviews tend to be talky-talk interviews, but I think it's good practice to ask for concrete numbers, estimates, or equations - e.g. estimating load factors, latency/throughput numbers, identifying bottlenecks, or reasoning about various types of subsystem failure.

## ML System Design

What: Design a solution to an ambiguous product or business need. The ideal problem starts from a real user need and leaves the solution space open-ended. The ideal solution should be co-designed around product context, user experience, dataset availability, likelihood of modeling success, tasteful selection of key metrics, and post-deploy monitoring.

Why: This tests the candidate's ability to extract a plausible junior-engineer shaped ML modeling problem, their taste and judgment in deciding what problems are worth throwing ML at, and their intuition on useful datasets to feed the ML system.

Comments: Almost nobody does "ML System Design" questions as I've just described them, but it's the ideal we should strive for.

## Project Deep Dive

What: Present an ML project, discussing the motivation, problem statement, difficulties encountered, impact, and any ancillary work. New grads can talk about a class project; PhD grads can talk about their research; self-learners can show off a portfolio project; industry hires can talk about a project they worked on.

Why: This gives strong signal on the candidate's seniority level, communication skills, and motivation for ML. It also offers a chance to demonstrate some valuable role-specific knowledge - e.g. if you're hiring for a role on a recommender systems team, then the candidate that presents a great recsys projects can have a very in-depth conversation with the interviewers.

Comments: The interviewer should approach this conversation with a collaborative mindset, rather than a skeptical one, and focus on how the candidate personally experienced their project, rather than on the interviewer's conception of how such a project should have been run. (The latter frame of mind is a bad habit acquired from academia.)

## Career Chat

What: Discuss your career arc, relevant highlights, and goals for next role.

Why: This gives signal on ambition, agency, growth potential, work flavor preferences, personality, and figures out whether the company's needs match what they are looking to do next. 

Comments: This is a great call for the hiring manager to take. I think this is a strict improvement on the "tell me about a time when..." flavor of people interviews, which is susceptible to fake prepared stories.

# Putting it all together

An abbreviated loop (for startups or interns) would include 1 coding interview, 1 data modeling interview, and a project deep dive interview.

For junior candidates, I would do 2 coding interviews, 1 coding interview with strong math flavor / math quiz flavor, 1 data modeling interview, and a project deep dive interview.

For senior candidates, I would do 2 coding interviews, 2 data modeling interviews, a system design interview, a project deep dive, and a career chat with the hiring manager.

For staff+ candidates, I would do a coding interview, 2 data modeling interviews, 1 system design interview, 1 ML system design interviews, a project deep dive, and a career chat with the hiring manager.

The ML Systems Design interview has potential for very high signal, but it needs a staff-level ML engineer to execute well. Unfortunately, there's a shortage of capable interviewers, given the empirical population pyramid of the field. That's why I only put it on the staff+ candidate loop. For what it's worth, I think that startup founders/early employees are qualified to run these kinds of interviews, and it might be worth throwing them into the hiring loop for ML/AI talent.

For strong candidates, there is no stronger pitch to join, than to present a slate of talented and thoughtful interviewers who could be their future coworkers, and an interview process rigorous enough to assure them that all of their coworkers will have been as thoroughly examined.
