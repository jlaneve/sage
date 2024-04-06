"Generate Summary of Command"
from openai import OpenAI

client = OpenAI()

SYSTEM_PROMPT = """You are a command summarizer. \
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

USER_PROMPT_TEMPLATE = """Command:
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
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_PROMPT_TEMPLATE.format(cmd=cmd)},
        ]
    )
    return response.choices[0].message.content


# Test
# print(generate_command_summary("md5sum $(which gcc)"))
    
    