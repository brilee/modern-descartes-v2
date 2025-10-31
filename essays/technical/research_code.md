A Research Codebase Manifesto
2023/2/14
software engineering,machine learning,popular

_Note: Multiple people have told me that this essay could equally well have been titled "A Startup Codebase Manifesto". YMMV._

At Google Brain, I was the tech lead of a team with multiple researchers and engineers actively running experiments and committing changes to a shared codebase. This codebase has generated feedback like "you have no idea how much i miss our old codebase", "this is a textbook example of what a research codebase should look like", and "I was curious how company X's research codebase would look and it's a complete mess compared to your codebase". (For curious googlers: you can find this codebase if you search for CLs submitted by brianklee@).

Managing a research codebase is difficult. I have heard of other research teams that attempted to join their many research subprojects' codebases, only to run into issues around code ossification, slower iteration cycles, and general researcher frustration. Yet other research teams, wary of these issues, embrace the academic baseline of untended anarchy (yes, even at Google).

Here are some of the lessons I've learned in helping our team make the best use of our codebase.

For some context, our team was roughly a 1:2 mix of engineers to researchers, and we worked on machine learning applied to molecular property prediction and representation learning. My advice is probably more useful for industry research groups and less useful for academic research groups. It will be difficult to bootstrap this type of codebase discipline without an engineering champion in your group.

# Codebase evolution

Writing a one-person research codebase is easy. The difficulty arises when you try to maintain this codebase over multiple people and over time. Software engineering best practices are designed to alleviate these issues, but the usual recommendations don't always work, because research codebases change far faster than product codebases. The stakes are higher, too - a stagnant product codebase can still generate business value, but a stagnant research codebase simply fails at its core purpose: to investigate and evaluate new ideas.

Here are some of the most common ways research teams respond to evolving research interests.

- Change code without caring about compatibility. The result is spooky breakage at a distance. A researcher can check in changes that progress their research by 1x and retard everyone else's research by 0.5x each, for a net drag on productivity. If everybody has their own solo codebase, then there are fewer costs to breakage, but also fewer benefits to collaboration. (This is the academic default.)
- Carefully update code, maintaining compatibility with project code. As older projects accumulate, the backwards compatibility tax grows and grows.
- Don't change code. Often groups end up in this category because their research group turned into a product group, but regardless of the reason, it spells the death of new research.
- Start over from scratch, copying code snippets from the old codebase as needed.

Each strategy has its pros and cons. I found the following strategy effective within my team.

# The Three-Tier Codebase

This strategy is a mix of approaches (2) and (4).

- Core. Libraries for reusable components like cloud data storage, notebook tooling, neural network libraries, model serialization/deserialization, statistics tests, visualization, testing libraries, hyperparameter optimization frameworks, wrappers and convenience functions built on top of third-party libraries. Engineers typically work here.
  - Code is reviewed to engineering standards. Code is tested, covered by continuous integration, and should never be broken. Very low tolerance for tech debt.
  - Breaking changes to core code should be accompanied by fixes to affected project code. The project owner should assist in identifying potential breakage. No need to fix experimental code.
- Projects. A new top-level folder for each major effort (rough criteria: a project represents 1-6 months of work). Engineers and researchers work here.
  - Code is reviewed for correctness. Testing is recommended but optional, as is continuous integration. 
  - No cross-project dependencies. If you need code from a different project, either go through the effort of polishing the code into core, or clone the code.
- Experimental. Anything goes. Typically used by researchers. I suggest namespacing by time (e.g. a new directory every month).
  - Rubber-stamp approvals. Code review is optional and comments may be ignored without justification. Do not plug this into continuous integration.
  - The goal of this directory is to create a safe space for researchers so that they do not need to hide their work. By passively observing research code "in the wild", engineers can understand research pain points.
  - Any research result that is shared outside the immediate research group may not be derived from experimental code.

The key idea is that when project-specific code is not generating research value, it is not worth upkeep and should be amputated. By configuring project-specific code to be amputation-ready, the codebase as a whole stays healthier. If this feels strange to you, remember that your job in a research group isn't to write code, it's to do research, and this remains true whether your job description says Engineer or Researcher/Scientist.

This structure solves for some tricky dynamics, which I will explain further.

## Engineer/Researcher collaboration

Tensions arise when engineers and researchers interact in a single codebase. Engineers have a shared understanding of software best practices, e.g. testing code, reusable functions, single-responsibility principle, etc.. Researchers, on the other hand, don't see the benefits of such best practices and resent the drag on their individual productivity.

This tension most commonly manifests during code review. Engineers tend to impose demands on researchers' code before it can be checked in, whereas researchers tend to rubber-stamp each others' code, leaving engineers to feel like they are permanently on clean-up duty. Researchers, annoyed by the slowdown in code velocity, will evade the code review mechanism by iterating in private on a solo code repository or by working entirely in notebooks instead of proper modules. Engineers' tools go underutilized because codebases are not integrated.

