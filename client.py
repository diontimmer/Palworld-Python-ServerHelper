import sys
import os
import subprocess
import json


class PalworldPlayer:
    def __init__(self, name, player_uid, steam_id):
        self.name = name
        self.player_uid = player_uid
        self.steam_id = steam_id

    def __str__(self):
        return (
            f"Name: {self.name}, PlayerUID: {self.player_uid}, SteamID: {self.steam_id}"
        )


class PalworldRconServer:
    def __init__(self, ip, port, password, custom_exec=None):
        self.ip = ip
        self.port = port
        self.password = password
        if custom_exec:
            self.rcon_exec = custom_exec
        else:
            self.rcon_exec = "./rcon" if os.name == "posix" else "rcon.exe"

        print(
            "Palworld Helper by Dion Timmer, replace this when something better is available."
        )
        print("Starting RCON server.. Type 'help' for a list of commands.")

    def _run_command(self, command):
        cmd = [
            self.rcon_exec,
            "-a",
            f"{self.ip}:{self.port}",
            "-p",
            self.password,
        ] + command
        return subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode("utf-8")

    def broadcast(self, message):
        message = message.replace(" ", "_")
        if os.name == "posix":
            msg = f"'Broadcast {message}'"
        else:
            msg = f'"Broadcast {message}"'
        cmd = f"{self.rcon_exec} -a {self.ip}:{self.port} -p {self.password} {msg}"
        os.system(cmd)

    def get_players(self):
        output = self._run_command(["showplayers"]).split("\n")[1:-1]
        return [PalworldPlayer(*player.split(",")) for player in output]

    def get_uids(self):
        raw_uids = [player.player_uid for player in self.get_players()]
        # remove 00000000
        return [uid for uid in raw_uids if uid != "00000000"]

    def get_steam_ids(self):
        raw_steam_ids = [player.steam_id for player in self.get_players()]
        # remove 00000000000000000
        return [
            steam_id for steam_id in raw_steam_ids if steam_id != "00000000000000000"
        ]

    def get_names(self):
        raw_names = [player.name for player in self.get_players()]
        # remove empty names
        return [name for name in raw_names if name != ""]

    def get_player_from_uid(self, uid):
        return next(
            (player for player in self.get_players() if player.player_uid == uid), None
        )

    def get_player_from_name(self, name):
        return next(
            (player for player in self.get_players() if player.name == name), None
        )

    def get_player_from_steam_id(self, steam_id):
        return next(
            (player for player in self.get_players() if player.steam_id == steam_id),
            None,
        )

    def get_steam_id_from_name(self, name):
        player = self.get_player_from_name(name)
        return player.steam_id if player else None


# load config

config = json.load(open("config.json"))
# if password is changeme, send a message to the console and exit
if config["rcon_password"] == "changeme":
    print(
        "Please change the rcon_password in config.json to your server's RCON password"
    )
    input("Press enter to exit")
    exit()

custom_exec = (
    None if config["rcon_exec"] == "current_directory" else config["rcon_exec"]
)
RCON_CLIENT = PalworldRconServer(
    config["server_ip"], config["rcon_port"], config["rcon_password"], custom_exec
)
