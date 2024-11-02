## Install Instructions

Install Django

`pip install django`

Install the OpenAI package

`pip install openai==0.28`

## Run the program

Change into directory with setting.py file. 

```
cd LeadGenerationApp
```

Run the server

```
py manage.py runserver  
```

## Set Up OpenAI API Key

To securely access OpenAI’s API, store your API key in an environment variable:

**On Windows, set the API key in the environment:**

```
setx OPENAI_API_KEY "your-secret-api-key"
```

Restart VSCode after setting this environment variable, as environment variables are loaded at startup.

**Linux and macOS:**

On Linux and macOS, you typically set environment variables in the shell or in your shell configuration file (like `.bashrc` or `.zshrc`).

```
export OPENAI_API_KEY="your_api_key_here"
```

After adding, reload the configuration:

```
source ~/.bashrc  # For bash users
source ~/.zshrc   # For zsh users
```
