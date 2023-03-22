    import discord
    import asyncio
    from pytube import YouTube
    from discord.ext import commands
    import random
    import os
    import discord.opus

    # Load the Opus library for audio encoding/decoding
    discord.opus.load_opus('libopus.so.0')

# Specify the channel ID where the bot should send the message
channel_id = 712008433443799150


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

async def send_hello():
    # Choose a random delay between 1 and 5 minutes
    delay = random.randint(60, 300)

    # Wait for the specified delay
    await asyncio.sleep(delay)

    # Get the channel object where the bot should send the message
    channel = client.get_channel(channel_id)

    # Send the message in the channel
    await channel.send('Пидорасы')


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

    # Start sending "hello" messages in a loop
    while True:
        try:
            await send_hello()
        except Exception as e:
            print(f'Error: {e}')

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

    client.run(bot_token)