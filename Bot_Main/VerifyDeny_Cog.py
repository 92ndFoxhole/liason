import discord, json
from discord.ext import commands


class BotCommands(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        
    
        
    @commands.has_permissions(manage_roles=True)
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        print("------")
        
    @commands.has_permissions(manage_roles=True)    
    @commands.command()
    async def deny(self, ctx, member: discord.Member, giveReason = "Denied"):
        with open("constants.json", "r") as constants:
            data = json.load(constants)
            recruit_Role = data["recruit_Role"]
            await member.remove_roles(discord.Object(id=recruit_Role), reason=giveReason)
            
            
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def verify(self, ctx, member: discord.Member, giveReason = "Verified"):
        
        with open("constants.json", "r") as constants:
            data = json.load(constants)
            
            recruit_Role = data["recruit_Role"]
            cadet_Role = data["cadet_Role"]
            member_Role = data["member_Role"]
            discussion_Channel = data["discussion_Channel"]
            roleAssignment_Channel = data["roleAssignment_Channel"]
            discussion_Channel = await self.bot.fetch_channel(discussion_Channel)
            roleAssignment_Channel = await self.bot.fetch_channel(roleAssignment_Channel)
            await member.add_roles(discord.Object(id= member_Role), discord.Object(id=cadet_Role), reason=giveReason)
            await member.remove_roles(discord.Object(id= recruit_Role), reason=giveReason)
            await discussion_Channel.send(member.mention + " Welcome to the 92nd, check out " + roleAssignment_Channel.mention + " and ask if you have any questions.")            

def setup(bot):
    bot.add_cog(BotCommands(bot))