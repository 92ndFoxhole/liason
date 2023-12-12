
from discord.ext import commands

class BotCommands(commands.Cog):
    #initialize bot should pass in bot.
    def __init__(self, bot):
        self.bot = bot
    #ran on cog bot setup
    @commands.Cog.listener()
    async def on_ready(self):
        pass
    #example command takes in self from class then ctx contains context of command including guild, member, channel and more.
    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Hello")
#Function to add cog takes in bot
def setup(bot):
    bot.add_cog(BotCommands(bot))