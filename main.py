import discord
from discord import Activity, ActivityType
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(activity=Activity(type=ActivityType.playing, name="in the trash"))
    global channel_time_dict
    global channel_message_dict
    channel_message_dict = {}
    channel_time_dict = {}
    
@client.event
async def on_guild_join(guild):
    try:
        global role
        role = await guild.create_role(name = "Trash Panda", permissions=discord.Permissions.none())
        print(f'Bot has crated role: {role.id}')
    except:
        print(Exception)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.guild is None:
        return

    if not any(role.name == "Trash Panda" for role in message.author.roles):
        return

    if client.user.mentioned_in(message):
        message_args = message.content.split()
        if message_args[1] == "start":
            await message.delete()
            if message_args[2] == "messages":
                channel_id = message.channel.id
                channel_message_dict[channel_id] = message_args[3]
                await message.channel.send(f'Auto Deletion will begin after {message_args[3]} messages.')

            elif int(message_args[2]):
                channel_id = message.channel.id
                if message_args[3] == "h":
                    time = int(message_args[2]) * 60 * 60
                elif message_args[3] == "m":
                    time = int(message_args[2]) * 60
                else:
                    pass
                channel_time_dict[channel_id] = time
                await message.channel.send(f'Auto Deletion will begin after {message_args[2]}{message_args[3]}.')
                print(channel_time_dict)
        
        elif message_args[1] == "stop":
            await message.channel.send("Stopping Auto Deletion!")
            try:
                channel_message_dict.pop(message.channel.id)
            except:
                channel_time_dict.pop(message.channel.id)

    if client.user.mentioned_in(message):
        return
    
    if message.channel.id in channel_time_dict:
        #print("Time has been started")
        await asyncio.sleep(channel_time_dict[message.channel.id])
        #print("Time has been finished")
        await message.delete()

    
    if message.channel.id in channel_message_dict:
        #print(f'{message.channel.id} exists in dictionary with value {channel_message_dict[message.channel.id]}')
        messages = []
        number_of_messages = int(channel_message_dict[message.channel.id])
        async for message in message.channel.history(limit=None):
            if message.author == client.user:
                continue
            messages.append(message)
        if len(messages) > number_of_messages:
            messages_to_delete = messages[number_of_messages:]
            await message.channel.delete_messages(messages_to_delete)


client.run(os.getenv("DISCORD_TOKEN"))

#@Deletor start messages 100 <- Deletes the oldest message so that only 100 messages are in the chat at once
#@Deletor start 24 h <- Deletes the message above after 24hrs
#@Deletor stop <- Stops the deletion process