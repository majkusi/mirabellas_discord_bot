import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv
from google.genai import errors

from .config import load_config
from .llm.client import LlmClient

MAX_TLDR_MESSAGES = 500

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


def main():
    logging.getLogger("google_genai").setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.INFO)
    config = load_config()
    bot.llm = LlmClient(llm_model=config.llm_model, llm_api_key=config.llm_api_key)

    bot.run(config.discord_token)


@bot.command(name="slunski")
async def translate_to_silesian(ctx, *, text: str):
    async with ctx.typing():
        result = await bot.llm.llm_translate_to_silesian(text)
    await ctx.send(result)


@bot.command(name="tldr")
async def tldr(ctx, limit: int = 200):
    limit = min(limit, MAX_TLDR_MESSAGES)

    async with ctx.typing():
        messages = [
            msg async for msg in ctx.channel.history(limit=limit, before=ctx.message)
        ]
        chat_log = [
            (msg.author.display_name, msg.content)
            for msg in reversed(messages)
            if not msg.author.bot and msg.content
        ]

        if not chat_log:
            await ctx.send("Nie ma czego streszczać.")
            return

        try:
            result = await bot.llm.llm_create_tldr(chat_log)
        except errors.APIError:
            await ctx.send("Gemini teraz nie odpowiada, spróbuj za chwilę.")
            return

    await ctx.send(result)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
