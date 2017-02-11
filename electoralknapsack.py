import json


def getresults():
    with open('results.json') as f:
        return json.load(f)


def loststates(results):
    '''Return list of states lost by Democrats.'''
    return [state for state, result in results.items() if result['delta'] > 0]


def evslostwonreqd(results, total=538):
    '''Returns number of EVs lost, won and required by Democrats.'''
    lost = sum(result['evs'] for state, result in results.items()
               if state in loststates(results))
    won = total - lost
    reqd = total//2 + 1 - won
    return lost, won, reqd


def demtargets(results):
    '''
    Determine states to which one would need to relocate the smallest possible
    number of Democrats that change the 2016 electoral college winner (assuming
    no one changes their vote).

    Uses DP knapsack algorithm to solve a related problem (states GOP won by
    the most votes that GOP can retain while losing the election). Remaining
    2016 GOP states are those that would most efficiently change election
    outcome.

    See http://stackoverflow.com/a/7950524/409879.
    '''
    items = [(state, result['delta'], result['evs'])
             for state, result in results.items()
             if state in loststates(results)]
    lost, won, reqd = evslostwonreqd(results)
    gophold, _ = knapsack(items, lost - reqd)
    return [state for state in loststates(results)
            if state not in [s for (s, _, _) in gophold]]


def printresults(flips, results):
    fmt = 'Move {} Californians to {} for {} EVs'.format
    for f in flips:
        print(fmt(results[f]['delta'], f, results[f]['evs']))
    print('Total of {} people for {} EVs'.format(
        sum(results[f]['delta'] for f in flips),
        sum(results[f]['evs'] for f in flips)
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
