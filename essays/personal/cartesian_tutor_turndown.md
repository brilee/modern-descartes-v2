Next steps for Cartesian Tutor
2025/11/3
personal,cartesian tutor,strategy

6 months ago, I started building Cartesian Tutor to explore AI tutors as the future of education. It's been an incredibly rewarding journey and despite the lack of commercial success, I've learned a tremendous amount. A++ experience, highly recommended.

I'll be job searching over the next few months. If you are looking for an AI-pilled staff software engineer with deep expertise in ML and LLMs who is also capable of fullstack prototyping and thinking holistically about product/technology/strategy, let me know. My search pipeline is currently underindexed on Boston-area / remote jobs, so these are especially welcome. **EDIT: my calendar is pretty full right now, no longer looking to start new interview processes.**

I'm happy to keep Cartesian Tutor up and running for students' sake, and as a continuing hobby project.

In this essay, I'll do a light postmortem and talk about what went well, what went poorly, and how I would do things differently next time.

# What I built

Cartesian Tutor scales 1-on-1 tutoring with AI.

Education is due for a change. The standard classroom model has many weaknesses: too many students to have dedicated 1:1 time for each student, too few students to achieve economies of scale in producing quality content, and enough variation in ability that the entire class moves at the pace of its 25%ile student.

Textbooks and YouTube creators set the bar for scalability. 1:1 tutoring sets the bar for effectiveness. Could we have both with AI tutors?

Let's look at why tutors are so effective. A tutor builds a mental model of their student: thinking style, misconceptions, knowledge gaps, working habits, and more. Using this mental model, the human tutor plans and delivers the specific lesson that most rapidly brings the student to mastery. Broken down as subtasks:

- inspect and debug the student's thought process by asking carefully crafted questions
- design curriculum and lesson plans
- create, maintain, incrementally update a model of the students' knowledge set
- deliver a lesson through some mix of didactic and Socratic instruction.
- (for high school students and younger) interface with the parent to align on goals and to do some light family therapy.

The Socratic method built into [ChatGPT's Study Mode](/essays/study_mode) is but one tiny step in this direction. I found that LLMs were not particularly good at any of the other subtasks. (That hasn't stopped a number of AI education companies from pushing slop generation products to teachers...)

Cartesian Tutor uses a mix of AI-delivered lessons/problem review with traditional software and hand-curated curriculum, practice tests, and lesson plans, and the result seems to work decently. An especially important ingredient here is human exam-writers' taste in writing good questions that can't just be solved by pattern matching/plug-and-chug. Students' failed attempts at solving these olympiad questions create a trail that AI can follow to diagnose students' weaknesses.

In addition to this core product offering, I also built:

- User acquisition funnels.
- Content scraping/generation/management system built around a hybrid AI/human review workflow.
- Engineering infra for rapid iteration + deployment of changes.
- Logging, billing, product analytics integrations to figure out how users were using my product.

# Why give up?

When I started, I and many other people believed that there was some nonzero chance that AI would quickly overtake many job descriptions, empowering small teams to compete toe-to-toe with larger incumbents by leveraging AI agents. I tried my hand at setting up an AI council to dispense startup advice; using AI tools to generate marketing copy; using AI tools to vibecode my frontend. None of this panned out. I believe now that most jobs are safe, and "startup founder" the safest of all, given how much adaptability, taste, and judgment it demands.

So, what should we make of the many recent examples of highly successful AI-centric startups, all of which have shown unprecedented growth rates and revenue numbers? VCs would love to spin the narrative that "AI changes everything", but I attribute this wave of hypergrowth startups to a different combination of factors:

1. tumult of mass layoffs pushing many potential founders to pull the trigger on doing a startup.
2. end of ZIRP encouraging a focus on revenue growth over headcount growth.
3. a flood of AI investment from VCs as well as traditional companies _all_ throwing 1-2% of their budget at AI experiments. Some subset of those AI experiments are now panning out, leading to a doubling-down of investment.

So fundamentally, I am heading back into the job market because my assessment is that I can create (and capture) the most value by working as an AI specialist employee at one of these highly successful AI-centric companies, rather than as a generalist startup founder.

That being said, I think it is highly likely that I will try another startup in the future. Hence, the notes.

# Things I would change for my next startup

## Focus

My efforts over these past 6 months were split between:

1. building a successful business
2. putting AI through its paces and learning its strengths and weaknesses
3. learning how to build a company

