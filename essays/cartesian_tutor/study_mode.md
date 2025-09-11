What ChatGPT Study Mode gets right and wrong
2025/7/29
cartesian tutor,llms

# Introduction

Today, OpenAI released [Study Mode](https://openai.com/index/chatgpt-study-mode/), a new ChatGPT features that offers step by step guidance instead of quick answers.

I've been working on a [startup in the AI tutoring space](https://www.moderndescartes.com/essays/tags/cartesian_tutor/) for the last few months, and Study Mode looks a lot like an [early prototype](/essays/5_16_2025/) I built. Having dogfooded this product for a month or two, here's what I find Study Mode to be good/bad for.

# The Socratic method has advantages

At its core, Study Mode is build around the idea of Socratic back-and-forth, relying on the LLM's knowledge of "core curriculum" to help guide the student in the right direction. This has a number of benefits:

- The student is actively engaged, rather than passively reading the ChatGPT answer.
- The student gets a chance to demonstrate the flaws in their thinking, which ChatGPT can pounce upon and correct.
- The students' unknown unknowns are typically within the LLM's world knowledge. The Socratic method is a great way to suss out these unknown unknowns.

# The student runs the lesson

The fundamental problem I found with the Socratic method is that the student is still in the driver's seat. This can be good, if the student is epistemically curious enough to systematically explore their blind spots. However, I have had sessions with my own tutor where I latch onto what I _think_ is a key idea, and the LLM will enthusiastically encourage me and build upon my "insight". Later on, I realize that this insight is 1. not actually that central of an idea and 2. led me to completely miss the actual lesson. Overall, the vibe is one of a tutor that didn't prep for the session and is just winging it.


## Problem solving

One flavor of this issue is when when the LLM doesn't always solve the problem correctly - especially when its context is being contaminated with potentially incorrect attempts from the student. On more difficult problems, the LLM will eagerly encourage mistakes and end up hopelessly confused along with the student. Here, it is useful to asynchronously solve the problem with a much more powerful model, summarize the key points of the solution, identify potential alternate solutions, and then system prompt the LLM to constrain the students' progress to these guardrails, offering hints as needed.

## Lesson planning

Another place this goes awry is with lesson planning. I figured that one solution to this might be analogous to the coding agent technique of "plan, then execute", where you first sketch out the lesson to be learned, and then learn it. However, this runs into the fundamental problem where you need to have expertise and taste in order to decide whether the lesson sketch is any good.

Here, a temptation might be to fall back upon the known syllabi of various classes - whether it's courses downloaded from MIT OCW, or course outlines for the AP tests. This sort of works, but suffers from the problem that the writers of K-12 curricula are often people with PhDs in education - people who have never practiced in the field they are now setting teaching standards for. You end up with pablum like this example taken from the Common Core State Standards for Mathematics:

> Students grasp the concept of a function as a rule that assigns to each input exactly one output. They understand that functions describe situations where one quantity determines another. They can translate among representations and partial representations of functions (noting that tabular and graphical representations may be partial representations), and they describe how aspects of the function are reflected in the different representations.

Putting this into the system prompt of an LLM will cause the LLM to start talking like this. You do **not** want to learn from a teacher that talks like this, I promise you.

Using the syllabus of a college course works better, because professors are overall more knowledgable and get direct feedback on the quality of their own curriculum. I think some version of Study Mode will make it into college campuses via Learning Management System products, with professors given a relatively simple interface where they can dump their curriculum/lesson notes/problem sets.

# Learning, to what end?

I think Study Mode will drive incremental signups of ChatGPT Plus, and possibly help in enterprise sales to schools. I don't see it being a killer app, though. Study Mode falls prey to a misconception common to highly educated people (including myself!): that people want to learn for the sake of learning.

Education is an [umbrella term](/essays/7_28_2025/#thoughts-on-the-fragmented-state-of-education), much in the way cancer is an umbrella diagnosis. Very few students learn for the sake of learning. Most students are instead seeking a diploma/certification/license/degree/test score (call this the "terminal goal"), for which they will begrudgingly learn something so they can pass an exam. To build a product that people will pay for, you have to help them meet their terminal goal, rather than selling them on the idea of learning better/faster. Solving that terminal goal often involves integrating, e.g. spaced-repetition flashcards, paced learning plans, good problem solving sequences, etc.., and need software support (not just raw LLMs).

The educational products market will remain fragmented because the set of terminal goals that people have is fragmented. There will likely be an LLM-powered app that captures the MCAT prep market, another that captures the remedial math market, another that captures the contest math market, and so on.

I think the beauty of Study Mode is that it ~75% works for just about anything you throw at it. ChatGPT was already a strong baseline that I found hard to beat, and Study Mode will be an even stronger one. Generic GPT wrapper education products will need to narrow in on their target audience and terminal goal if they want to survive.
