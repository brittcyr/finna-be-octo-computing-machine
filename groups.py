#!/usr/bin/env python
from random import random, seed
from games_precompute import pairwise_simulate

#1A vs 2B
#1C vs 2D

#1E vs 2F
#1G vs 2H

#1B vs 2A
#1D vs 2C

#1F vs 2E
#1H vs 2G

# To get to next round, we just take adjacent teams and play the match, then append the winner to the next array
#Knockout = [A[0], B[1], C[0], D[1], E[0], F[1], G[0], H[1], A[1], B[0], C[1], D[0], E[1], F[0], G[1], H[0]]


# Play an individual game based on similar games and add a small points tweak
def play_game(team1, team2, precomputed_table):
    # Small random error so that I will not have to deal with tie breakers later
    tweak = random() / 100
    (win, loss, tie) = precomputed_table[(team1, team2)]
    outcome = random()
    if win > outcome:
        return 3 + tweak, 0 + tweak
    if win + loss > outcome:
        return 0 + tweak, 3 + tweak
    return 1 + tweak, 1 + tweak


# Sort the group in the proper order
def play_group_stage(group, precomputed_table):
    points = {}
    for team in group:
        points[team] = 0

    for team1 in group:
        for team2 in group:
            if team1 <= team2:
                continue

            team1_score, team2_score = play_game(team1, team2, precomputed_table)
            points[team1] = points[team1] + team1_score
            points[team2] = points[team2] + team2_score

    print points
    group_sorted = sorted(points.keys(), key=points.get, reverse=True)
    print group_sorted


# Run a group stage simulation
def run_simulation():
    # This is the list of groups
    A = ['Brazil', 'Croatia', 'Mexico', 'Cameroon']
    B = ['Spain', 'Netherlands', 'Chile', 'Australia']
    C = ['Colombia', 'Greece', 'C\xc3\xb4te dIvoire', 'Japan']
    D = ['Uruguay', 'Costa Rica', 'England', 'Italy']
    E = ['Switzerland', 'Ecuador', 'France', 'Honduras']
    F = ['Argentina', 'Bosnia-Herzegovina', 'Iran', 'Nigeria']
    G = ['Germany', 'Portugal', 'Ghana', 'United States']
    H = ['Belgium', 'Algeria', 'Russia', 'Korea Republic']

    groups = [A, B, C, D, E, F, G, H]

    qualified = sum(groups, [])
    precomputed_table = pairwise_simulate(qualified)
    for group in groups:
        group = play_group_stage(group, precomputed_table)


if __name__ == "__main__":
    run_simulation()
