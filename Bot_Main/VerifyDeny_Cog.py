import discord
from discord.ext import commands


class BotCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    def idPusher(self):
        self.guild = self.bot.get_guild(1163561993530253375)      
        self.cadet_role = self.guild.get_role(1174541862204342282)
        self.member_role = self.guild.get_role(1174535263578497125)
        self.recruit = self.guild.get_role(1174547968796393494)
        self.discussion = self.guild.get_channel(1174553795699671151)
        self.verifcationChannel = self.guild.get_channel(1174552689280045106)
        self.roleAssignment = self.guild.get_channel(1174559644115546232)
        
    @commands.has_permissions(manage_roles=True)
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------")
        self.idPusher() #Note here that idpusher is not called in init because to use get_role you have to connect to discord server first.
        
    @commands.has_permissions(manage_roles=True)    
    @commands.command()
    async def deny(self, ctx, member: discord.Member, giveReason = "Denied"):
        
        
        await member.remove_roles(self.recruit, reason=giveReason)
        await self.verifcationChannel.send(member.display_name + " Has been denied reason: " + giveReason)
            
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def verify(self, ctx, member: discord.Member, giveReason = "Verified"):
        
        
        await member.add_roles(self.member_role, self.cadet_role, reason=giveReason)
        await member.remove_roles(self.recruit, reason=giveReason)
        await self.discussion.send(member.mention + " Welcome to the 92nd, check out " + self.roleAssignment.mention + " and ask if you have any questions.")
        await self.verifcationChannel.send(member.display_name + " Has been verified reason: " + giveReason)

def setup(bot):
    bot.add_cog(BotCommands(bot))