# The Electoral College and the knapsack problem

What is the smallest number of Democrats that could change the outcome of a
United States presidential election by relocating to another state? And where
should they move?

This code uses the a dynamic programming knapsack solver to determine the
answer.

See [The Electoral College and the knapsack
problem](http://mike.place/2017/electoralknapsack/) for more details.

```python
In [1]: results = getresults('2016.json')

In [2]: results
Out[2]:
{'AK': {'dem': 116454, 'evs': 3, 'gop': 163387},
 'AL': {'dem': 729547, 'evs': 9, 'gop': 1318255},
 'AR': {'dem': 380494, 'evs': 6, 'gop': 684872},
 'AZ': {'dem': 1161167, 'evs': 11, 'gop': 1252401},
 ...
 'WA': {'dem': 1742718, 'evs': 12, 'gop': 1221747},
 'WI': {'dem': 1382536, 'evs': 10, 'gop': 1405284},
 'WV': {'dem': 188794, 'evs': 5, 'gop': 489371},
 'WY': {'dem': 55973, 'evs': 3, 'gop': 174419}}

In [3]: findflips(results)
Out[3]: [('WI', 22749, 10), ('PA', 44293, 20), ('MI', 10705, 16)]

In [4]: for year in (2000, 2004, 2008, 2012, 2016):
   ...:     results = getresults(str(year) + '.json')
   ...:     flips = findflips(results)
   ...:     loser = 'Democrats' if winnerloser(results)[1] == 'dem' else 'Republicans'
   ...:     print(" - - " + str(year))
   ...:     printresults(flips, loser=loser)
   ...:
 - - 2000
Move 538 Democrats to FL for 25 EVs
Total of 538 people for 25 EVs
 - - 2004
Move 10060 Democrats to IA for 7 EVs
Move 5989 Democrats to NM for 5 EVs
Move 99524 Democrats to CO for 9 EVs
Total of 115573 people for 21 EVs
 - - 2008
Move 68293 Republicans to NH for 4 EVs
Move 28392 Republicans to IN for 11 EVs
Move 146562 Republicans to IA for 7 EVs
Move 234528 Republicans to VA for 13 EVs
Move 262225 Republicans to OH for 20 EVs
Move 14178 Republicans to NC for 15 EVs
Move 236451 Republicans to FL for 27 EVs
Total of 990629 people for 97 EVs
 - - 2012
Move 39644 Republicans to NH for 4 EVs
Move 166273 Republicans to OH for 18 EVs
Move 67807 Republicans to NV for 6 EVs
Move 79548 Republicans to NM for 5 EVs
Move 74310 Republicans to FL for 29 EVs
Total of 427582 people for 62 EVs
 - - 2016
Move 22749 Democrats to WI for 10 EVs
Move 44293 Democrats to PA for 20 EVs
Move 10705 Democrats to MI for 16 EVs
Total of 77747 people for 46 EVs
```
