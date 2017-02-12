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


def evslostwonreqd(results, total=538):
    '''Returns number of EVs lost, won and required by Democrats.'''
    lost = sum(result['evs'] for state, result in results.items()
               if state in loststates(results))
    won = total - lost
    reqd = total//2 + 1 - won
    return lost, won, reqd


def findflips(results):
    '''
    Determine states to which one would need to relocate the smallest possible
    number of voters for the losing party to change the electoral college
    winner (assuming no one changes their vote).

    Uses DP knapsack algorithm to solve a related problem (states the actual
    winner won by the most votes they can retain while losing the election).
    Remaining winner's states are those that would most efficiently change
    election outcome.

    See http://stackoverflow.com/a/7950524/409879.
    '''
    winner, loser = winnerloser(results)
    items = [(state, result[winner] - result[loser] + 1, result['evs'])
             for state, result in results.items()
             if state in loststates(results)]
    lost, won, reqd = evslostwonreqd(results)
    hold, _ = knapsack(items, lost - reqd)
    flips = [state for state in loststates(results)
             if state not in [s for (s, _, _) in hold]]
    return flips


def printresults(flips, results):
    winner, loser = winnerloser(results)
    lstring = 'Democrats' if loser == 'dem' else 'Republicans'
    fvars = [(result[winner] - result[loser] + 1,
              lstring, state, result['evs'])
             for state, result in results.items() if state in flips]
    for fvar in fvars:
        print('Move {} {} to {} for {} EVs'.format(*fvar))
    print('Total of {} people for {} EVs'.format(
        sum(fvar[0] for fvar in fvars),
        sum(fvar[3] for fvar in fvars)
    ))


def knapsack(items, W):
    '''
    Solve knapsack problem for an iterable of items and knapsack capacity W.

    Return the maximum possible total value of items in a knapsack of capacity
    W, and the items selected.

    Each items is a (label, value, weight) triple.
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
