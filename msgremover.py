import discord
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

token = "" # Insert your discord token
prefix ="" # Select a prefix for the command.
command = "" # Set the command to whatever you want

@client.event
async def on_ready():
    print("\n\n\nMessage-Remover v1.3 is ready")
    print("You have set the command to: " + prefix + command)
    print("\n\n\nJoin the discord if you have any questions")
    print(discord)


@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith(prefix + command):
        if isinstance(message.channel, discord.DMChannel):
            async for msg in message.channel.history(limit=None):
                if msg.author == client.user and not msg.type == discord.MessageType.pins_add:
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    await asyncio.sleep(0.6)  # Change how fast messages should be deleted for DMs

        elif isinstance(message.channel, discord.TextChannel):
            async for msg in message.channel.history(limit=None):
                if msg.author == client.user and not msg.type == discord.MessageType.pins_add:
                    try:
                        await msg.delete()
                    except discord.Forbidden:
                        pass
                    await asyncio.sleep(0.6)  # Change how fast messages should be deleted for servers


discord = "https://discord.gg/Nv57hscasX"

client.run(token, bot=False)