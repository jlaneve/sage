"Generate Summary of Command"
import re
from typing import Dict, List
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT_SUMMARIZER = """You are a command summarizer. \
You will be given a command starting with "Command:" with the command string surrounded by ``` blocks. \
Your task is to summarize the command with no more than 3 sentences. If the command is simple, then 1 sentence should suffice. \
The summary should be concise and informative. Do not provide unnecessary comments. \
For example, here are 2 example inputs below:

Example 1 Command: 
```
ls -l
```

Example 1 Output:
Lists the files and directories in the current directory in long format, providing detailed information such as file permissions, ownership, size, and modification date and time. Each item in the list is displayed on a separate line.

Example 2 Command: 
```
perl -pi -e 'BEGIN { print "A new line" }' $(find . -name '*.py')
```

Example 2 Output:
Add "A new line" on top of each *.py files under current directory

"""

USER_PROMPT_TEMPLATE_FOR_SUMMARIZER = """Command:
```
{cmd}
```
"""
def generate_command_summary(cmd: str) -> str:
    """
    Generate a summary of a command using LLM
    """
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        temperature=0.3,
        max_tokens=600,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_SUMMARIZER},
            {"role": "user", "content": USER_PROMPT_TEMPLATE_FOR_SUMMARIZER.format(cmd=cmd)},
        ]
    )
    return response.choices[0].message.content


# Test
# print(generate_command_summary("md5sum $(which gcc)"))
    
SYSTEM_PROMPT_RAG_CODE_COMPLETION = """You are a command line bash code completion model. \
You will be given a prompt starting with "Prompt:" with the prompt string surrounded by ``` blocks. \
You will also be given a list of retrieved most relevant commands to the prompt that have been previously used by the user's coworkers. \
Your task is to use the prompt and the retrieved relevant previous commands to generate a new command line bash code. \
The new command line bash code should be a valid bash command that is relevant to the prompt. \
If the relevant previous commands are not useful, you can ignore them. \
Surround the output command with ``` blocks. \

For example, here is an example input below:
Example Prompt:
```
Command to list just the files in the current directory
```

Example Retrieved Commands:
Previous Command 1:
`ls`: List files in the current directory
Previous Command 2:
`ls -a`: List all files in the current directory, including hidden files
Previous Command 3:
`ps -ef`: List all running processes

Example Output:
```
ls
```
"""

USER_PROMPT_TEMPLATE_FOR_RAG_CODE_COMPLETION = """Prompt:
```
{prompt}
```

Retrieved Commands:
"""

DOC_TEMPLATE_FOR_RAG_CODE_COMPLETION = """
Previous Command {index}:
`{command}`: {summary}
"""
def extract_content(input_string):
    pattern = r'```(.*?)```'
    matches = re.findall(pattern, input_string, re.DOTALL)
    return matches

def complete_command_code_with_rag(prompt: str, retrieved_docs: List[Dict[str, str]]):
    """
    Generate command line code based on user prompt and retrieved documents
    """
    user_prompt = USER_PROMPT_TEMPLATE_FOR_RAG_CODE_COMPLETION.format(prompt=prompt)
    docs_info = ""
    for i, doc in enumerate(retrieved_docs):
        docs_info += DOC_TEMPLATE_FOR_RAG_CODE_COMPLETION.format(index=i, command=doc['command'], summary=doc['command_summary'])

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        temperature=0.3,
        max_tokens=600,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT_RAG_CODE_COMPLETION},
            {"role": "user", "content": user_prompt+docs_info},
        ]
    )
    
    llm_response = response.choices[0].message.content
    code_blocks_in_response = extract_content(llm_response)

    if len(code_blocks_in_response) > 0:
        return code_blocks_in_response[0]
    else:
        return ""
