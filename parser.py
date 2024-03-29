import numpy
from numpy import zeros
from numpy.linalg import inv


HOME_ADVANTAGE = 0
BRAZIL_BOOST = .5

# This is for removing blowouts or really old games etc.
def using_game(home, away, home_goals, away_goals):
    if abs(int(home_goals) - int(away_goals)) > 6:
        return False
    return True

# Total number of games that are used
def get_number_of_games():
    f = open("results.csv", 'r')
    f.readline()
    count = 0
    for line in f:
        line = line.replace('\"', '')
        [date, home, away, home_goals, away_goals, neutral] = line.split(',')
        if using_game(home, away, home_goals, away_goals):
            count += 1
    f.close()
    return count

# List of all teams
def get_list_of_teams():
    f = open("results.csv", 'r')
    f.readline()
    teams = set([])
    for line in f:
        line = line.replace('\"', '')
        [date, home, away, home_goals, away_goals, neutral] = line.split(',')
        teams.add(home)
        teams.add(away)
    f.close()
    list_of_teams = sorted(list(teams))
    return list_of_teams

# Number of teams overall
def get_number_of_teams():
    return len(get_list_of_teams())

# Matrix of adjusted score differentials
def get_y():
    y = [0] * get_number_of_games()
    f = open("results.csv", 'r')
    f.readline()
    teams = set([])
    ind = 0
    for line in f:
        line = line.replace('\"', '')
        [date, home, away, home_goals, away_goals, neutral] = line.split(',')
        if using_game(home, away, home_goals, away_goals):
            home_field = abs(1 - int(neutral)) * HOME_ADVANTAGE
            y[ind] = int(home_goals) - int(away_goals) + HOME_ADVANTAGE
            ind += 1
    f.close()
    return y

# This is the matrix of games played
def get_x():
    x = zeros(( get_number_of_games(), get_number_of_teams()))
    list_of_teams = get_list_of_teams()
    f = open("results.csv", 'r')
    f.readline()
    teams = set([])
    ind = 0
    for line in f:
        line = line.replace('\"', '')
        [date, home, away, home_goals, away_goals, neutral] = line.split(',')
        if using_game(home, away, home_goals, away_goals):
            x[ind][list_of_teams.index(home)] = 1
            x[ind][list_of_teams.index(away)] = -1
            ind += 1
    f.close()
    return x

# This optimizes the homefield advantage over the data set
def get_best_ratings():
    list_of_teams = get_list_of_teams()
    number_of_teams = len(list_of_teams)
    number_of_games = get_number_of_games()

    global HOME_ADVANTAGE
    best_advantage = 0.0
    best_error = 999999999
    best_ratings = None
    Xm = numpy.mat(numpy.array(get_x()))
    for val in range(-200, 200):
        HOME_ADVANTAGE = 1.0 / 100 * val
        Ym = numpy.mat(numpy.array(get_y()))
        r = numpy.linalg.pinv(Xm).dot(Ym.T)

        e = Xm.dot(r) - Ym
        e_norm = numpy.linalg.norm(e)

        if best_error > e_norm:
            best_error = e_norm
            best_advantage = HOME_ADVANTAGE
            best_ratings = r

    # Brazil gets a home boost of .5 goals per game
    global BRAZIL_BOOST

    r[list_of_teams.index("Brazil")] = r[list_of_teams.index("Brazil")] + BRAZIL_BOOST
    return r

if __name__ == "__main__":
    ratings = get_best_ratings()
    teams = get_list_of_teams()
