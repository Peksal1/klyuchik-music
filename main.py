import asyncio
import discord
from pytube import YouTube
from discord.ext import commands
import random
import os
import discord.opus
import requests
import re

# Load the Opus library for audio encoding/decoding
discord.opus.load_opus('libopus.so.0')
users = {
    'peksal1': 'Бродерман',
    'flocke456': 'Натика'
}
user_statuses = {user: {'status': False, 'wow_nickname': users.get(user, 'user')} for user in users}

endpoint = 'https://klyuchik-v-durku-backend.herokuapp.com/is-streaming/'
# Get the bot token from the environment variable
bot_token = os.environ.get('DISCORD_BOT_TOKEN')
if not bot_token:
    print('Error: no bot token specified in DISCORD_BOT_TOKEN environment variable')
    exit(1)

# Initialize the Discord client
intents = discord.Intents.default()

intents.members = True
client = discord.Client(command_prefix='/', intents=intents, port=os.environ.get('PORT'))

url_regex = re.compile(r'^https?://(?:www\.)?youtube\.com/watch\?v=([A-Za-z0-9_-]{11})$')

@bot.command()
async def add(ctx, url: str, name: str):
    if 'youtube.com' not in url:
        await ctx.send('Invalid URL. Only YouTube URLs are allowed.')
    else:
        video_urls.append((url, name))
        await ctx.send(f'Added {name} ({url}) to video URLs.')

@bot.command()
async def remove(ctx, name: str):
    urls_to_remove = [u for u in video_urls if u[1] == name]
    if len(urls_to_remove) == 0:
        await ctx.send(f'No video URLs found with the name {name}.')
    elif len(urls_to_remove) == 1:
        video_urls.remove(urls_to_remove[0])
        await ctx.send(f'Removed {name} from video URLs.')
    else:
        urls_str = '\n'.join([u[0] for u in urls_to_remove])
        await ctx.send(f'There are multiple video URLs with the name {name}:\n{urls_str}\nPlease use the name that corresponds to the URL you want to remove.')

@bot.command()
async def list(ctx):
    if len(video_urls) == 0:
        await ctx.send('No video URLs added yet.')
    else:
        urls_str = '\n'.join([f'{u[1]}: {u[0]}' for u in video_urls])
        await ctx.send(f'Video URLs:\n{urls_str}')

# List of YouTube video URLs to play
video_urls = [
    #'https://www.youtube.com/watch?v=jumQ76GEYLQ', #
    #'https://www.youtube.com/watch?v=Cz5q05Hl5gs', #
    #'https://www.youtube.com/watch?v=Uift1RYej0w', #
    #'https://www.youtube.com/watch?v=qT_R_D3tCes', #
   # 'https://www.youtube.com/watch?v=6IUqSY783_8', # собака писала
   # 'https://www.youtube.com/watch?v=vkPXG11Fj_U', # шипупи
    #'https://www.youtube.com/watch?v=G6pqAN8ALC8', # пасха
    #'https://www.youtube.com/watch?v=azd1ZnHNt9g', # радужный гимн
    #'https://www.youtube.com/watch?v=t4TnTqH6E8M', # Мальчик на девятке
    'https://www.youtube.com/watch?v=pUROT2f6azM', # drop
    'https://www.youtube.com/watch?v=heLj63wUIrk', # gender
    'https://www.youtube.com/watch?v=PpSTwj6Plc8', # gravy train 
    'https://www.youtube.com/watch?v=6bYEtcwDhU8', # mdma
    'https://www.youtube.com/watch?v=e-ndA04nCao', # do it like a russian
    'https://www.youtube.com/watch?v=XjrPJRwY3s0', # bassmark
    'https://www.youtube.com/watch?v=fKopy74weus', # thunder
    'https://www.youtube.com/watch?v=QvyclAhWlAY', # shaman king
    'https://www.youtube.com/watch?v=6Wvda9AkDnM', # zombie
    'https://www.youtube.com/watch?v=YZKESqe4MIU', # monkeys
    'https://www.youtube.com/watch?v=KR-eV7fHNbM', # calling
    'https://www.youtube.com/watch?v=I_2D8Eo15wE', # black betty
    'https://www.youtube.com/watch?v=8sz2kxRxfzM', # мое сердце
    'https://www.youtube.com/watch?v=K6BRna4_bmg', # edamame
    'https://www.youtube.com/watch?v=p47fEXGabaY', # livin da vida loca
    'https://www.youtube.com/watch?v=MxJKqd8sPy0', # holding on
]

async def check_streaming_status(user):
    while True:
        try:
            response = requests.get(endpoint + user)
            data = response.json()
            is_streaming = data['isStreaming']

            # Check if streaming status has changed
            if user in user_statuses and user_statuses[user]['status'] != is_streaming:
                if is_streaming:
                    print(f'{user_statuses[user]["wow_nickname"]} включил стрим!')
                    # Replace 712008433443799150 with your Discord channel ID
                    channel = client.get_channel(1088848545261572116)
                    await channel.send(f'{user_statuses[user]["wow_nickname"]} включил стрим! Заходим на https://www.twitch.tv/{user}')
                else:
                    print(f'{user_statuses[user]["wow_nickname"]} выключил стрим!')
                    # Replace 712008433443799150 with your Discord channel ID
                    channel = client.get_channel(1088848545261572116)
                    await channel.send(f'{user_statuses[user]["wow_nickname"]} выключил стрим!')

            # Update streaming status
            user_statuses[user]['status'] = is_streaming

            # Wait 5 minutes before checking again
            await asyncio.sleep(300)

        except Exception as e:
            print(f'Error: {e}')
            # Wait 30 seconds before trying again
            await asyncio.sleep(30)


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

    # Start checking streaming status for each user in the array
    for user in users:
        asyncio.ensure_future(check_streaming_status(user))

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
nouns1 = ['анимешник', 'портки обосранные', 'пидар', 'ore', 'хуесос', 'Ле перфекто!', "еще пэнсел, пэнсил покричи", "милидэнсер хуев"]
nouns2 = ['варикозник', 'жепанюх', 'el pidoraso', 'гном', 'пидорас', 'Ле перфекто!']

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

    # 5%
    if random.random() > 0.95:
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
    elif random.random() < 0.05:
        # Randomly reply with a phrase 5% of the time
            phrases = [
                'Авг 1200 рио чел',
                'невижу на почте 100000голд',
                'как говарил один пьяный призедент',
                'да мне насрать кто где летает',
                "милидэнс",
                "пэнсел",
                'ля',
                'жалование пришлите',
                'Пидорасы',
                'Гц?',
                'красава, бро',
                'пхахахах',
                'Пошла ебка',
                'Ле перфекто!'
            ]
            reply = random.choice(phrases)
            await message.channel.send(reply)

client.run(bot_token)