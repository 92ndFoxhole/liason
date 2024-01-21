import discord
from discord.ext import commands
import sqlite3
import os
import importlib.util
import json
import prettytable
from prettytable import PrettyTable, from_db_cursor, MSWORD_FRIENDLY, HEADER, FRAME, ALL
from colorama import Fore, Back, Style
import pkgutil
import importlib

def main():
    print('Liason Bot v0.0.1 \n A Discord Bot written for the 92nd Regiment for the game Foxhole. \n Please see out Github for more information @ https://github.com/92ndFoxhole/liason. \n Licensed under MIT, see license.txt for more information. \n')
    print('Modules Loaded:')
    from cogs.stockpilecodes import CogInformation

if __name__ == '__main__':
    main()

# IMPORT BOT TOKEN FROM token.json
try:
    token_import = open('token.json')
    load_token = json.load(token_import)
    bot_token = load_token["bot_token"]
    if len(bot_token) < 1:
        raise Exception
except:
    print(Fore.RED + "ERROR: Missing bot token from token.json." + Fore.WHITE + "Please copy your bot token and paste it into token.json.")

try: 
        constants_import = open('constants.json')
        constants = json.load(constants_import)
        guildId = constants["guild"]
        #print(load_constants)
        if len(constants) < 1:
            raise Exception
except:
        print(Fore.RED + "ERROR: Missing constants from constants.json." + Fore.WHITE + "Please copy the constants from constants.json.example and paste them into constants.json.")

class SQLiteConnection:
    def __init__(self, db_name):
        self.con = sqlite3.connect(db_name)
        self.cur = self.con.cursor()

    def execute(self, query, params=()):
        self.cur.execute(query, params)

    def commit(self):
        self.con.commit()

    def close(self):
        self.con.close()


intents = discord.Intents.all()

bot = discord.Bot(intents=intents)

# LIST OF COGS
bot.load_extension('cogs.stockpilecodes')
#bot.load_extension('cogs.test')


# SOME DEBUG SLASH COMMANDS
@bot.slash_command(guild_ids=[guildId],description="Reload currently designated cog")
async def reload(ctx):
     # Reloads the file, thus updating the Cog class.
    bot.reload_extension('cogs.stockpilecodes')
    await ctx.respond("Reloaded!", ephemeral=True)

@bot.slash_command(guild_ids=['1163561993530253375'],description="Sends the bot's latency.") # this decorator makes a slash command
async def ping(ctx): # a slash command will be created with the name "ping"
    await ctx.respond(f"Pong! Latency is {bot.latency}")

@bot.slash_command(guild_ids=['1163561993530253375'],description="Says hello") # this decorator makes a slash command
async def hello(ctx): # a slash command will be created with the name "ping"
    await ctx.respond("Hello!")    

@bot.slash_command(guild_ids=['1163561993530253375'],description="Says goodbye") # this decorator makes a slash command
async def goodbye(ctx): # a slash command will be created with the name "ping"
    await ctx.respond("goodbye!")

bot.run(bot_token)