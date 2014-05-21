#!/usr/bin/env python
from parser import get_best_ratings, get_list_of_teams

RANGE = .20

# Run a simulation of all pairs in the list of teams
def pairwise_simulate(teams):
    ratings = get_best_ratings()
    list_of_teams = get_list_of_teams()

    f = open("results.csv", 'r')
    f.readline()

    # a result is (rating1, rating2, -1 for loss : 0 for tie : 1 for win)
    results = set([])

    # Determine the result of every game in the file
    for line in f:
        line = line.replace('\"', '')
        [date, home, away, home_goals, away_goals, neutral] = line.split(',')
        home_goals = int(home_goals)
        away_goals = int(away_goals)
        result = 0
        if home_goals == away_goals:
            result = 0
        if home_goals > away_goals:
            result = 1
        if home_goals < away_goals:
            result = -1

        home_rating = ratings[list_of_teams.index(home)]
        away_rating = ratings[list_of_teams.index(away)]

        results.add((home_rating, away_rating, result))
        results.add((away_rating, home_rating, -result))

    f.close()

    outcomes = {}
    for team1 in teams:
        for team2 in teams:

            # only play each game once and with different teams
            if team1 <= team2:
                continue

            # Similar games are defined as those within range
            rating1 = ratings[list_of_teams.index(team1)]
            rating2 = ratings[list_of_teams.index(team2)]

            rating1_lo = rating1 - RANGE
            rating1_hi = rating1 + RANGE
            rating2_lo = rating2 - RANGE
            rating2_hi = rating2 + RANGE

            # WIN, LOSE, DRAW
            similar_games = [0,0,0]

            # Take all similar games
            for result in results:
                (rating1, rating2, res) = result
                if rating1 > rating1_lo and rating1 < rating1_hi:
                    if rating2 > rating2_lo and rating2 < rating2_hi:
                        similar_games[res - 1] = similar_games[res - 1] + 1

            number_of_games = sum(similar_games)
            outcome = [float(x) / number_of_games for x in similar_games]
            outcome_rev = [outcome[1], outcome[0], outcome[2]]
            outcomes[(team1, team2)] = outcome
            outcomes[(team2, team1)] = outcome_rev
    return outcomes

if __name__ == "__main__":
    teams = get_list_of_teams()
    pairwise_simulate(teams)
