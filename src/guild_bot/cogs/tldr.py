from discord.ext import commands
from google.genai import errors

MAX_TLDR_MESSAGES = 500


class Tldr(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="tldr")
    async def tldr(self, ctx, limit: int = 200):
        limit = min(limit, MAX_TLDR_MESSAGES)
        async with ctx.typing():
            messages = [
                msg
                async for msg in ctx.channel.history(limit=limit, before=ctx.message)
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
                result = await self.bot.llm.llm_create_tldr(chat_log)
            except errors.APIError:
                await ctx.send("Gemini teraz nie odpowiada, spróbuj za chwilę.")
                return

            await ctx.send(result)
