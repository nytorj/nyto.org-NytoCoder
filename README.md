# nyto.org-NytoCoder
Coder assistant using OpenAI chat-gpt om backgroud. Works similary to auto-gpt, gpt-engineer, smol, etc.

# Usage:
- pip install -r requirements.txt
- python final_main.py

- You will be asked to enter your project name.
- Then you will be asked what do you want to build... 
- You can either type it out, or hit enter and the script will load prompt.md instead.
- Just edit prompt.md if you want a larger and more detailed prompt.

# Demo:
  https://youtube.com/nytoCoder/...
# Tech:
- The code imports several modules and packages such as `os`, `sys`, `time`, `json`, `openai`, `ast`, `shutil`, `random`, and custom modules from the `lib` package.
- It sets the OpenAI API key to a specific value using `openai.api_key = "YOUR_API_KEY"`. This key is necessary to make requests to the OpenAI API.
- The `AI` class is defined, and it has various methods to interact with the OpenAI API and perform certain operations.
- The `response_raw` method takes a message as input and sends it to the OpenAI Chat Completion API to get a response. It handles errors, retries requests with exponential backoff, and returns the generated response.
- The `response_fnc` method is similar to `response_raw` but also includes a custom function call.
- The `write_file` method writes content to a file specified by `file_path`. If the directory does not exist, it creates the necessary directories.
- The `add_messages` method adds a new message to a list of messages based on the specified role ("system", "assistant", or "user").
- The `extract_filepath` method extracts file paths from a JSON string and adds them as messages to the existing list of messages.
- The `extract_filecode` method extracts a file code from a response and returns it. If the extraction fails, it returns an error message.
- The `exit_program` method prints a message and exits the program.
- The `delete_directory` method deletes a specified directory if it exists.
- The `output_messages_parser` method parses document content and extracts file codes and file paths.
- The `start` method is the entry point of the script. It prompts the user to enter the name of a project and a prompt for the project. It then calls the `main` method to initiate the interaction with the OpenAI API.
- The `main` method handles the conversation flow with the OpenAI API. It starts by creating an instance of the `AI` class and setting up initial messages. It then interacts with the user, retrieves responses from the API, extracts file paths, and generates files based on the responses.
- The `main` method also includes a loop to continue the conversation and generate files until the user decides to exit.

- Enjoy
