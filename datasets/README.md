# MAPS Datasets
The first Multilingual Agentic AI Benchmark for evaluating agentic AI systems across different languages and diverse tasks.

Benchmark enables systematic analysis of how agents perform under multilingual conditions. To balance performance and safety evaluation, our benchmark comprises 805 tasks: 405 from performance-oriented datasets (GAIA, SWE-bench, MATH) and 400 from the Agent Security Benchmark. We selected 165 tasks from GAIA (full validation set), 140 high-difficulty tasks from MATH (20 per topic across 7 topics), and 100 hard and medium tasks from SWE-bench. The remaining 400 tasks include all safety-relevant prompts from ASB. Each task was translated into 11 target languages resulting in a total of 9.6K multilingual tasks. 

## Dataset Details
### Dataset Description
This benchmark is designed to evaluate agentic AI systems for both performance and safety across a wide range of tasks in a multilingual setting. It enables testing how well agents perform when operating in different languages, covering realistic tasks from multiple domains:

**GAIA**: Web search and tool-use tasks that test an agent’s ability to interact with external tools and follow multi-step reasoning.

**MATH**: Complex mathematical problem-solving tasks from seven topics, requiring structured reasoning and accurate computation.

**SWE-bench**: Software engineering tasks involving real-world GitHub issues, focusing on code understanding, bug fixing, and technical reasoning.

**ASB (Agent Security Benchmark)**: Safety-focused tasks designed to probe agent behavior under adversarial or sensitive scenarios, ensuring safe and aligned outputs across languages.

## languages
Each task in the benchmark is translated into the following 11 languages to enable comprehensive multilingual evaluation: Spanish (es), German (de), Arabic (ar), Russian (ru), Japanese (ja), Portuguese (pt), Hindi (hi), Hebrew (he), Korean (Ko), Italian (it), Cheinese (zn-ch)

### Dataset Size
Each dataset in the benchmark includes a fixed number of instances per language, all translated into 11 languages. Below is the breakdown (including english):

**GAIA**: 165 tasks per language × 12 languages = 1,980 tasks total
**MATH**: 140 tasks per language × 12 languages = 1,680 tasks total
**SWE-bench**: 100 tasks per language × 12 languages = 1,200 tasks total
**ASB**: 400 attack per language × 12 languages = 4,800 attacks total