One of the strengths of the three-tier codebase is that it helps engineers and researchers collaborate by setting code review expectations. The benefits include healthier team dynamics, increased probability of correctness, mutual learning opportunities, and overall a happier team.

## Keeping track of code

Another strength of the three-tier codebase is centralization of code. Centralization creates a single source of truth, encourages core code reuse, and streamlines workflows. It's important enough that the sole purpose of the Experimental directory is to discourage the creation of private codebases. A Colab notebook on Google Drive or an unpushed git branch on your laptop's hard drive count as private codebases, in this reckoning. Ultimately, a shared codebase is a foundation for shared progress and learning.

In the absence of centralization, many inefficiencies arise. If you haven't struggled to recover the precise version of some notebook that generated figure 4 in your paper, which Reviewer 2 is now critiquing, then have you really done research? What about haggling with your IT department's privacy lawyers to try and salvage a python notebook from a former intern's returned laptop?

That being said, you shouldn't bother checking in every snippet of throwaway code. A good rule of thumb is that you should check in code only if the result was interesting enough to share with your team. (I mean result in a general sense: an explanation, knowledge, a specific number, and _especially_ a dataset.) If you wouldn't pollute their mindspace during group meetings, why would you pollute the codebase?

# A comment on notebooks

Some people hate notebooks because they are sometimes not much more legible than a transcript of an interpreter session. They can even introduce new and exciting failure modes, usually due to out-of-order execution or hidden state due to overwritten/deleted cells. Yet, they're an indispensable part of the research toolkit. 

Not all notebooks are worth checking in. As mentioned before, a good cutoff criterion is whether the notebook generates a research result that you thought interesting enough to share with your team. When you check in a notebook, the following steps will minimize unnecessary sadness for future readers and users of the notebook (including yourself):

- delete nonessential cells
- check in cell output (but do trim noisy/verbose output)
- restart kernel and run your notebook from top to bottom to check for out-of-order execution issues

Despite my statement about experimental being "anything goes", I do think the above steps are easy enough that they should be insisted upon even for experimental code.

# Keeping up with the times

One final pathology endemic to research codebases is the build-or-buy dilemma. By their very nature, research codebases are typically on the cutting edge of what people are interested in building, and there are rarely well-built libraries for the thing you are trying to accomplish. So at first, build is really the only option. But unless you have a large enough engineering budget (cough DeepMind cough) that you can create your own ecosystem of well-polished first-party solutions, time will eventually produce a third-party solution that does it better.

The three-tier codebase forces an explicit decision to polish and promote project code into core. Good judgment is necessary to decide whether to polish something into core or to procrastinate by just copying old code into a new project directory. Neither decision is necessarily wrong. My hit rate was roughly 60% of our core libraries which are still the best available solution to their problems, which seems decent. As a case study on one of the 40% I missed on, consider our graph neural network library.

We built our own TF2 graph neural network (GNN) library in late 2019, mere months after TF2's release. It was customized for molecules, taking advantage of carbon's four-valence constraint to optimize the adjacency list representation. I was the resident TF2 expert in the Cambridge research office, so it seemed like a natural choice at the time. But if we had to restart today I would probably go with [JAX/Jraph](https://github.com/deepmind/jraph), publicly released in late 2020. 

We never made the jump to JAX/Jraph, because the cost-benefit never seemed to be worth it. (JAX's static shape requirements and serialization weaknesses significantly increased the migration costs, while our small molecule datasets limited the upside to better GNN architectures.) While the existing GNN libraries worked well for what we were doing, it impeded new research in subtle ways - hypergraph or multi-molecule architectures were forever on our horizon because they were difficult to implement. I overinvested in our GNN libraries and they subsequently got interwoven into our workflows, making it difficult to migrate away.

The "obvious" solution is to cut your losses early and migrate as soon as a better library is identified, but that's easier said than done. It's particularly impressive if you can identify and switch to a library with a better trajectory, even before it reaches feature parity with your existing libraries. DeepMind's early 2020 decision to shift their entire organization to JAX continues to impress me with its foresight.

# Parting thoughts

Academic research groups often complain about the inequality of resources relative to industrial research groups. Compute resources typically come to mind, but another important inequality is industry's ability and willingness to hire engineers alongside researchers. The difference is structural: even though engineering wisdom is free and readily available online to any grad student who wishes to obtain it, it rarely happens because that's not what gets you your PhD. And even then, merely hiring an engineer is not enough to make your research group more productive. Integrating the research and engineering worlds requires researchers to understand when engineering is necessary, and engineers to understand when it is not. It's a culture shift that's hard to pull off.
