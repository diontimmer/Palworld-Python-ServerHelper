import time
import concurrent.futures
from client import RCON_CLIENT
import commands
import os

# check if rcon.exe or rcon is in the current dir; if not send a message
# to the console and exit
if not os.path.exists("./rcon") and not os.path.exists("rcon.exe"):
    print(
        "rcon.exe or rcon not found in the current directory! Please download from https://github.com/gorcon/rcon-cli"
    )
    input("Press enter to exit")
    exit()

def catch_logins(rcon_client, interval=1):
    previous_players = set()

    while True:
        player_objs = rcon_client.get_players()
        current_players = {(obj.steam_id, obj.name) for obj in player_objs}

        if previous_players:
            players_left = previous_players - current_players
            players_joined = current_players - previous_players

            with concurrent.futures.ThreadPoolExecutor() as executor:
                for steam_id, name in players_left:
                    time.sleep(1)  # allow time for the player to switch to nickname
                    # check if steam_id is still in the server
                    steamids = rcon_client.get_steam_ids()
                    if steam_id in steamids:
                        continue
                    executor.submit(announce_left, steam_id, name, rcon_client)
                    
                for steam_id, name in players_joined:
                    executor.submit(announce_login, steam_id, rcon_client)

        previous_players = current_players
        time.sleep(interval)

def announce_left(steam_id, name, rcon_client):
    rcon_client.broadcast(f"{name}-[Disconnected!]")
    print(f"{name} left | steam_id: {steam_id}")

def announce_login(steam_id, rcon_client):
    time.sleep(1)  # allow time for the player to switch to nickname
    players = rcon_client.get_players()
    for obj in players:
        if obj.steam_id == steam_id:
            name = obj.name
            rcon_client.broadcast(f"{name}-[Connected!]")
            print(f"{name} joined | steam_id: {steam_id}")
            break

if __name__ == "__main__":
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(catch_logins, RCON_CLIENT, 1)
        executor.submit(commands.run_custom_console)
