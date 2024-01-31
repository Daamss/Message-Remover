import discord
import asyncio

intents = discord.Intents.default()
intents.typing = False
intents.presences = False

client = discord.Client(intents=intents)

token = ""  # Insert your discord token
prefix = ""  # Select a prefix for the command.
command = ""  # Set the command to whatever you want
discord_invite_link = "https://discord.gg/D5ghz8C4gq"  # Renamed variable

# Rate limit for message deletion (seconds per message)
message_deletion_rate_limit = 0.6

class MessageDeletionQueue:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, message):
        await self.queue.put(message)

    async def dequeue(self):
        return await self.queue.get()

    async def process_queue(self):
        while True:
            message = await self.dequeue()
            await self.delete_message(message)
            await asyncio.sleep(message_deletion_rate_limit)

    async def delete_message(self, message):
        try:
            await message.delete()
        except discord.Forbidden:
            pass

message_deletion_queue = MessageDeletionQueue()

@client.event
async def on_ready():
    print("\n\n\nMessage-Remover v1.3 is ready")
    print("You have set the command to: " + prefix + command)
    print("\n\n\nJoin the discord if you have any questions")
    print(discord_invite_link)  # Fixed variable name
    asyncio.create_task(message_deletion_queue.process_queue())

@client.event
async def on_message(message):
    if message.author == client.user and message.content.startswith(prefix + command):
        if isinstance(message.channel, discord.DMChannel) or isinstance(message.channel, discord.TextChannel):
            async for msg in message.channel.history(limit=None):
                if msg.author == client.user and not msg.type == discord.MessageType.pins_add:
                    await message_deletion_queue.enqueue(msg)

client.run(token, bot=False)
