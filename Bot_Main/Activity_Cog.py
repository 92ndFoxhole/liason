import discord
from discord.ext import commands


class BotCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    def idPusher(self):
        self.guild = self.bot.get_guild(1163561993530253375)  
        self.recruit = self.guild.get_role(1174547968796393494)

    
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.idPusher()
        
        
    @commands.command()
    async def active(self, ctx, member: discord.Member, giveReason = "No reason given"):
        pass
        
        
            

    @commands.command()
    async def inactive(self, ctx, member: discord.Member, giveReason = "No reason given"):
        for i in member.roles:
            try:
                await member.remove_roles(i)
            except:
                print(f"Can't remove the role {i}")
        await member.add_roles(self.recruit, reason=giveReason)
        
    
    
    
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
