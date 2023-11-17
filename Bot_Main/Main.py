import discord
from discord.ext import commands





bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
bot.load_extension("VerifyDeny_Cog")
bot.run("TOKEN")



