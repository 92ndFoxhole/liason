# WARNING
# BEFORE GOING AND TINKERING WITH THIS, PLEASE NOTE THAT THIS COG IS A ROUGH IMPLEMENTATION.
#
# <!> EDIT THIS AT YOUR OWN RISK <!>

import discord
from discord.ext import commands
from datetime import date, datetime, timezone
import sqlite3
import os
import prettytable
from prettytable import PrettyTable, from_db_cursor, MSWORD_FRIENDLY, HEADER, FRAME, ALL
from uuid import uuid4
from Main import SQLiteConnection
from colorama import Fore, Back, Style
import json

class CogInformation():
        Name = "stockpilecodes.py"
        Version = "0.0.5"
        Author = "KingdomKeeper"
        print(f"@ {Name} - v{Version} by {Author}")

# Stockpile Commands
# Stockpile read command

try: 
        constants_import = open('constants.json')
        constants = json.load(constants_import)
        guildId = constants["guild"]
        stockpileChannel = constants["stockpileChannel_id"]
        stockpileMessage = constants["stockpileMessage_id"]
        supportChannel = constants["supportChannel_id"]
        #print(load_constants)
        if len(constants) < 1:
            raise Exception
except:
        print(Fore.RED + "ERROR: Missing constants from constants.json." + Fore.WHITE + "Please copy the constants from constants.json.example and paste them into constants.json.")

