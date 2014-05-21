#!/usr/bin/env python
from random import random
from games_precompute import pairwise_simulate
from numpy import zeros

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

def play_game_to_winner(team1, team2, precomputed_table):
    score1, score2 = play_game(team1, team2, precomputed_table)
    while score1 < 3 and score2 < 3:
        score1, score2 = play_game(team1, team2, precomputed_table)
    return int(score1), int(score2)


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

    group_sorted = sorted(points.keys(), key=points.get, reverse=True)
    return group_sorted


# Run a group stage simulation
def run_simulation(precomputed_table):
    # This is the list of groups
    A = ['Brazil', 'Croatia', 'Mexico', 'Cameroon']
    B = ['Spain', 'Netherlands', 'Chile', 'Australia']
    C = ['Colombia', 'Greece', 'C\xc3\xb4te dIvoire', 'Japan']
    D = ['Uruguay', 'Costa Rica', 'England', 'Italy']
    E = ['Switzerland', 'Ecuador', 'France', 'Honduras']
    F = ['Argentina', 'Bosnia-Herzegovina', 'Iran', 'Nigeria']
    G = ['Germany', 'Portugal', 'Ghana', 'United States']
    H = ['Belgium', 'Algeria', 'Russia', 'Korea Republic']

    # This gets a list of all teams
    groups = [A, B, C, D, E, F, G, H]
    qualified = sum(groups, [])

    A = play_group_stage(A, precomputed_table)
    B = play_group_stage(B, precomputed_table)
    C = play_group_stage(C, precomputed_table)
    D = play_group_stage(D, precomputed_table)
    E = play_group_stage(E, precomputed_table)
    F = play_group_stage(F, precomputed_table)
    G = play_group_stage(G, precomputed_table)
    H = play_group_stage(H, precomputed_table)

    knockout = [A[0], B[1], C[0], D[1], E[0], F[1], G[0], H[1],
                A[1], B[0], C[1], D[0], E[1], F[0], G[1], H[0]]

    round_of_8 = []
    for ind in range(0, len(knockout), 2):
        score1, score2 = play_game_to_winner(knockout[ind], knockout[ind + 1], precomputed_table)
        if score1 > score2:
            round_of_8.append(knockout[ind])
        else:
            round_of_8.append(knockout[ind + 1])

    round_of_4 = []
    for ind in range(0, len(round_of_8), 2):
        score1, score2 = play_game_to_winner(round_of_8[ind], round_of_8[ind + 1], precomputed_table)
        if score1 > score2:
            round_of_4.append(round_of_8[ind])
        else:
            round_of_4.append(round_of_8[ind + 1])

    round_of_2 = []
    for ind in range(0, len(round_of_4), 2):
        score1, score2 = play_game_to_winner(round_of_4[ind], round_of_4[ind + 1], precomputed_table)
        if score1 > score2:
            round_of_2.append(round_of_4[ind])
        else:
            round_of_2.append(round_of_4[ind + 1])

    champion = []
    runner_up = []
    score1, score2 = play_game_to_winner(round_of_2[0], round_of_2[1], precomputed_table)
    if score1 > score2:
        runner_up.append(round_of_2[1])
        champion.append(round_of_2[0])
    else:
        runner_up.append(round_of_2[0])
        champion.append(round_of_2[1])

    # RESULT is [[Knocked out in group stage],
    #            [Knocked out in last 16],
    #            [Knocked out in quarter-finals],
    #            [Knocked out in semi-finals],
    #            [Runner-up],
    #            [Champion],]

    out_in_group_stage = [team for team in qualified if team not in knockout]
    out_in_last_16 = [team for team in knockout if team not in round_of_8]
    out_in_last_8 = [team for team in round_of_8 if team not in round_of_4]
    out_in_last_4 = [team for team in round_of_4 if team not in round_of_2]

    result = [out_in_group_stage, out_in_last_16, out_in_last_8, out_in_last_4, runner_up, champion]
    return result

def do_simulations():
    # This is the list of groups
    A = ['Brazil', 'Croatia', 'Mexico', 'Cameroon']
    B = ['Spain', 'Netherlands', 'Chile', 'Australia']
    C = ['Colombia', 'Greece', 'C\xc3\xb4te dIvoire', 'Japan']
    D = ['Uruguay', 'Costa Rica', 'England', 'Italy']
    E = ['Switzerland', 'Ecuador', 'France', 'Honduras']
    F = ['Argentina', 'Bosnia-Herzegovina', 'Iran', 'Nigeria']
    G = ['Germany', 'Portugal', 'Ghana', 'United States']
    H = ['Belgium', 'Algeria', 'Russia', 'Korea Republic']

    # This gets a list of all teams
    groups = [A, B, C, D, E, F, G, H]
    qualified = sum(groups, [])

    precomputed_table = pairwise_simulate(qualified)
    NUM_SIMULATIONS = 1000000

    NUM_ROUNDS = 6
    results = zeros(( len(qualified), NUM_ROUNDS))

    for sim in range(NUM_SIMULATIONS):
        result = run_simulation(precomputed_table)
        # RESULT is [[Knocked out in group stage],
        #            [Knocked out in last 16],
        #            [Knocked out in quarter-finals],
        #            [Knocked out in semi-finals],
        #            [Runner-up],
        #            [Champion],]

        for cur_round in range(len(result)):
            teams = result[cur_round]
            for team in teams:
                results[qualified.index(team)][cur_round] += 1

    for ind in range(len(results)):
        name = qualified[ind]
        group = format(float(results[ind][0]) / NUM_SIMULATIONS, 'f')
        knockout = format(float(results[ind][1]) / NUM_SIMULATIONS, 'f')
        quarter = format(float(results[ind][2]) / NUM_SIMULATIONS, 'f')
        semi = format(float(results[ind][3]) / NUM_SIMULATIONS, 'f')
        runner_up = format(float(results[ind][4]) / NUM_SIMULATIONS, 'f')
        winner = format(float(results[ind][5]) / NUM_SIMULATIONS, 'f')

        print '{name}\t{group}\t{knockout}\t{quarter}\t{semi}\t{runner_up}\t{winner}'.format(name=name,group=group,knockout=knockout,quarter=quarter,semi=semi,runner_up=runner_up,winner=winner)


if __name__ == "__main__":
    do_simulations()
