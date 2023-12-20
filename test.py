import re
import valve.rcon

# Connect to RCON server
server_address = ('pug.amsgaming.in', 27015)
rcon_password = 'myrconok'

with valve.rcon.RCON(server_address, rcon_password) as rcon: 
    res = rcon.execute(f'status')
    rcon_data = res.body.decode('utf-8', 'ignore')

    # Extract data using regular expressions
    hostname_pattern = r'hostname:\s*(.*)'
    version_pattern = r'version\s*:\s*(.*)'
    udp_pattern = r'udp/ip\s*:\s*(.*)'
    os_pattern = r'os/ip\s*:\s*(.*)'
    type_pattern = r'type/ip\s*:\s*(.*)'
    map_pattern = r'map\s*:\s*(.*)'
    gotv_pattern = r'gotv[0]\s*:\s*(.*)'
    players_pattern = r'players\s*:\s*(.*)'

    hostname = re.search(hostname_pattern, rcon_data).group(1)
    version = re.search(version_pattern, rcon_data).group(1)
    map_name = re.search(map_pattern, rcon_data).group(1)
    players = re.search(players_pattern, rcon_data).group(1)

    # Print extracted data
    print(f"Hostname: {hostname}")
    print(f"Version: {version}")
    print(f"Map Name: {map_name}")
    print(f"Players: {players}")

    # Extract player list from RCON result
    players = []
    for line in rcon_data.split("\n"):
        if "#" in line:
            player_data = line.split()
            player = {}
            player["id"] = player_data[0]
            player["name"] = " ".join(player_data[1])
            player["score"] = player_data[2]
            player["ping"] = player_data[3]
            players.append(player)

    print("Player List:")
    for player in players:
        print(player)