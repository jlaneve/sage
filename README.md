![Sage_ A CLI Copilot](https://github.com/jlaneve/sage/assets/5252587/23be78fa-a6d8-4190-9d35-9b1206d17beb)

# sage

Sage is an AI copilot designed to enhance developer productivity and streamline onboarding processes. By suggesting and autocompleting terminal commands, it significantly reduces the time developers spend on routine tasks.

Many companies have specific commands for their teams and projects. With Sage, developers no longer need to waste time searching through documentation or asking colleagues for help with these commands.

Sage stores historical commands used by team members, allowing it to provide relevant suggestions based on context. It features an extension that records successfully executed commands in real-time, with built-in data redaction through Hugging Face for privacy protection. These commands are stored in a vector database, enabling hybrid search and reranking retrieval. Additionally, Sage offers RAG-based code completion for command-line suggestions, further enhancing its usability.

## demo

#### click on thumnail to watch the demo video
[![video](https://i.imgur.com/wiPWFZK.png)](https://github.com/jlaneve/sage/assets/5252587/0169f467-9be6-48d8-8e0a-71ff6b68d086)

## ingestion

![image](https://github.com/jlaneve/sage/assets/5252587/cd775df4-a072-4dca-a0ce-e7e4258196a5)

## retrieval

![image](https://github.com/jlaneve/sage/assets/5252587/4936f882-ce3b-468b-94cc-9c9eeb7cfe10)

## graph

<img width="668" alt="Screenshot 2024-04-07 at 2 24 02 PM" src="https://github.com/jlaneve/sage/assets/5252587/744cf49a-d598-49ec-a7bb-05a46b224ef3">

## local dev

Note, this was a 10-hour hackathon project and we didn't invest time into building a great developer experience, so try this at your own risk. This is also not currently deployed, so local dev is the easiest way to test it for yourself. There are 3 components:

### [oh-my-zsh](https://ohmyz.sh) plugin

This plugin captures commands as you run them. It's located in `shell/`. To install this, from the root of the repo:

1. Run the `shell/install.sh` script. This creates a copy of your `~/.zshrc` config into `shell/zsh-with-plugin.zshrc`.
2. Update the `shell/zsh-with-plugin.zshrc` and extend your `plugins` to include `tbd`. We made this first, before we decided on a name 🙂. Your plugins should then look something like this: `plugins=(git z zsh-syntax-highlighting zsh-autosuggestions tbd)`.
3. Use the `shell/zsh-with-plugin.zshrc` as your new shell by running `source shell/zsh-with-plugin.zshrc`.

This should update your shell to include the plugin. Now, whenever you run commands, they'll be sent to the local server.

### python server

There's a Python FastAPI server that powers ingestion and retrieval. It authenticates to a few different services from a `.env` file. Create the `.env` at `server/.env` and populate the following:

```
MONGO_URL=
HF_INFERENCE_URL=
HF_TOKEN=
OPENAI_API_KEY=
NOMIC_API_KEY=
COHERE_API_KEY=
```

Then, install the requirements from the `requirements.txt` file. You can run the server with `python main.py`.

### hugging face

We use [StarPII](https://huggingface.co/bigcode/starpii) from Hugging Face to flag PII, and Hugging Face inference to host the model. You need to deploy this model, as-is, to an Inference Endpoint on HF.

### mongodb

The MongoDB setup should be fairly straightforward. You need to create a deployment (we called our database `command` and our collection `recorded_commands`) and add two indices in Atlas Search:

1. A vector search index with the following config:

```json
{
  "fields": [
    {
      "numDimensions": 512,
      "path": "summary_embeddings",
      "similarity": "cosine",
      "type": "vector"
    }
  ]
}
```

2. A search index with the following config:

```json
{
  "mappings": {
    "dynamic": false,
    "fields": {
      "command_summary": [
        {
          "type": "string"
        }
      ]
    }
  }
}
```

You can then bulk ingest some sample data with `mongo_bulk_ingest.py`.

### cli

The CLI lives in the `cli/` directory and is packaged with [Poetry](https://python-poetry.org). You can run `poetry install` in the directory, which should drop you into a shell where you have access to the `sage` CLI.

You can then ask the CLI questions with `sage ask "list files"`.
