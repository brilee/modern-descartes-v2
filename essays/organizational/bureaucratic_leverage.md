Bureaucratic Leverage
2023/12/12
strategy,popular

Why do we hate bureaucracy?

Taken literally, a bureaucracy is just an organization tasked with ensuring some outcome. In the public sector, OSHA ensures worker safety, FDA ensures drug safety, EPA ensures environmental protection; in the private sector, HR ensures legal compliance, IT ensures trade secrets and data privacy, and so on. Yet even if people agree with the outcome, they often disagree with the implementation. Bureaucracies have an endless talent for finding wasteful and ineffective solutions.

Bureaucracies are ineffective due to a lack of accountability. If a bureaucrat imposes a wasteful policy, what are the consequences? Well, as long as they are achieving their desired outcome, they are doing their job, regardless of the pain they inflict on others. They can wield legal, technical, or financial penalties to force compliance. And paradoxically, when bureaucrats fail to achieve their desired outcome, they often get a bigger budget or a bigger stick to wield, rather than being fired for incompetence. The inability to recognize failure goes hand in hand with the inability to recognize success: competent and ambitious people avoid working for bureaucracies because their efforts go unrewarded. Bureaucracies end up staffed with middling managers, and we have learned to hate them.

I don't know how to solve this problem in the public sector, but I think it's solvable in the private sector, because there is theoretically a CEO who is incentivized to maximize the overall effectiveness of the company; they just need the right tactics. The solution is simple: **hold bureaucracy accountable by forcing them to do the actual work**. Let me explain.

# Bureaucratic leverage

Bureaucracies usually don't do any work. This is true in two layered senses:

- they don't accomplish primary objectives; they are in the business of ensuring secondary objectives.
- they don't do the work of accomplishing the secondary objectives either; the work is usually pushed onto the same people accomplishing the primary objectives.

To give a concrete example: the FDA doesn't research, develop, or manufacture the drugs; pharmaceutical companies do. The FDA merely ensures that the drugs are safe and effective. And in ensuring so, the FDA doesn't run the clinical trials; instead, the pharmaceutical companies are responsible for running the trials at cost, and submitting the paperwork to the FDA.

**Bureaucratic leverage** is defined as the ratio of work produced for _external entities_ to do, relative to the amount of work _directly done_ by the bureaucracy. In this example, the FDA's 2023 human drugs budget was $2.3 billion dollars [(reference)](https://www.fda.gov/media/166182/download?attachment), while the U.S. clinical trials market was $25 billion dollars [(reference)](https://www.biospace.com/article/releases/u-s-clinical-trials-industry-is-rising-rapidly-usd-35-1-bn-by-2030/). To a first approximation, the FDA's human drugs subdivision therefore has a bureaucratic leverage ratio of 11x.

To give another example, GitHub in 2020 [changed the default git branch name from `master` to `main`](https://github.com/github/renaming), a change intended to promote greater inclusivity of historically and currently enslaved peoples. I would estimate that roughly 3 person-months of GitHub's effort went into considering the impact and implementation details of this change - a very generous and thoughtful investment into inclusivity. Yet, the changes imposes a global cost that I would roughly estimate at ~1 million affected developers * 15 minutes per developer = ~300 person-months of effort, for an approximate bureaucratic leverage ratio of 100x.

A high bureaucratic leverage ratio is not intrinsically a bad thing. However, scope insensitivity is a real problem: when a bureaucrat wields 100x leverage, it is a heavy responsibility that is easily underestimated. There are situations I've seen at Google where every hour of downtime costs the company millions of dollars - and a crack team of site reliability engineers whose combined hourly wages are tens of thousands of dollars are desperately working to get it back up. That is the level of urgency that a 100x leverage ratio _should_ demand. Does the typical bureaucrat with a 100x leverage ratio behave with that level of urgency? Absolutely not.

# Creating bureaucratic accountability

"Force bureaucracies do the work" now takes on a more precise definition: we should hold bureaucracies to a 1x bureaucratic leverage ratio.

The rationale is simple: it is globally efficient for a bureaucracy to spend 1 unit of time, if it will reduce everyone else's workload by more than 1 unit of time. At this breakeven point, the bureaucracy will have done roughly 50% of the total work. This rule is not meant to be taken too literally, since these quantities are difficult to measure precisely.

From the bureaucrat's point of view, this means that they have two budgets to manage: their internal budget, and the external budget for asking other organizations to do something. Bureaucrats will be incentivized to reexamine and optimize their external demands. From everyone else's perspective, they can be assured that what they're asked to do has been priority-sorted - or if it hasn't been, they can at least be assured that there's a limited amount of it they'll be asked to do.

The truth is, this external budget has always existed - implicitly - in the form of compliance. Consider a badly run IT/security department. They run third-party security scanners on the company's servers, and file hundreds of low-value automated tickets with other teams to fix. They require frequent password changes and relogins. They ban installation of all non-approved apps and drag their heels on approving new apps. A few days of "work" can easily generate years of lost productivity for product teams, if their demands are taken at face value.

In practice, people have limited tolerance for bullshit; if you flood their bug tracker with automated security reports, they'll just bookmark a custom search page that filters out security reports. If you require frequent password changes, they'll use a formulaic password or keep a password post-it on their monitor. If you drag your heels on approving apps, they'll upload the company data to a webapp or run it off a USB stick. The oft-cited "bullshit umbrella" role of managers is essentially a rate-limiter on bureaucracy.

On the positive side, centralization of work creates economies of scale - a topic [I've previously discussed in the context of code quality](/essays/codemates/#you-get-a-papercut-you-get-a-papercut-everybody-gets-a-papercut). A bureaucrat forced to grapple with personally doing a lot of repetitive paperwork will very quickly decide that some paperwork was never necessary and will invest in solutions to autofill fields where possible.

# Embedded bureaucrats

In a past life as a bureaucrat, my manager asked me to spend my first three months doing a rotation with a partner team for three months. On paper it looked like he was just donating his headcount to other teams, but I was amazed at how many secondary benefits came out of this rotation program.

- It made us insiders: by working alongside the partner team, we became friends and our requests were readily accepted by the partner team.
- We empathized with our partners: since we knew what burden our requests would create, we could try to avoid wasted effort and respect our partners' time.
- It made us credible: our partners could see that we were competent and that they should believe us if we said something was necessary.
- It was an advance payment: by giving free resources to the partner team, we could later ask for at least that much without questions asked.

This rotation arrangement seems like a no-brainer to me, at least within the company context. Something I don't understand is why this is frowned upon as a "revolving door" of corruption in the public sector, when it is so plainly beneficial in the private sector.

# Conclusion

Creating bureaucratic accountability begins with eliminating excuses, which eventually lets us measure performance, punish poor performance, and reward excellence. The usual excuse is noncompliance - "we made bad demands and people ignored/worked around us. If only we had a bigger stick to enforce compliance, we would have been able to accomplish our goals." A bureaucracy with a limited external budget means that people who find ways to do more with less will be rewarded - the right alignment of incentives.
