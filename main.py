import discord
import asyncio
from pytube import YouTube
import random
import os

bot_token = os.environ['DISCORD_BOT_TOKEN']

# Replace YOUR_TOKEN_HERE with your bot's token
client = discord.Client()

# List of YouTube video URLs
video_urls = [
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=2ZIpFytCSVc',
    'https://www.youtube.com/watch?v=3GwjfUFyY6M',
]

async def play_song():
    # Choose a random video URL from the list
    url = random.choice(video_urls)

    # Download the video
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).first()
    filename = stream.download()

    # Send the audio to the voice channel
    voice_channel = client.get_channel(VOICE_CHANNEL_ID)
    voice_client = await voice_channel.connect()
    voice_client.play(discord.FFmpegPCMAudio(filename))

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

    # Start playing songs
    while True:
        await play_song()
        await asyncio.sleep(5) # wait 5 seconds before playing the next song

# Replace VOICE_CHANNEL_ID with the ID of the voice channel you want the bot to join
client.run('bot_token')