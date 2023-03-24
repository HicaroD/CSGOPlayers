import csv

def read_players_dataset():
    csgo_players = []
    with open("./csgo_players.csv") as file:
        dataset = csv.reader(file) 
        for row in dataset:
            player_name, nationality = row[0], row[1]
            csgo_players.append((player_name, nationality))
    return csgo_players

def main():
    csgo_players = read_players_dataset()
    print(csgo_players)

if __name__ == "__main__":
    main()