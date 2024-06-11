Small Data, Big Compute
2024/3/31
software engineering,machine learning,strategy,popular

LLMs are really expensive to run, computationally speaking. I think you may be surprised by the order of magnitude difference.

While working at Lilac, I coined a phrase "small data, big compute" to describe this pattern, and used it to drive engineering decisions.

# Arithmetic intensity

Arithmetic intensity is a concept [popularized by NVidia](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html#understand-perf) that measures a very simple ratio: how many arithmetic operations are executed per byte transferred?

Consider a basic business analyst query: `SELECT SUM(sales_amount) FROM table WHERE time < end_range AND time >= start_range`. This query executes 1 addition for each 4-byte floating point number it processes, for an arithmetic intensity of 0.25. However, the bytes corresponding to `sales_amount` are usually interleaved with the bytes for `time` and `row_id` and everything else in the table, so only 1-10% of the bits read from disk are actually relevant to the calculation, for a net arithmetic intensity of 0.01.

Is 0.01 good or bad? Well, computers can read data from disk at roughly 1 GiB per second, or 250M floats per second; they can compute at roughly 8-16 FLOPs per cycle, with 3GHz clock speed = 25-50B float ops per second. Computers therefore have a 100:1 available ratio of compute to disk. Any code with an arithmetic intensity of less than 100 is underutilizing the CPU.

In other words, your typical business analyst query is horrendously underutilizing the computer, by a factor of about 10,000x. This mismatch is why there exists a $100B market for database companies and technologies that can optimize these business queries (Spark, Parquet, Hadoop, MapReduce, Flume, etc.). They do so by using columnar databases and on-the-fly compression techniques like [run-length encoding, bit-packing, and delta compression](https://duckdb.org/2022/10/28/lightweight-compression.html), which trade increased compute for more effective use of bandwidth. The result is blazing fast analytics queries that actually fully utilize the 100:1 available ratio of compute to disk.

How many FLOPs do we spend per byte of user data in an LLM? Well... consider the popular 7B model size. As a rough approximation, let's say each parameter-byte interaction results in 1 FLOP, for an arithmetic intensity of $10^{10}$ operations per byte processed. Other larger LLMs can go to $10^{13}$. You could quibble about bytes vs. tokens or multiply vs. add and the cost of exponentiation. But does it really matter if it's 8 or 9 orders of magnitude more expensive per byte than the business analyst query? Convnets for image processing have an arithmetic intensity of $10^4$ - $10^5$. It's large but not unreasonable, which is why they've found many applications in factory QC, agriculture, satellite imagery processing, etc..

Needless to say, this insane arithmetic intensity breaks just about every assumption and expectation that's been baked into the way we think about software for the past twenty years.

# Technical implications

## No need for distributed systems

Unless you work at a handful of companies that train LLMs from scratch, you will not have the budget to operate LLMs on "big data". A single 1TB harddrive can store enough text data to burn 10 million dollars in [GPT4 API calls](https://help.openai.com/en/articles/7127956-how-much-does-gpt-4-cost)!

As a result, most business use cases for LLMs will inevitably operate on small data - say, <1 million rows.

The software industry has spent well over a decade learning how to build systems that scale across trillions of rows and thousands of machines, with the tradeoff that you would wait at least 30s per invocation. We got used to this inconvenience because it let us turn a 10 day single-threaded job into a 20 minute distributed job.

Now, faced with the daunting prospect of a mere 1 million rows, all of that is unnecessary complexity. Users deserve sub-second overheads when doing non-LLM computations on such small data. Lilac utilizes DuckDB to blast all cores on a single machine to compute basic summary statistics for every column in the user's dataset, in less than a second - a luxury that we can afford because of small data!

## Massive budget for bloat

Ordinarily, inefficiencies in per-item handling can add up to a significant cost. This includes things like network bandwidth/latency, preprocessing of data in a slow language like Python, HTTP request overhead, unnecessary dependencies, and so on.

LLMs are so expensive that everything else is peanuts. There is a lot more budget for slop and I fully expect businesses to use this budget. I am sorry to the people who are frustrated with the increasing bloat of the modern software stack - LLMs will bring on yet another expansionary era of bloat.

At Lilac, we ended up building a per-item progress saver into our `dataset.map` call, because it was honestly a small cost, relative to the fees that our users were incurring while making API calls to OpenAI. In comparison, HuggingFace's `dataset.map` doesn't implement checkpointing, because it would be an enormous waste of time and compute and disk space to checkpoint the result of a trivial arithmetic operation.

## Latency-batching tradeoffs

GPU cores have a compute-memory bandwidth ratio of around 100 - they are not fundamentally different from computers in this regard. Ironically, LLMs end up bandwidth-limited despite the insane arithmetic intensity quoted above. If you also count the parameters of the model in the "bytes transferred" denominator, then LLM arithmetic intensity is roughly $\frac{nm}{n + m}$, with n = input bytes and m = model bytes. Since $m \gg n$, arithmetic intensity is proportional to $n$. Increasing batch size is thus a free win, up to the point where the GPU is compute-bound rather than bandwidth-bound.

For real-time use cases like chatbots, scale is king! When you have thousands of queries per second, it becomes easy to wait 50 milliseconds for a batch of user queries to accumulate, and then execute them in a single batch. If you only have one query per second, you are in a situation where you will either get poor GPU utilization (expensive hardware goes to waste), or users will have to wait multiple seconds for enough accumulated queries to make a batch.

For offline use cases like document corpus embedding/transformation, we can automatically get full utilization through internal batching of the corpus. Because GPUs are the expensive part, I expect organizations to implement a queueing system to maximize usage of GPUs around the clock, possibly even intermingling offline jobs with real-time computation.

## Minimal viable fine-tune

As a corollary of "compute cost dominates all", any and all ways to optimize compute cost will be utilized. We will almost certainly see a relentless drive towards specialization of cheaper fine-tuned models for every conceivable use case. Stuff like [speculative decoding](https://arxiv.org/abs/2302.01318) shows just how expensive the largest LLMs are - you can productively run a smaller LLM to try and predict the larger LLM's output, in real time! 

In between engineering optimizations, fine-tuning/research breakthroughs, and increased availability of massively parallel hardware optimized for LLMs, the cost for any particular performance point will decrease significantly - some people claim 4x every year, which sounds aggressive but not even that unreasonable - 1.5x each from hardware, research, and engineering optimizations gets you close to ~4x.

I expect there to be a good business in drastically reducing compute costs by making it very easy to fine-tune a minimal viable model for a specific purpose.

# Business implications

## Data egress is not a moat

Cloud providers invest a lot of money into onboarding customers, with the knowledge that once they're inside, it becomes very expensive to unwind all of the business integrations they've built. Furthermore, it becomes very expensive to even try to diversify into multiple clouds, because data egress outside of the cloud is [stupidly expensive](https://www.hostdime.com/blog/data-egress-fees-cloud/). This is all part of an intentional strategy to make switching harder.

Yet, the insane cost of LLMs means that data egress costs are a relatively small deal. 1GB of egress costs ~$0.10, while embedding 1GB worth of text would cost ~$50. As a result, I expect that...

## A new GPU cloud will emerge

Because of the ease with which small data can flow between clouds, I expect a new cloud competitor, focused on cheap GPU compute. Scale will be king here, because increased scale results in negotiating power for GPU purchase contracts, investments into GPU reliability, investments into engineering tricks to maximize GPU utilization, improved latency for realtime applications, and investments into data/security/compliance certifications. Modal, Lambda, and NVidia seem like potential cloud winners here, but the truth is that we're all winners, because relentless competition will drive down GPU costs for everyone.

## Attack > defense

A certain class of user-generated content will become a Turing Arena of sorts, where LLMs will generate fake text (think Amazon product reviews or Google search result spam or Reddit commenter product/service endorsements), and LLMs will try to detect LLM-generated text. I think it's a reasonable guess that LLMs will only be able to detect other LLMs of lesser quality.

Unfortunately for the internet, I think attack will win over the defense. The reason is safety in numbers.

A small number of attackers will have the resources to use the most expensive LLMs to generate the most realistic looking fake reviews, specifically in categories where the profit margins are highest (think "best hotel in manhattan" or "best machu picchu tour"). However, a much larger number of attackers will have moderate resources to use medium-sized LLMs to generate a much larger volume of semi-realistic fake reviews. The defense, on the other hand, has to scale up LLMs to run on all user-generated content, and realistically they will only be able to afford running medium or small LLMs to do so. Dan Luu's [logorrhea on the diseconomies of scale](https://danluu.com/diseconomies-scale/) is exactly the right way to think here.

# Conclusion

"Small data, big compute" allowed us to optimize for a certain class of dataset and take certain shortcuts. The Lilac team will be [joining Databricks](https://www.databricks.com/blog/lilac-joins-databricks-simplify-unstructured-data-evaluation-generative-ai) and I look forward to continuing to build systems tailored to the unusual needs of LLMs!