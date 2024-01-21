import discord
from discord.ext import commands

class BotCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    def idPusher(self):
        self.guild = self.bot.get_guild(1163561993530253375)  
        self.recruit = self.guild.get_role(1174547968796393494)
        self.activityChannel = self.guild.get_channel(1175517710587809792) 
        self.inactiveRole = self.guild.get_role(1175517567641727046)
        self.message_id = None
    
    
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.idPusher()

    
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
            await payload.member.remove_roles(self.inactiveRole)
            
            
        except discord.HTTPException:
            
            raise "Failed to updated users roles"
   
   
    @commands.is_owner()
    @commands.command()
    async def newWar(self, ctx):
        #increase inactive wars by 1
        message = await self.activityChannel.send("Activity message, react to be marked active for this war.")
        self.message_id = message.id
        print()
        for member in self.guild.members:
            await member.add_roles(self.inactiveRole) #Should work but for some reason guild.members only returns the bot. WIP
        
        
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def active(self, ctx, member: discord.Member, giveReason = "No reason given"):
        pass
        
        
            
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def inactive(self, ctx, member: discord.Member, giveReason = "No reason given"):
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        await member.add_roles(self.recruit, reason=giveReason)
        
    
    
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
    
                

async def setup(bot):
    await bot.add_cog(BotCommands(bot))