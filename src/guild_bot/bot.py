import discord
from discord.ext import commands
from dotenv import load_dotenv
from .llm.client import LlmClient
from .config import load_config
import logging

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

def main():
    logging.getLogger("google_genai").setLevel(logging.DEBUG)
    logging.getLogger("httpx").setLevel(logging.INFO)
    config = load_config()
    bot.llm = LlmClient(
        llm_model=config.llm_model,
        llm_api_key=config.llm_api_key
    )    
    
    bot.run(config.discord_token)

@bot.command(name="slunski")
async def translate_to_silesian(ctx, *, text: str):
    async with ctx.typing():
        result = await bot.llm.llm_translate_to_silesian(text)
    await ctx.send(result)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
