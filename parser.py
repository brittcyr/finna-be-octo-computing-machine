import numpy
from numpy import zeros
from numpy.linalg import inv


HOME_ADVANTAGE = 0

def using_game(home, away, home_goals, away_goals):
    return True

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

def get_number_of_teams():
    return len(get_list_of_teams())

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

if __name__ == "__main__":
    list_of_teams = get_list_of_teams()
    number_of_teams = len(list_of_teams)
    number_of_games = get_number_of_games()

    Xm = numpy.mat(numpy.array(get_x()))
    Ym = numpy.mat(numpy.array(get_y()))

    # r is the rankings from simple least squares
    r = numpy.linalg.pinv(Xm).dot(Ym.T)
    print r


