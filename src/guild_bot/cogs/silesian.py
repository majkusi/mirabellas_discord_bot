from discord.ext import commands


class Silesian(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="slunski")
    async def translate_to_silesian(self, ctx, *, text: str):
        async with ctx.typing():
            result = await self.bot.llm.llm_translate_to_silesian(text)
        await ctx.send(result)
