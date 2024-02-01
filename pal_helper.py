import time
import threading
from client import RCON_CLIENT
import commands
import os

# check if rcon.exe or rcon is in the current dir; if not send a message
# to the console and exit
if not os.path.exists("./rcon") and not os.path.exists("rcon.exe"):
    print(
        "rcon.exe or rcon not found in current directory! Please download from https://github.com/gorcon/rcon-cli"
    )
    input("Press enter to exit")
    exit()


def catch_logins(rcon_client, interval=1):
    while True:
        previous_names = set(rcon_client.get_names())
        time.sleep(interval)
        current_names = set(rcon_client.get_names())
        people_left = previous_names - current_names
        people_joined = current_names - previous_names
        try:
            for name in people_left:
                rcon_client.broadcast(f"{name}-[Disconnected!]")
                print(f"{name} left")
            for name in people_joined:
                rcon_client.broadcast(f"{name}-[Connected!]")
                print(f"{name} joined")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    # if
    threading.Thread(target=catch_logins, args=(RCON_CLIENT, 1)).start()
    commands.run_custom_console()
