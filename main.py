import asyncio
from pytube import YouTube
from discord.ext import commands
import random
import os
import discord.opus

# Load the Opus library for audio encoding/decoding
discord.opus.load_opus('libopus.so.0')

# Get the bot token from the environment variable
bot_token = os.environ.get('DISCORD_BOT_TOKEN')
if not bot_token:
    print('Error: no bot token specified in DISCORD_BOT_TOKEN environment variable')
    exit(1)

# Initialize the Discord client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# List of YouTube video URLs to play
video_urls = [
    'https://www.youtube.com/watch?v=jumQ76GEYLQ', #
    'https://www.youtube.com/watch?v=Cz5q05Hl5gs', #
    'https://www.youtube.com/watch?v=Uift1RYej0w', #
    'https://www.youtube.com/watch?v=qT_R_D3tCes', #
    'https://www.youtube.com/watch?v=6IUqSY783_8', # собака писала
    'https://www.youtube.com/watch?v=vkPXG11Fj_U', # шипупи
    'https://www.youtube.com/watch?v=G6pqAN8ALC8', # пасха
    'https://www.youtube.com/watch?v=azd1ZnHNt9g', # радужный гимн
]

async def play_song(voice_client):
    # Choose a random video URL from the list
    url = random.choice(video_urls)

    # Download the video as an audio stream
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    if not stream:
        print(f'Error: could not download audio stream from {url}')
        return

    # Save the audio stream to a temporary file
    filename = f'{yt.video_id}.mp3'
    stream.download(filename=filename)

    # Send the audio stream to the voice channel
    source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filename))
    voice_client.play(source, after=lambda e: print(f'Finished playing {filename}'))
    print(f'Playing {filename}')

    # Wait for the song to finish playing before deleting the temporary file
    while voice_client.is_playing():
        await asyncio.sleep(1)
    os.remove(filename)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # Find the voice channel with the specified ID
    voice_channel = client.get_channel(712008433443799151)
    if not voice_channel:
        print(f'Error: could not find voice channel with ID 712008433443799151')
        exit(1)
    print(f'Connecting to voice channel {voice_channel.name} ({voice_channel.id})')

    # Connect to the voice channel
    voice_client = await voice_channel.connect()
    print(f'Connected to voice channel {voice_channel.name}')

    # Start playing songs in a loop
    while True:
        try:
            if voice_client and voice_client.is_connected():
                await play_song(voice_client)
            else:
                print('Bot is not connected to a voice channel')
                voice_client = None
                await asyncio.sleep(5) # wait 5 seconds before trying to reconnect
                voice_client = await voice_channel.connect()
                print(f'Connected to voice channel {voice_channel.name}')
        except Exception as e:
            print(f'Error: {e}')


# Define the verb and noun arrays
verbs = ['пососи', 'пидор', 'сперма', 'чмо', 'членасос', "выродок", "говно", "карлик"]
verbs2 = ['чё надо?', 'иди помойся', 'тебе пёрнуть?', 'а я ебу?', 'ключ закрыть? да иди нахуй', "я заебался тут торчать,", "пошли в танки", "ты без меня в ключ пошел?"]
nouns1 = ['анимешник', 'портки обосранные', 'пидар', 'ore', 'хуесос']
nouns2 = ['варикозник', 'жепанюх', 'el pidoraso', 'гном', 'пидорас']

@client.event
async def on_message(message):
    # Check that the message was not sent by the bot itself
    if message.author == client.user:
        return
    print(message.content)
    # Check if the message contains 'крол' or 'кромь'
    if 'крол' in message.content or 'кромь' in message.content:
        # Get the sender's nickname
        nickname = message.author.display_name
        # Choose a random verb and noun
        verb = random.choice(verbs)
        verb2 = random.choice(verbs2)
        noun1 = random.choice(nouns1)
        noun2 = random.choice(nouns2) if random.random() < 0.2 else ''
        # Construct the reply message
        reply = f"{nickname} {verb}, {verb2} {noun1}"
        if noun2:
            reply += f", {noun2}"
        # Send the reply message
        await message.channel.send(reply)
    else:
        # Randomly reply with a phrase 10% of the time
        if random.random() < 0.1:
            phrases = [
                'Авг 1200 рио чел',
                'невижу на почте 100000голд',
                'как говарил один пьяный призедент',
                'да мне насрать кто где летает',
                'ля',
                'жалование пришлите',
                'Пидорасы',
                'Гц?',
                'красава, бро',
                'пхахахах',
            ]
            reply = random.choice(phrases)
            await message.channel.send(reply)


    # Handle any other commands or messages as usual
    await client.process_commands(message)

client.run(bot_token)