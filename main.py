import discord
import asyncio
from pytube import YouTube
import random
import os
import discord.opus
discord.opus.load_opus('libopus.so.0')

bot_token = os.environ['DISCORD_BOT_TOKEN']
print('hello')
# Replace YOUR_TOKEN_HERE with your bot's token
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# List of YouTube video URLs
video_urls = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=2ZIpFytCSVc',
    'https://www.youtube.com/watch?v=3GwjfUFyY6M',
]

async def play_song(voice_client):
    # Choose a random video URL from the list
    url = random.choice(video_urls)

    # Download the video
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.download()

    # Send the audio to the voice channel
    voice_client.play(discord.FFmpegPCMAudio(filename))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # Find the voice channel with the specified ID
    voice_channel = client.get_channel(712008433443799151)
    print(f'Connecting to voice channel {voice_channel.name} ({voice_channel.id})')

    # Connect to the voice channel
    voice_client = await voice_channel.connect()
    print('Connected to voice channel')

    # Start playing songs
    while True:
        await play_song(voice_client)
        print('Playing a song')
        await asyncio.sleep(5) # wait 5 seconds before playing the next song   

client.run(bot_token)