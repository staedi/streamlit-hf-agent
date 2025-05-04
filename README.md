# streamlit-hf-agent

This is a Streamlit implementation of selected Agent codes from the [Huggingface Agent Course](https://huggingface.co/learn/agents-course).

## Organization

### Default

For generic helper functions, the following files are available.

- [root]
  - streamlit_app.py: Entry point file
  - frontend.py: Frontend-related functions
- helpers
  - utils.py: Generic utility functions

### Pages

This app has multiple pages based on their frameworks (i.e., [smolagents](https://huggingface.co/docs/smolagents/index) and [llama-index](https://docs.llamaindex.ai)).
- smolagents.py
- llamaindex.py

Those framework headings have the following pages.
- smolagents
  - 💻code_agent.py
  - 🔎agentic_RAG.py
  - 🔨tool_calling_agent.py
  - 🆒use-case.py

- llamaindex
  - 🎛️workflows.py
  - 🔨tools.py
  - 🕵️agents.py
  - 🆒use-case.py

Note: Only the pages with the framework which is installed are shown.
For instance, if the Streamlit app is being run in the environment, under which `llamaindex` has been installed, only `llamaindex` pages are displayed.  


### Framework backends

Each framework has the helpers definitions enclosed in the following directories.
- components
- tools
- agent

## LLMs

To run the LLMs within my local machine (Macbook Air M1), I used the [ollama](https://ollama.com) with the following models.

- [llama3.1](https://ollama.com/library/llama3.1/tags): `llama3.1:8b-instruct-q4_0`
- [qwen2.5-coder](https://ollama.com/library/qwen2.5-coder/tags): `qwen2.5-coder:7b-instruct`


## To run

### Requirements

The following is required.

- LLM models via [ollama](https://ollama.com)
- Framework libraries having been installed (either, [smolagents](https://huggingface.co/docs/smolagents/index) or [llama-index](https://docs.llamaindex.ai))

### Entrypoint

Run the following command under the environment where the framework is installed.

```
streamlit run streamlit_app.py
```