import json
import pandas as pd
import os


def csv2json(csvpath):
    head, ext = os.path.splitext(csvpath)
    results = pd.read_csv(csvpath, index_col=0)
    results.to_json(head + '.json', orient='index')


def getresults(jsonpath):
    with open(jsonpath) as f:
        return json.load(f)


def winnerloser(results):
    '''Return ('gop', 'dem') if GOP won, else return ('dem', 'gop').'''
    demevs = sum(result['evs'] for state, result in results.items()
                 if result['dem'] - result['gop'] > 0)
    gopevs = sum(result['evs'] for state, result in results.items()
                 if result['gop'] - result['dem'] > 0)
    return ('gop', 'dem') if gopevs > demevs else ('dem', 'gop')


def loststates(results):
    '''Return list of states lost by loser.'''
    winner, loser = winnerloser(results)
    return [state for state, result in results.items()
            if result[winner] > result[loser]]


def evsreqd(results, total=538):
    '''Returns number of EVs lost, won and required by Democrats.'''
    lost = sum(result['evs'] for state, result in results.items()
               if state in loststates(results))
    won = total - lost
    reqd = total//2 + 1 - won
    return reqd


def findflips(results):
    '''
    Determine states to which one would need to relocate the smallest possible
    number of voters for the losing party to change the electoral college
    winner (assuming no one changes their vote).
    '''
    winner, loser = winnerloser(results)
    items = [(state, result[winner] - result[loser] + 1, result['evs'])
             for state, result in results.items()
             if state in loststates(results)]
    flips, _ = complementaryknapsack(items, evsreqd(results))
    return flips


def printresults(flips, loser='Democrats'):
    for flip in flips:
        print('Move {} {} to {} for {} EVs'.format(
            flip[1], loser, flip[0], flip[2]))
    print('Total of {} people for {} EVs'.format(
        sum(flip[1] for flip in flips),
        sum(flip[2] for flip in flips)
    ))


def complementaryknapsack(items, W):
    '''
    Solve complementary knapsack problem for an iterable of items and knapsack
    capacity W. Each item is a (label, value, weight) triple.

    Returns the items selected and their total value.

    The complementary knapsack selection is the subset of items that minimizes
    the total value of the knapsack while exceeding its capacity.

    See http://stackoverflow.com/a/7950524/409879.
    '''
    Wtot = sum(weight for label, value, weight in items)
    picks, _ = knapsack(items, Wtot - W)
    complement = [(label, value, weight) for label, value, weight in items
                  if label not in [labelp for labelp, _, _ in picks]]
    complementvalue = sum(value for label, value, weight in complement)
    return complement, complementvalue


def knapsack(items, W):
    '''
    Solve knapsack problem for an iterable of items and knapsack capacity W.
    Each item is a (label, value, weight) triple.

    Returns the items selected and their total value.

    The knapsack selection is the subset of items that maximizes the total
    value of the knapsack without exceeding its capacity.
    '''
    items = list(items)
    n = len(items)
    # A[i, x] stores the solution to the optimal knapsack problem for items
    # 1..i inclusive, given a knapsack of capacity x. The items are labelled 1
    # to n, but A also stores optimal values for the empty set of items (i = 0)
    # and a zero capacity knapsack (W = 0), which are of course all zero.
    A = [[0] * (W+1) for _ in range(n+1)]

    # Populate the array A from bottom up
    for i in range(1, n+1):
        # The value and weight of the ith item in items (-1 handles Python's
        # 0-indexed arrays).
        vi = items[i-1][1]
        wi = items[i-1][2]

        for x in range(0, W+1):
            if wi <= x:
                A[i][x] = max(A[i-1][x], A[i-1][x-wi] + vi)
            else:
                A[i][x] = A[i-1][x]

    w = W
    picks = []
    for j in range(n, 0, -1):
        if (A[j][w] != A[j-1][w]):
            w -= items[j-1][2]
            picks.append(items[j-1])

    return picks, A[n][W]
