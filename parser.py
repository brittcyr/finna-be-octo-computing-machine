



def load_file():
    f = open("results.csv", 'r')
    f.readline()
    teams = set([])
    for line in f:
        line = line.replace('\"', '')
        [date, home, away, home_goals, away_goals, neutral] = line.split(',')
        teams.add(home)
        teams.add(away)
        print home, away
    f.close()

    list_of_teams = sorted(list(teams))

    print list_of_teams








if __name__ == "__main__":
    load_file()
