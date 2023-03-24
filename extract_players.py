import ast
import csv
from typing import List


def read_players_dataset():
    csgo_players = []
    with open("./csgo_players.csv") as file:
        dataset = csv.DictReader(file)
        for row in dataset:
            player_name, current_team = row["nick"], ast.literal_eval(row["teams"])[0]
            csgo_players.append((player_name, current_team))
    return csgo_players


def get_base_create_command(player_name: str, current_team: str):
    return f'MERGE (:PLAYER {{name: "{player_name}"}}) -[:PLAYS_FOR]-> (:TEAM {{name: "{current_team}"}})'


def convert_player_data_to_cypher_commands(csgo_players_data: List[tuple[str, str]]):
    commands = []
    for player_name, current_team in csgo_players_data:
        commands.append(get_base_create_command(player_name, current_team))
    return commands


def create_file_with_commands(cypher_commands):
    with open("commands.txt", "w") as file:
        for command in cypher_commands:
            file.write(command + "\n")


def main():
    csgo_players = read_players_dataset()
    commands = convert_player_data_to_cypher_commands(csgo_players)
    create_file_with_commands(commands)


if __name__ == "__main__":
    main()