While I failed at my first goal, I made amazing progress on the second and third goals. I don't regret learning about AI or building companies, but next time will be a clear focus on building a successful business.

I also spent some time consulting for another ed tech company, which generated some revenue, helped sharpen my consulting skills, and helped me see a very different way of working with Claude -- but ultimately I think this was just another distraction I could do without next time.

## Environment

I originally thought it would be a waste of money to go for a coworking subscription when I had a nice WFH setup, but in retrospect it would have been a good idea. My most productive times were in busy coffeeshop environments, even if I was missing my split keyboard/widescreen monitor.

Physical health could have used more attention. My previous daily routine included a bike ride into the office, and without that, I found my physical fitness gradually dropping, until I suffered some sort of acute lower back injury. I've recovered and am doing more yoga to help strengthen my core.

## Fortuitous encounters

Overall, I was surprised at how often much I enjoyed random meetings with old and new friends. Part of this was undoubtedly the social isolation that comes with being a solo founder. I also found the conversations helpful in refining and developing ideas for my startup. This time, I spent ~2% of my time meeting people, and next time I think I should spend more like 5-10% meeting people. As a Boston-based founder, the base rate of fortuitous encounters is a lot lower, so it's worth being deliberate about finding and chatting with people.

# Things I wouldn't change

## Blogging

The [weekly blogging thing](/essays/tags/cartesian_tutor/) was honestly great. It helped me sort through the zillion thoughts that were running through my head and set weekly goals for myself. Community-wise, many people I chatted with had read many or all of my updates. It sparked many good conversations, and at a time when so many people are looking for informed takes on where AI is going, it was a great way to build some reputational currency.

## Flex days and working pace

I worked roughly 30-50 hours/week during this startup period. Looking at the pattern of my work hours, I found myself working in extremely productive 2-4 hour bursts, followed by a few hours after to recover. I found the following times particularly productive

- 5-8AM before the family was really up and about.
- 10AM-1PM on weekdays, when I was fresh.
- 4-6PM on weekdays after I had recovered from the morning sprint.
- 10AM-2PM on weekends if I felt the itch to keep on building.
- more rarely, 9-11PM, after family went to bed and I had showered and had lots of interesting shower thoughts/ideas on what to build.

Given how little overlap there is here with a traditional 9-5 working schedule. I'll have to think about how I can create these optimal conditions in my next job.

I also took many opportunistic hiking trips to New Hampshire when the weather was particularly nice. I never regretted this, as I got to spend quality time with family and found it refreshing enough that I easily made up the missed time on the next day.

There were also many days when I found myself extremely unproductive, or procrastinating on some specific thing that I was dreading doing. For these days, just getting started was the most important thing, and I often found that spark by asking Claude to do it for me. Still, many other days went by where I actually did manage to procrastinate the whole day. Those days, you just have to accept that there's something else on your mind, write off that day, and just let your mind chew on whatever it's chewing on.

# Startup learnings

- Find your first customer/user, even before you have a product. It is the business equivalent of writing your tests/specs before writing the code. I don't think I would use the "build vaporware marketing/landing pages until somebody clicks through and asks where the product is" strategy, but I have renewed appreciation for how to-the-point it is.
- You really can't underinstrument your app/website. Even something as simple as knowing "which menu item do they click first upon landing on your site?" is a hint at what they find most intriguing or valuable.
- Relatedly - run surveys as part of onboarding. These surveys are so important in figuring out why somebody found you and what they want out of your product.
- A buffet of features is what happens when you have enough users that you are your own distribution channel, and upselling is worthwhile. Until you hit that point, you are searching for the one feature that users must have, that they will abandon their existing solutions for. Don't cargo-cult larger companies with established product suites.
- Find the right mix between low-cost experimentation and polished product development. Better to showcase your best feature than to overwhelm with many mediocre features.
- Do things that don't scale. Even if the premise of Cartesian Tutor was "scale myself with AI", I should have manually tutored some number of students, just to get a visceral sense for what they are struggling with on a day-to-day basis and what they need in terms of software/tutoring/lesson support.
- When optimizing for SEO, study competitors to figure out what their recurring new customer funnels are. For example, one competitor in Cartesian Tutor's space offers brand-new practice olympiad exams every year, and this ends up as a recurring source of new students who are looking for practice olympiads.

# Acknowledgments

To my wife, for giving me the time, space, and encouragement to try a startup.

Fred, for giving me emotional permission to move on from Cartesian Tutor.

Loyal readers of my blog and mailing list, for the many great suggestions, feedback, and connections.
