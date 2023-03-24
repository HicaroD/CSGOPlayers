import ast
import csv
import re
from typing import List


def clean_name(name: str):
    return "a" + re.sub("\W+", "", name).replace(" ", "_")


def read_players_dataset():
    csgo_players = []
    with open("./csgo_players.csv") as file:
        dataset = csv.DictReader(file)
        for row in dataset:
            player_name, current_team = row["nick"], ast.literal_eval(row["teams"])[0]
            csgo_players.append((player_name, current_team))
    return csgo_players


def build_cypher_command(label_name: str, data_name: str):
    return f'({clean_name(data_name)}:{label_name} {{name: "{data_name}"}}),'


def build_cyper_relationship_command(
    first_node_name: str,
    relationship_name: str,
    second_node_name: str,
):
    # TODO: refactor this
    converted_first_node_name = clean_name(first_node_name)
    converted_second_node_name = clean_name(second_node_name)
    return f"({converted_first_node_name}) -[:{relationship_name}]-> ({converted_second_node_name}),"


def create_players_commands(csgo_players_data: List[tuple[str, str]]):
    commands = []
    for player_name, _ in csgo_players_data:
        command = build_cypher_command("PLAYER", player_name)
        if command not in commands:
            commands.append(command)
    return commands


def create_teams_commands(csgo_players_data: List[tuple[str, str]]):
    commands = []
    for _, team_name in csgo_players_data:
        command = build_cypher_command("TEAM", team_name)
        if command not in commands:
            commands.append(command)
    return commands


def create_relationships_commands(csgo_players_data: List[tuple[str, str]]):
    commands = []
    for player_name, team_name in csgo_players_data:
        commands.append(
            build_cyper_relationship_command(player_name, "PLAYS_FOR", team_name)
        )
    return commands


def convert_player_data_to_cypher_commands(csgo_players_data: List[tuple[str, str]]):
    commands = ["CREATE"]
    commands += create_players_commands(csgo_players_data)
    commands += create_teams_commands(csgo_players_data)
    commands += create_relationships_commands(csgo_players_data)
    return commands


def create_file_with_commands(cypher_commands: List[str]):
    with open("commands.txt", "w") as file:
        for i, command in enumerate(cypher_commands):
            if i == len(cypher_commands) - 1:
                command = command.removesuffix(",") + ";"
            file.write(command)
            file.write("\n")


def main():
    csgo_players = read_players_dataset()
    commands = convert_player_data_to_cypher_commands(csgo_players)
    print(commands)
    create_file_with_commands(commands)


if __name__ == "__main__":
    main()
