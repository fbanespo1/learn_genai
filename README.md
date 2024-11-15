# Learn GenAI

A package to learn Generative AI through practical examples.

## Installation

1. Install Ollama:
   Follow the instructions at [Ollama's official website](https://ollama.ai/) to install Ollama for your operating system.
   For this project is important download the correct models, because the package is made using those specific models. Please

   ```bash
   ollama pull nomic-embed-text
   ```

   This is the embedding model for Ollama. Now go for the main model:

   ```bash
   ollama run llama3.2:3b
   ```
   
   
3. Install the learn_genai package:

```bash
pip install learn_genai
```


## Usage

After installation, run the application with:

```bash
learn_genai
```


This will open a Streamlit interface in your default web browser, where you can explore three use cases:

1. Text Summarizer
2. RAG Chatbot
3. LangGraph Agents

Each use case demonstrates different aspects of Generative AI using the Llama3.2:3b model and other advanced NLP techniques.

