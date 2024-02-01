from client import RCON_CLIENT
import threading


def run_custom_console():
    threading.Thread(target=run_cmd_loop).start()


def run_cmd_loop():
    while True:
        cmd_input = input(">")
        args = cmd_input.split(" ")
        command = args.pop(0)
        on_command(command, args)


def on_command(command, args):
    command = command.lower()
    if command in commands:
        commands[command]["function"](args)
    elif command == "help":
        print_help()
    else:
        print("Invalid command")


def print_help():
    for cmd, info in commands.items():
        print(f"{cmd}: {info['description']}")
        if info["usage"]:
            print(f"  Usage: {info['usage']}")
        print()  # Blank line for readability


commands = {}


def command(name, description="No description available", usage=""):
    def decorator(func):
        commands[name] = {"function": func, "description": description, "usage": usage}
        return func

    return decorator


@command("broadcast", "Broadcasts a message to all players", "broadcast <message>")
def handle_broadcast(args):
    if not args:
        print("Usage: broadcast <message>")
    RCON_CLIENT.broadcast(" ".join(args))


@command("players", "Lists all players")
def handle_players(args):
    player_objects = RCON_CLIENT.get_players()
    for player in player_objects:
        print(player)


@command("uids", "Lists all player UIDs")
def handle_uids(args):
    print(RCON_CLIENT.get_uids())


@command("steamids", "Lists all player SteamIDs")
def handle_steamids(args):
    print(RCON_CLIENT.get_steam_ids())


@command("list", "Lists all player names")
def handle_list(args):
    print(RCON_CLIENT.get_names())


@command("playerinfo", "Lists all player info", "playerinfo <name>")
def handle_playerinfo(args):
    if not args:
        print("Usage: playerinfo <name>")
        return
    print(RCON_CLIENT.get_player_from_name(args[0]))


@command("steamid", "Gets a player's steamid", "steamid <name>")
def handle_steamid(args):
    if not args:
        print("Usage: steamid <name>")
        return
    print(RCON_CLIENT.get_steam_id_from_name(args[0]))


@command("save", "Saves the game")
def handle_save(args):
    print(RCON_CLIENT._run_command(["save"]))


@command("kick", "Kicks a player", "kick <name>")
def handle_kick(args):
    if not args:
        print("Usage: kick <name>")
        return
    steamid = RCON_CLIENT.get_steam_id_from_name(args[0])
    if steamid is None:
        print("Player not found")
        return
    print(RCON_CLIENT._run_command(["KickPlayer", steamid]))


@command("ban", "Bans a player", "ban <name>")
def handle_ban(args):
    if not args:
        print("Usage: ban <name>")
        return
    steamid = RCON_CLIENT.get_steam_id_from_name(args[0])
    if steamid is None:
        print("Player not found")
        return
    print(RCON_CLIENT._run_command(["BanPlayer", steamid]))
