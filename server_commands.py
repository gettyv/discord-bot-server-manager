import subprocess
from mcstatus import MinecraftServer

def start_server(game):
    """Starts server when given a game"""
    global server_process
    server_process = subprocess.Popen('./' + game + '.sh', stdin = subprocess.PIPE, stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL)
    print(f'Starting {game} server process')

def stop_server(game):
    """Communicates with server process to stop server"""
    if game == 'minecraft' or game == 'mc_modded':
        exit_command = 'stop'
    if game == 'terraria':
        exit_command = 'exit'
    print(f'Attempting to stop {game} server process')
    server_process.communicate(str.encode(exit_command))

def query_server(game, ip, port):
    """Requests advanced server status data for minecraft servers(must be enabled in server.properties)"""
    names = ''
    query_server = MinecraftServer(ip, int(port))
    query = query_server.query()
    if query.players.online == 0:
        output = f'There are no players on the currently running {game} server'
    elif query.players.online == 1:
        output = f'{query.players.names[0]} is on the currently running {game} server'
    else:
        for name in query.players.names:
            names = names + name + ', '
        output = f'{query.players.online} players are on the {game} server: {names}'
    return output