class StockpileCodes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #SQL Connection
        self.db = SQLiteConnection("sql/regiment")
    bot = discord.Bot()

    @bot.slash_command(guild_ids=[guildId],description="Says hellostock") # this decorator makes a slash command
    async def hellostock(self, ctx): # a slash command will be created with the name "ping"
        await ctx.respond("Hello from the Stockpile Code Cog!") 

    @bot.slash_command(guild_ids=[guildId],description="Prints a list of public stock pile codes")
    async def stockpiles(self, ctx):
        guildName = ctx.guild.name
        cwd = os.getcwd()
        self.res = self.db.execute("SELECT name, region, code FROM stockpiles WHERE isPrivate IS NULL")
        slp = from_db_cursor(self.db.cur)
        slp.hrules = HEADER
        slp.align = "c"
        slp.border = True

        def get_notes():
            self.db.execute(f"SELECT name, notes FROM stockpiles WHERE isPrivate IS NULL")
            rows = self.db.cur.fetchall()
            return "\n".join([f"{row[0]} - {row[1]}" for row in rows])
        await ctx.respond(f"# Public Stockpiles for {guildName} \n```\n{slp}\n``` \n\n __Please see the stockpile notes below:__ \n{get_notes()}", ephemeral=True)


    @bot.slash_command(guild_ids=[guildId],description="Creates initial stockpile message, should only need to be run once.")
    async def stockpilesetup(self, ctx):
        channel = self.bot.get_channel(stockpileChannel)
        cwd = os.getcwd()
        self.db = SQLiteConnection("sql/regiment")
        self.db.execute("SELECT name, region, code FROM stockpiles WHERE isPrivate IS NULL")
        slp = from_db_cursor(self.db.cur)
        slp.hrules = HEADER
        slp.align = "c"
        slp.border = True

        def get_notes():
            self.db.execute(f"SELECT name, notes FROM stockpiles WHERE isPrivate IS NULL")
            rows = self.db.cur.fetchall()
            return "\n".join([f"{row[0]} - {row[1]}" for row in rows])
        await ctx.respond(f"Please check <#{stockpileChannel}> for the current stockpile codes.", ephemeral=True),
        await channel.send(f"# Stockpile Codes\n Included in the table below are the current stockpiles for the active war. For more information regarding each stockpile please use the `/stockpile notes` command. If you encounter any errors or bugs, please report these in our <#{supportChannel}> channel. Thank you! ```\n{slp}\n``` __Please see stockpile notes below:__ \n{get_notes()}")
        #await channel.send(cwd)


    stockpile = discord.SlashCommandGroup(name="stockpile", description="Manage Stockpiles", guild_ids=[guildId])
    @stockpile.command(description="Add a new stockpile")
    @commands.has_role("92nd Regiment")
    async def new(self, ctx: discord.ApplicationContext, stockpiletype: discord.Option(str, choices=['public', 'private'], required = False)):
        PublicModal = StockpileModal(self.bot, 'public', title="Submit A New Stockpile Code")
        PrivateModal = StockpileModal(self.bot, 'private', title="Submit A New Private Stockpile Code")
        if stockpiletype == 'public':
            await ctx.send_modal(PublicModal)

        if stockpiletype == 'private':
            await ctx.send_modal(PrivateModal)


    @stockpile.command(description="Delete a stockpile")
    async def delete(self, ctx: discord.ApplicationContext, name: discord.Option(str, required = True)):
        stockpileName = name
        channel = self.bot.get_channel(stockpileChannel)
        message = await channel.fetch_message(stockpileMessage)
        cwd = os.getcwd()
        self.db.execute(f"SELECT name, userId, isPrivate FROM stockpiles WHERE name IS '{stockpileName}'")
        rows = self.db.cur.fetchone()
        print(rows)
        if stockpileName == rows[0] and ctx.author.id == rows[1] or ctx.author.guild_permissions.manage_messages:
            self.db.execute(f"DELETE FROM stockpiles WHERE name IS '{stockpileName}'")
            self.db.commit()
            await ctx.send_response (f"Stockpile {stockpileName} deleted.", ephemeral=True)
            self.db.execute("SELECT name, region, code FROM stockpiles WHERE isPrivate IS NULL")
            slp = from_db_cursor(self.db.cur)
            slp.hrules = HEADER
            slp.align = "c"
            slp.border = True
            def get_notes():
                self.db.execute(f"SELECT name, notes FROM stockpiles WHERE isPrivate IS NULL")
                rows = self.db.cur.fetchall()
                return "\n".join([f"{row[0]} - {row[1]}" for row in rows])
            await message.edit(content=f"# Stockpile Codes\n Included in the table below are the current stockpiles for the active war. If you encounter any errors or bugs, please report these in our <#{supportChannel}> channel. Thank you! ```\n{slp}\n``` __Please see stockpile notes below:__ \n{get_notes()}")

        else:
            await ctx.send_response (f"Sorry, you do not have permission to delete this stockpile.", ephemeral=True)      


    private = stockpile.create_subgroup (name="private", description="Manage Private Stockpiles", guild_ids=[guildId])
    @private.command(guild_ids=[guildId],description="Prints a list of private stock pile codes")
    async def view(self, ctx: discord.ApplicationContext):
        userID = ctx.author.id
        user = await self.bot.fetch_user(userID)
        authorName = user.name
        cwd = os.getcwd()
        self.res = self.db.execute(f"SELECT name, region, code FROM stockpiles WHERE isPrivate IS 1 AND userId IS ?", (userID,))
        slp = from_db_cursor(self.db.cur)
        slp.hrules = HEADER
        slp.align = "c"
        slp.border = True

        def get_notes():
            self.db.execute(f"SELECT name, notes FROM stockpiles WHERE isPrivate IS 1 AND userID IS {userID}")
            rows = self.db.cur.fetchall()
            return "\n".join([f"{row[0]} - {row[1]}" for row in rows])
        await ctx.respond(f"# Private Stockpiles for {authorName} \n```\n{slp}\n``` \n\n __Please see the stockpile notes below:__ \n {get_notes()}", ephemeral=True)


    officer = stockpile.create_subgroup (name="officer", description="Manage Officer Stockpiles", guild_ids=[guildId])
    @officer.command(guild_ids=[guildId],description="Prints a list of officer stock pile codes")
    @commands.has_permissions(manage_messages=True)
    async def view(self, ctx: discord.ApplicationContext):
        try:
            userID = ctx.author.id
            guildName = ctx.guild.name
            user = await self.bot.fetch_user(userID)
            authorName = user.name
            cwd = os.getcwd()
            self.res = self.db.execute(f"SELECT name, region, code FROM stockpiles WHERE isPrivate IS 2")
            slp = from_db_cursor(self.db.cur)
            slp.hrules = HEADER
            slp.align = "c"
            slp.border = True

            def get_notes():
                self.db.execute(f"SELECT name, notes FROM stockpiles WHERE isPrivate IS 2")
                rows = self.db.cur.fetchall()
                return "\n".join([f"{row[0]} - {row[1]}" for row in rows])
            await ctx.respond(f"# Officer Stockpiles for {guildName} \n```\n{slp}\n``` \n\n __Please see the stockpile notes below:__ \n {get_notes()}", ephemeral=True)
        except discord.Forbidden:
            await ctx.respond(f"Sorry, you do not have permission to view officer stockpiles.", ephemeral=True)
