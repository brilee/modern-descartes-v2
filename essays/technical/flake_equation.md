The Tyranny of the Flake Equation
2024/6/11
software engineering,statistics

I once worked with an algorithm whose runtime scaled roughly linearly with the number of rows of data. To date, the largest job we'd ever attempted had taken a few hours. One day, we tried to run a job that was only four times as large as our previous largest job. We figured we'd just leave it running for a day and it would be complete. Instead, due to frequent job preemption and other flakiness, the job took almost two weeks to complete! Each time, the easiest path forward was to restart and pray for good luck. I joked that we'd somehow discovered an algorithm with exponential runtime.

When I went back and did the math, it turns out we did, in fact, have exponential runtime! If flakiness is proportional (with rate $p$) to the base flake-free runtime of the job, then the flake equation says that total runtime grows exponentially with job size.

$$O(f(n)) \rightarrow O(f(n)\cdot e^{p\cdot f(n)})$$

When the expected number of flakes is less than one, we're in the flat part of the exponential term, and flakiness is an occasional nuisance. However, as the expected number of flakes exceeds one per run, the likelihood of job success drops exponentially. If you retry the job until it completes, you can expect to wait some time that is exponential in the job size.

The derivation is pretty simple. The expected number of flakes is $O(p\cdot f(n))$, and then the probability that you complete the job with zero flakes is, by the [Poisson distribution](https://en.wikipedia.org/wiki/Poisson_distribution), $O(e^{-p\cdot f(n)})$. Inverting this probability, we see that on average, we must repeat the job $O(e^{p\cdot f(n)})$ times before a job completes without flaking.

# A grand unified theory of bug fixes

Flakiness is not just bad luck. It is a failure to design for the realities of the production environment. And yet we only have limited engineering hours to fix all possible scenarios. Flakes are omnipresent, passing through our software like neutrinos through the Earth, and we cannot and should not try to fix them all. The only folks who actually worry about literal cosmic rays, are NASA, who must deal with elevated radiation in space with extended mission times, precisely the two terms that show up in the flake equation's exponential term.

The flake equation presents a sharp decision boundary: any specific flake will exist in one of two regimes: occasionally annoying, or oppressively showstopping. As you scale up software usage, flakes flip from the former regime to the latter, giving you the shortest of warning periods during the transition. In my experience, great engineers can sniff out early hints of flakiness and fix them while the exponential is still in the somewhat flat parts of its growth curve, allowing teams to scale smoothly.

Because of the exponential growing penalty associated with these flakes, there is no ignoring flakes - as soon as a flake mode starts to rear its head, you will not be able to scale more than 2x past your current level without seeing that flake grow into a reliable job-killing monster.

# Flake-prone contexts

Software scaling can happen in many forms: in job size, in job volume, in heterogeneity of deployment environments, and in the diversity of user journeys. Each of these scale ups presents an opportunity for an previously innocuous flake mode to go exponential. You will encounter increasingly obscure modes of flakiness, and you will have to fix them, or stop growing. Your software's growth rate is capped at the rate at which you can fix these showstoppers.

We can see the flake equation most clearly in software whose usage grows continuously in multiple dimensions.

## Continuous integration

One haven for flakiness is in continuous integration and testing, where developer activity generates both increased volume and heterogeneity of tests. CI is particularly pernicious because there is often no recourse to a failed CI run other than to simply rerun the entire test suite! Software teams adopt the following mitigations to stave off the inevitability of flaky CI:

- reduction in scope of how many tests need to run with each change
- discipline in not writing inherently flaky tests (no random numbers, no network connections, no complex containers/servers etc.)
- granular retries of failed tests, with tests marked pass if the second try passes.

Test-level retries seems to irritate some folks who think that we should focus our efforts on reducing flaky tests in the first place, but I will point out that retrying is dead simple to activate and reduces the flake equation penalty from $e^{p\cdot O(f(n))}$ to $e^{p^2\cdot O(f(n))}$, while fixing flaky tests consumes developer time linear to each fixed test. It allows teams to exponentially flatten the global failure rate while continuing to derive value from individual flaky tests. (Presumably the flaky tests still generate some value, otherwise they ought to be deleted entirely!)

## Large Language Model Training

Another contemporary haven for flakes is LLM training runs. LLM scaling implies scaling up in volume and variety of data, quantity of hardware being orchestrated, and duration of training. As training runs scale from GPT2 to GPT3 to GPT4 to GPT5 sized models, increasingly obscure failure modes are encountered. To give an example of a GPT3-scale flake, if the average lifetime of a GPU is 5 years, then if you run a cluster of 500 GPUs for a week, well.. that's about 10 years of GPU time. Two of the GPUs will die on average per run, and how will the code respond to that?

For LLMs, checkpointing is the canonical solution to flakiness. It's a powerful solution because it covers a broad class of flake modes, whereas rearchitecting to detect and recover from failed GPUs, irregular network connectivity, etc. is far harder and requires deep engineering expertise for each flake mode fixed.

### Checkpointing optimization

Some fun math, feel free to skip: if there are $\lambda$ expected flakes per run, the whole job costs $N$, rate of flakes is $p$ (with $Np = \lambda$), and checkpointing costs $C$ per checkpoint save, then what is the optimal frequency of checkpointing?

Let's assume all progress since the last checkpoint is lost if a flake occurs, and that the checkpointing operation itself is flake-free. Then, we can track the total cost of a job as the cost to reach each checkpoint. Call the number of checkpoints $f$. The cost to reach each checkpoint is $\frac{N}{f}e^{Np/f}$, and the total cost is $Ne^{Np/f} + Cf$.

We can take the derivative w.r.t. $f$ to find the minimum of this function to be the solution of the following equation:

$$-N^2p/f^2 * e^{Np}/f + C = 0$$

Rearranging, we get the following equation:

$$f^2e^f = \frac{N^2p^2e^{Np}}{pC}$$

As an approximation to the solution, let's guess that $f = Np$ (i.e. if there are 5 expected flakes per run, then take 5 checkpoints). In that scenario, we're left with the equation $pC=1$, or equivalently $fC = N$. So in other words, if there are 5 flakes, and we checkpoint 5 times, and the cost of one checkpoint is roughly 1/5th the cost of the whole job, then this is the optimal frequency of checkpointing. If checkpointing is cheaper than that, then we should checkpoint more frequently than the expected number of flakes, and vice versa.

# Conclusion

It is highly counterintuitive to me that the retry penalty of flakiness is exponential, rather than linear. I think the reason is that we so rarely manage to glimpse and understand this transitionary phase from mostly flat to exponential blowup. Either the job is only mildly flaky/annoying (in which case the Taylor approximation to the exponential is, in fact, linear), or it is so annoying that it already got fixed.

There are contexts in which we live this transitionary phase for years: sometimes company growth is *just* slow enough that the exponential growth term comes on gradually over one or two years. In these scenarios, the metaphorical frog is boiled, and only an outside perspective can comprehend the stupidly low productivity. From the inside, it just feels like a bad case of tech debt. While the "tech debt" diagnosis is trivially true, the underlying insight is that incremental tech debt gets added together, and then exponentiated - so that each marginal unit of debt is responsible for another multiplicative slowdown for the whole team! As companies scale, technical excellence and investments into developer productivity teams is what forestalls the tyranny of the flake equation.