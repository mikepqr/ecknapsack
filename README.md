# The Electoral College and the knapsack problem

What is the smallest number of supporters of the losing party that could have
changed the outcome of a United States presidential election by relocating to
another state? And where should they have moved?

This code uses a dynamic programming knapsack solver to determine the
answer.

See [The Electoral College and the knapsack
problem](http://mike.place/2017/ecknapsack/) for more details.

```text
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

In [4]: for year in (2016, 2012, 2008, 2004, 2000, 1996, 1992, 1988, 1976):
          ...:     results = getresults(str(year) + '.json')
          ...:     flips = findflips(results)
          ...:     loser = 'Democrats' if winnerloser(results)[1] == 'dem' else 'Republicans'
          ...:     print("\n" + str(year))
          ...:     printresults(flips, loser=loser)
          ...:

2016
Move 10705 Democrats to MI for 16 EVs
Move 44293 Democrats to PA for 20 EVs
Move 22749 Democrats to WI for 10 EVs
Total of 77747 people for 46 EVs

2012
Move 74310 Republicans to FL for 29 EVs
Move 67807 Republicans to NV for 6 EVs
Move 39644 Republicans to NH for 4 EVs
Move 79548 Republicans to NM for 5 EVs
Move 166273 Republicans to OH for 18 EVs
Total of 427582 people for 62 EVs

2008
Move 236451 Republicans to FL for 27 EVs
Move 28392 Republicans to IN for 11 EVs
Move 146562 Republicans to IA for 7 EVs
Move 68293 Republicans to NH for 4 EVs
Move 14178 Republicans to NC for 15 EVs
Move 262225 Republicans to OH for 20 EVs
Move 234528 Republicans to VA for 13 EVs
Total of 990629 people for 97 EVs

2004
Move 99524 Democrats to CO for 9 EVs
Move 10060 Democrats to IA for 7 EVs
Move 5989 Democrats to NM for 5 EVs
Total of 115573 people for 21 EVs

2000
Move 538 Democrats to FL for 25 EVs
Total of 538 people for 25 EVs

1996
Move 31216 Republicans to Arizona for 8 EVs
Move 302335 Republicans to Florida for 25 EVs
Move 127615 Republicans to Iowa for 7 EVs
Move 13332 Republicans to Kentucky for 8 EVs
Move 135920 Republicans to Missouri for 11 EVs
Move 4731 Republicans to Nevada for 4 EVs
Move 49683 Republicans to New Hampshire for 4 EVs
Move 40745 Republicans to New Mexico for 5 EVs
Move 288340 Republicans to Ohio for 21 EVs
Move 111490 Republicans to Oregon for 7 EVs
Move 45617 Republicans to Tennessee for 11 EVs
Total of 1151024 people for 111 EVs

1992
Move 66832 Republicans to Colorado for 8 EVs
Move 23742 Republicans to Delaware for 3 EVs
Move 13715 Republicans to Georgia for 13 EVs
Move 42489 Republicans to Hawaii for 4 EVs
Move 47927 Republicans to Kentucky for 8 EVs
Move 82586 Republicans to Louisiana for 9 EVs
Move 10301 Republicans to Montana for 3 EVs
Move 13321 Republicans to Nevada for 4 EVs
Move 6557 Republicans to New Hampshire for 4 EVs
Move 79342 Republicans to New Jersey for 15 EVs
Move 90633 Republicans to Ohio for 21 EVs
Move 92222 Republicans to Tennessee for 11 EVs
Total of 569667 people for 103 EVs

1988
Move 352685 Democrats to California for 47 EVs
Move 106725 Democrats to Colorado for 8 EVs
Move 73658 Democrats to Connecticut for 8 EVs
Move 30993 Democrats to Delaware for 3 EVs
Move 95000 Democrats to Illinois for 24 EVs
Move 63563 Democrats to Maine for 4 EVs
Move 49864 Democrats to Maryland for 10 EVs
Move 83335 Democrats to Missouri for 11 EVs
Move 21477 Democrats to Montana for 4 EVs
Move 25845 Democrats to New Mexico for 5 EVs
Move 38821 Democrats to North Dakota for 3 EVs
Move 105144 Democrats to Pennsylvania for 25 EVs
Move 19856 Democrats to South Dakota for 3 EVs
Move 8557 Democrats to Vermont for 3 EVs
Total of 1075523 people for 158 EVs
```