# STAFF COMMANDS
    @officer.command(description="Add a new officer stockpile")
    @commands.has_permissions(manage_messages=True)
    async def new(self, ctx: discord.ApplicationContext):
        channel = self.bot.get_channel(stockpileChannel)
        message = await channel.fetch_message(stockpileMessage)
        OfficerModal = StockpileModal(self.bot, 'officer', title="Submit A New Officer Stockpile Code")    
        await ctx.send_modal(OfficerModal)




# STOCKPILE MODAL
class StockpileModal(discord.ui.Modal):

    def __init__(self, bot, modal_type, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot

        #SQL Connection
        self.db = SQLiteConnection("sql/regiment")
        self.modal_type = modal_type

        self.add_item(discord.ui.InputText(label="Stockpile Name:", max_length=8))
        self.add_item(discord.ui.InputText(label="Stockpile Region: (ex: Deadlands)", max_length=9))
        self.add_item(discord.ui.InputText(label="Stockpile Code:", max_length=6))
        self.add_item(discord.ui.InputText(label="Stockpile Notes:", style=discord.InputTextStyle.long))

    async def callback(self, interaction: discord.Interaction):
        
        form1 = self.children[0].value
        form2 = self.children[1].value
        form3 = self.children[2].value
        form4 = self.children[3].value
        getStockpileDate = datetime.now(timezone.utc)
        stockpileDate = getStockpileDate.date()
        user = interaction.user.id
        uuid = uuid4()

        if self.modal_type == 'public':
            #print(uuid4(), form1, form2, form3, form4, user)
            self.db.execute("INSERT INTO stockpiles (date,name,region,code,notes,userId) VALUES (?, ?, ?, ?, ?, ?)", (stockpileDate, form1, form2, form3, form4, user))
        elif self.modal_type == 'private':
            print(f"Private Stockpile = {form1},{form2},{form3},{form4}")
            self.db.execute(f"INSERT INTO stockpiles (date,name,region,code,notes,isPrivate,userId) VALUES (?, ?, ?, ?, ?, ?, ?)", (stockpileDate, form1, form2, form3, form4, '1', user))
        elif self.modal_type == 'officer':
            print(f"Officer Stockpile = {form1},{form2},{form3},{form4}")
            self.db.execute(f"INSERT INTO stockpiles (date,name,region,code,notes,isPrivate,userId) VALUES (?, ?, ?, ?, ?, ?, ?)", (stockpileDate, form1, form2, form3, form4, '2', user))

        self.db.commit()

        self.db.execute("SELECT name, region, code FROM stockpiles WHERE isPrivate IS NULL")
        StockpileCodes.slp = from_db_cursor(self.db.cur)
        StockpileCodes.slp.hrules = HEADER
        StockpileCodes.slp.align = "c"
        StockpileCodes.slp.border = True
        
        channel = self.bot.get_channel(stockpileChannel)
        message = await channel.fetch_message(stockpileMessage)
        def get_notes():
            self.db.execute(f"SELECT name, notes FROM stockpiles WHERE isPrivate IS NULL")
            rows = self.db.cur.fetchall()
            return "\n".join([f"{row[0]} - {row[1]}" for row in rows])
        await interaction.response.send_message(f"{form1} stockpile has been submitted. Thank you.", ephemeral=True)
        await message.edit(content=f"# Stockpile Codes\n Included in the table below are the current stockpiles for the active war. If you encounter any errors or bugs, please report these in our <#{supportChannel}> channel. Thank you! ```\n{StockpileCodes.slp}\n``` __Please see stockpile notes below:__ \n{get_notes()}")


        

def setup(bot):
    bot.add_cog(StockpileCodes(bot))