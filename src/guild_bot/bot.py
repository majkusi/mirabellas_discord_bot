import logging

import discord
from discord.ext import commands
from dotenv import load_dotenv

from .cogs.silesian import Silesian
from .cogs.tldr import Tldr
from .config import load_config
from .llm.client import LlmClient

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True


class MirabellasBot(commands.Bot):
    async def setup_hook(self):
        await self.add_cog(Silesian(self))
        await self.add_cog(Tldr(self))


bot = MirabellasBot(command_prefix="!", intents=intents)


def main():
    logging.getLogger("google_genai").setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.INFO)
    config = load_config()
    bot.llm = LlmClient(llm_model=config.llm_model, llm_api_key=config.llm_api_key)
    bot.run(config.discord_token)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
