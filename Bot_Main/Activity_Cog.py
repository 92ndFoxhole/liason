import discord, json
from discord.ext import commands

class BotCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None
    
    
 

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if self.message_id == None:
            # Reaction message not sent yet
            return
        
        
        #make sure it is the react message
        if payload.message_id != self.message_id:
            return

        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            # Check if is in guild
            return

        try:
            # Reset active wars on database for member
            with open("constants.json", "r") as constants:
                data = json.load(constants)
                inactive_Role = data["inactive_Role"]
                await payload.member.remove_roles(discord.Object(id=inactive_Role))
            
            
        except discord.HTTPException:
            
            raise "Failed to updated users roles"
   
   
    @commands.is_owner()
    @commands.command()
    async def newWar(self, ctx):
        #increase inactive wars by 1
        with open("constants.json", "r") as constants:
            data = json.load(constants)
            inactive_Role = data["inactive_Role"]
            activity_Channel = data["activity_Channel"]
            activity_Channel = await self.bot.fetch_channel(activity_Channel)
            message = await activity_Channel.send("Activity message, react to be marked active for this war.")
            self.message_id = message.id
            for member in ctx.guild.members:
                await member.add_roles(discord.Object(id=inactive_Role)) 
        
        
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def active(self, ctx, member: discord.Member, giveReason = "No reason given"):
        with open("constants.json", "r") as constants:
            data = json.load(constants)
            inactive_Role = data["inactive_Role"]
            await member.remove_roles(discord.Object(id=inactive_Role))
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def active(self, ctx, member: discord.Member, giveReason = "No reason given"):
        with open("constants.json", "r") as constants:
            data = json.load(constants)
            inactive_Role = data["inactive_Role"]
            await member.add_roles(discord.Object(id=inactive_Role))
        
            
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def derole(self, ctx, member: discord.Member, giveReason = "No reason given"):
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        
        
    
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def leaveOfAbsence(self, ctx, member: discord.Member, giveReason = "No reason given"):
        pass 
    
    @commands.command()
    @commands.is_owner()
    async def massDemotion(self, ctx, inactiveWars):
        
        if inactiveWars != int:
            raise TypeError("Inactive wars is an integer")
        if inactiveWars == 0:
            ctx.send("Would mark everyone as inactive.")
    
                

def setup(bot):
    bot.add_cog(BotCommands(bot))