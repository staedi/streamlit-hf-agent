# streamlit-hf-agent

This is a Streamlit implementation of selected Agent codes from the [Huggingface Agent Course](https://huggingface.co/learn/agents-course).

## Organization

### Pages

This app has multiple pages based on their frameworks (i.e., [smolagents](https://huggingface.co/docs/smolagents/index) and [llama-index](https://docs.llamaindex.ai)).
- smolagents
- llamaindex

Those framework headings have the following pages.
- smolagents
- - 💻code_agent
  - 🔎agentic_RAG
  - 🔨tool_calling_agent
  - 🆒use-case

- llamaindex
- - 🎛️workflows
  - 🔨tools
  - 🕵️agents
  - 🆒use-case

### Framework backends

Each framework has the helpers definitions enclosed in the following directories.
- components
- tools
- agent

## LLMs

To run the LLMs within my local machine (Macbook Air M1), I used the [ollama](https://ollama.com) with the following models.

- `llama3.1:8b-instruct-q4_0`
- `qwen2.5-coder:7b-instruct`
