import discord
import asyncio
from pytube import YouTube
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

@client.event
async def on_message(message):
    # Check that the message was not sent by the bot itself
    if message.author == client.user:
        return

    # Randomly reply with a phrase 10% of the time
    if random.random() < 0.1:
        phrases = [
            'Авг 1200 рио чел',
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