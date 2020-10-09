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
    def __init__(self, title, port, query):
        self.port = port
        self.title = title
        self.active = False
        self.has_query = query
        self.start_script = './' + self.title + '.sh'

game_library = {}
for title, info in config['game_library'].items():
    if info[1]:
        query_enabled = True
    else:
        query_enabled = False
    port = info [0]
    game_library[title] = Game(title, port, query_enabled)

bot_token = config['bot_token']
public_ip = config['public_ip']

#Sends message to console upon loading in and sets listening status for bot
@client.event
async def on_ready():
    """Sends ready message and sets listening status"""
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="$help"))

@client.command()
async def start(ctx, game):
    """Starts server for the given game"""
    global server_status
    global current_game
    global current_game_port
    if not server_status:
        if game in game_library:
            await ctx.send(f'Starting {game} server')
            server_command.start_server(game)
            current_game = game
            current_game_port = config[current_game + "_port"]
            server_status = True
        else:
            await ctx.send(f'{game} is not supported')
    else:
        await ctx.send(f'{current_game} server already running')

@client.command()
async def stop(ctx):
    """Stops currently running server if there is one running"""
    global server_status
    global current_game
    global current_game_port
    if server_status:
        await ctx.send(f'Stopping {current_game} server')
        server_command.stop_server(current_game)
        current_game = None
        current_game_port = None
        server_status = False
    else:
        await ctx.send('No server currently running')

@client.command()
async def hello(ctx):
    """Responds with a friendly greeting"""
    await ctx.send('Hello!')

@client.command()
async def library(ctx):
    """Lists available games"""
    output = 'Available games: '
    for game in game_library:
        if game == current_game:
            game = '*' + game + '*' #This will highlight the current game
        output = output + game + ', '
    await ctx.send(output)

@client.command()
async def status(ctx):
    """Checks the status of the currently running server"""
    if server_status:
        if current_game in ['minecraft', 'mc_modded']:
            await ctx.send(server_command.query_server(current_game, public_ip, current_game_port))
        else:
            await ctx.send(f'There is currently a {current_game} server running')
    else:
        await ctx.send('No active server running')

@client.command()
async def ip(ctx):
    """Returns IP and port info for running server"""
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
