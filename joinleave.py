class join():
    async def on_member_join(member):
        print(f'{member.mention} has joined the server')
        channel = client.get_channel(1163561994574643295)
        await channel.send(f'{member.mention} has joined!')


async def setup(bot):
    await bot.add_cog(BotCommands(bot))