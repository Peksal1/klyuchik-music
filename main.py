import asyncio
import discord
from pytube import YouTube
from discord.ext import commands
import random
import os
import discord.opus

# Load the Opus library for audio encoding/decoding
discord.opus.load_opus('libopus.so.0')

# Get the bot token and Twitch client ID from environment variables
bot_token = os.environ.get('DISCORD_BOT_TOKEN')
twitch_client_id = os.environ.get('TWITCH_CLIENT_ID')
twitch_access_token = os.environ.get('TWITCH_ACCESS_TOKEN')
if not bot_token:
    print('Error: no bot token specified in DISCORD_BOT_TOKEN environment variable')
    exit(1)
if not twitch_client_id:
    print('Error: no Twitch client ID specified in TWITCH_CLIENT_ID environment variable')
    exit(1)


# Initialize the Discord client
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# Set the Twitch API endpoint and headers
twitch_api_endpoint = 'https://api.twitch.tv/helix/streams?user_login=peksal1'
twitch_api_headers = {
    'Client-ID': twitch_client_id,
    'Authorization': 'Bearer ' + twitch_access_token
}


# Get the Discord text channel where you want to announce the live status
announcement_channel_id = 712008433443799150 # replace with the ID of your channel
announcement_channel = None

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
        global announcement_channel
    announcement_channel = client.get_channel(announcement_channel_id)
    print(f'Logged in as {client.user} and ready to announce live status in #{announcement_channel.name}')

async def announce_live_status():
    # Check the Twitch API to see if the channel is live
    response = requests.get(twitch_api_endpoint, headers=twitch_api_headers)
    if response.status_code == 200:
        data = response.json()
        if data['data'] and data['data'][0]['type'] == 'live':
            # The channel is live, so announce it in the Discord channel
            await announcement_channel.send('@everyone peksal1 is now live! Watch at https://www.twitch.tv/peksal1')
        else:
            # The channel is not live
            print('peksal1 is currently offline')
    else:
        # There was an error with the Twitch API request
        print(f'Error getting live status for peksal1: {response.status_code}')

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
nouns1 = ['анимешник', 'портки обосранные', 'пидар', 'ore', 'хуесос', "еще пэнсел, пэнсил покричи", "милидэнсер хуев"]
nouns2 = ['варикозник', 'жепанюх', 'el pidoraso', 'гном', 'пидорас']

@client.event
async def on_member_join(member):
    # Get the channel where you want to send the greeting
    channel = client.get_channel(712008433443799150)
    # Choose a random verb and noun
    verb = random.choice(verbs)
    verb2 = random.choice(verbs2)
    noun1 = random.choice(nouns1)
    noun2 = random.choice(nouns2) if random.random() < 0.2 else ''
    # Construct the greeting message
    greeting = f"{member.mention} {verb}, добро пожаловать в ключик в дурку! {verb2} {noun1}"
    if noun2:
        greeting += f", {noun2}"
    # Send the greeting message
    await channel.send(greeting)

@client.event
async def on_message(message):
    # Check that the message was not sent by the bot itself
    if message.author == client.user:
        return

    # 10%
    if random.random() > 0.90:
        # Get the sender's nickname
        nickname = message.author.mention
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
        if random.random() < 0.05:
            phrases = [
                'Авг 1200 рио чел',
                'невижу на почте 100000голд',
                'как говарил один пьяный призедент',
                'да мне насрать кто где летает',
                "милидэнс",
                "пэнсел"
                'ля',
                'жалование пришлите',
                'Пидорасы',
                'Гц?',
                'красава, бро',
                'пхахахах',
            ]
            reply = random.choice(phrases)
            await message.channel.send(reply)

# Schedule the live status announcement to run every 5 minutes
client.loop.create_task(announce_live_status())
client.run(bot_token)