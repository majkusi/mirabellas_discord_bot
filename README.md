# mirabellas_discord_bot

![Python](https://img.shields.io/badge/Python_3.14-3776AB?logo=python&logoColor=white)
![discord.py](https://img.shields.io/badge/discord.py-5865F2?logo=discord&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini_API-8E75B2?logo=googlegemini&logoColor=white)
![Last commit](https://img.shields.io/github/last-commit/majkusi/mirabellas_discord_bot)
![License](https://img.shields.io/github/license/majkusi/mirabellas_discord_bot)

Discord bot for Mirabelki, a World of Warcraft guild. It translates Polish chat messages into Silesian and summarises long conversations.

Built as an application to deploy on the [homelab](https://github.com/majkusi/homelab) Proxmox server, and to practise Python, containers and CI along the way.

## Features

- **`!slunski <text>`** translates Polish into Silesian, spelled with the Polish alphabet the way the guild writes it in chat
- **`!tldr [count]`** summarises the last `count` messages in the channel (default 200, max 500), skipping bot messages
- **Planned:** slash commands instead of text commands

## Stack

- **Language:** Python 3.14, `src` layout, packaged with `pyproject.toml`
- **Discord:** [discord.py](https://discordpy.readthedocs.io/)
- **LLM:** Google Gemini through the [`google-genai`](https://googleapis.github.io/python-genai/) SDK, async, with a request timeout and a single retry
- **Configuration:** environment variables, loaded from `.env` in development
- **Planned:** Ruff, pytest, Docker image on GHCR, deployment with Ansible

## Repository layout

```
src/guild_bot/
  __main__.py      entry point (python -m guild_bot)
  bot.py           Discord client and commands
  config.py        reads and validates settings from the environment
  llm/
    client.py      Gemini client
    prompts.py     system prompts and few-shot examples
```

## Setup

Requirements: Python 3.14, a Discord application with a bot user, and a Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

In the [Discord Developer Portal](https://discord.com/developers/applications):

1. Enable **Message Content Intent** under Bot → Privileged Gateway Intents.
2. Generate an invite under OAuth2 → URL Generator with the `bot` and `applications.commands` scopes, Guild Install, and only these permissions: View Channels, Send Messages, Read Message History.

Install the project into a virtual environment:

```sh
python3.14 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

Create `.env` from the template and fill it in:

```sh
cp .env.example .env
```

## Configuration

| Variable | Description |
| --- | --- |
| `DISCORD_TOKEN` | Bot token from the Developer Portal |
| `DISCORD_GUILD_ID` | ID of the server used for development |
| `LLM_API_KEY` | Gemini API key |
| `LLM_MODEL` | Gemini model name, e.g. `gemini-flash-latest` ([available models](https://ai.google.dev/gemini-api/docs/models)) |

## Usage

```sh
python -m guild_bot
```

Then, in a channel the bot can see:

```
!slunski Idziemy dziś na raid o 20, kto będzie?
!tldr 100
```

## Roadmap

Planned work is tracked in the [homelab issues](https://github.com/majkusi/homelab/issues?q=is%3Aissue+label%3Adiscord-bot) under the `discord-bot` label and on the [project board](https://github.com/users/majkusi/projects/6).

## Privacy

Text passed to `!slunski` is sent to the Gemini API, and `!tldr` sends recent channel history, including authors' display names. On the free tier, Google may use them to improve its models (see the [Gemini API terms](https://ai.google.dev/gemini-api/terms)). Do not use the bot on content the guild would not want to share.

## Security

Tokens and API keys live only in `.env`, which is git-ignored, and never in the code or the repository. The bot is a private application and requests only the permissions it needs.

## License

[MIT](LICENSE)
