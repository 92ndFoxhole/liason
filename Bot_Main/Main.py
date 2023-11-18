import discord
from discord.ext import commands






bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    intents=intents,
)

bot.load_extension("VerifyDeny_Cog")
bot.load_extension("Activity_Cog")

bot.run("TOKEN")