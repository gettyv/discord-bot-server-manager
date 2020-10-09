import subprocess
from mcstatus import MinecraftServer

def start_server(game):
    """Starts server when given a game object"""
    script_name = game.start_script
    game.server_process = subprocess.Popen(script_name, stdin = subprocess.PIPE, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    print(f'Starting {game.title} server process')

def stop_server(game):
    """Communicates with server process to stop server when given a game object"""
    print(f'Attempting to stop {game} server process')
    game.server_process.communicate(str.encode(game.exit_command))

def query_server(game):
    """Requests advanced server status data for minecraft servers(must be enabled in server.properties)"""
    names = ''
    query_server = MinecraftServer(game.ip, game.port)
    query = query_server.query()
    if query.players.online == 0:
        output = f'There are no players on the currently running {game.title} server'
    elif query.players.online == 1:
        output = f'{query.players.names[0]} is on the currently running {game.title} server'
    else:
        for name in query.players.names:
            names = names + name + ', '
        output = f'{query.players.online} players are on the {game.title} server: {names}'
    return output
