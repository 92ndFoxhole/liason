import discord

TOKEN = "Your token"



def main():
    
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)
    
    @client.event

    async def on_ready():
        
        print(f'We have logged in as {client.user}')

        
    client.run(TOKEN)







if __name__ == "__main__":
    main()
