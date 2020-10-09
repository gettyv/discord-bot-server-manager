import discord
from discord.ext import commands
import subprocess
import json
import server_commands as server_command
#Defines discord client, can change command prefix here
client = commands.Bot(command_prefix = '$')
#Loads user config and defines variabels
with open('bot_config.json') as f:
    config = json.load(f)

class Game:
    def __init__(self, title, port, query, exit_command):
        self.port = port
        self.title = title
        self.active = False
        self.has_query = query
        self.exit_command = exit_command
        self.start_script = './' + self.title + '.sh'
    
    def start_server(self):
        print(f'Starting {self.title} server')
        server_command.start_server(self)

game_library = {}
for title, info in config['game_library'].items():
    port = info [0]
    if info[1]:
        query_enabled = True
    else:
        query_enabled = False
    exit_command = info[2]
    game_library[title] = Game(title, port, query_enabled, exit_command)

bot_token = config['bot_token']
public_ip = config['public_ip']

#Sends message to console upon loading in and sets listening status for bot
@client.event
async def on_ready():
    """Sends ready message and sets listening status"""
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$help"))

@client.command()
async def start(ctx, game_title):
    """Starts server for the given game"""
    try:
        game = game_library[game_title]
        if game.active:
            await ctx.send(f'{game.title} server already running')
        else:
            await ctx.send(f'Starting {game} server')
            game.start_server()
            game.active = True
    except KeyError:
        await ctx.send(f'{game.title} is not supported or mistyped')

@client.command()
async def stop(ctx, game_title):
    """Stops currently running server if there is one running"""
    try:
        game = game_library[game_title]
        if game.active:
            await ctx.send(f'Stopping {game.title} server')
            game.stop_server()
            game.active = False
        else:
            await ctx.send(f'{game.title} is not currently running')
    except KeyError:
        await ctx.send(f'{game.title} is not supported or mistyped')

@client.command()
async def hello(ctx):
    """Responds with a friendly greeting"""
    await ctx.send('Hello!')

@client.command()
async def library(ctx):
    """Lists available games"""
    output = 'Available games: '
    for game_title in game_library:
        output = output + game_title + ', '
    await ctx.send(output)

@client.command()
async def status(ctx):
    """Checks the status of the currently running servers"""
    if server_status:
        if current_game in ['minecraft', 'mc_modded']:
            await ctx.send(server_command.query_server(current_game, public_ip, current_game_port))
        else:
            await ctx.send(f'There is currently a {current_game} server running')
    else:
        await ctx.send('No active server running')

@client.command()
async def ip(ctx):
    """Returns IP and port info for running servers"""
    for title, game in game_library.items():
        if game.active:
            
    if server_status:
        await ctx.send(f'Info for {current_game} server - IP: {public_ip} | Port: {current_game_port}')
    else:
        await ctx.send('No server running to get IP of')

@client.command()
async def exit(ctx):
    """Exits the bot"""
    if server_status:
        await ctx.send('Cannot exit as there is an active server running!')
    else:
        await ctx.send('Goodbye!')
        await client.close()
        print('Bot exited')

client.run(bot_token)
