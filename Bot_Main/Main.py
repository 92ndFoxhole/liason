
import discord
from discord.ext import commands


description = """The 92nd regiment bot"""

intents = discord.Intents.default()
intents.members = True


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description=description,
    intents=intents,
)
    

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")
    
    
@bot.command(description='Deny members to the 92nd regiment takes in their user id, or their name, or just ping them also has an optional field for reason which will appear in audit logs default reason is "verified" example: !verify casualpigeon "Hes the dev writing this"')
async def deny(ctx, member: discord.Member, giveReason = "Denied"):
    """This system of calling all the channels/roles  by id in this command is terrible but is simply for testing purposes I will fix this tommorow if I am free"""
    guild = bot.get_guild(1163561993530253375)      
    recruit = guild.get_role(1174547968796393494)
    verifcationChannel = guild.get_channel(1174552689280045106)
    await member.remove_roles(recruit, reason=giveReason)
    await verifcationChannel.send(member.display_name + " Has been denied reason: " + giveReason)
        

@bot.command(description='Verify members to the 92nd regiment takes in their user id, or their name, or just ping them also has an optional field for reason which will appear in audit logs default reason is "verified" example: !verify casualpigeon "Hes the dev writing this"')
async def verify(ctx, member: discord.Member, giveReason = "Verified"):
    """This system of calling all the channels/roles  by id in this command is terrible but is simply for testing purposes I will fix this tommorow if I am free"""
    guild = bot.get_guild(1163561993530253375)      
    cadet_role = guild.get_role(1174541862204342282)
    member_role = guild.get_role(1174535263578497125)
    recruit = guild.get_role(1174547968796393494)
    discussion = guild.get_channel(1174553795699671151)
    verifcationChannel = guild.get_channel(1174552689280045106)
    await member.add_roles(member_role, cadet_role, reason=giveReason)
    await member.remove_roles(recruit, reason=giveReason)
    await discussion.send(member.mention + "welcome to the 92nd, check out #role-assignment and ask if you have any questions.")
    await verifcationChannel.send(member.display_name + " Has been verified reason: " + giveReason)
    
bot.run("TOKEN")



