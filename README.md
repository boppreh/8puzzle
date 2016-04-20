# 8puzzle

Python solution to sliding 8-puzzle. We start with the final state

    123
    804
    765

and compute all states reachable by it, depth-first. The resulting table has ~180,000 entries and is saved to a file (`table.pkl`) for faster queries. The table takes about 6 seconds to be built and persisten on my machine, and subsequent queries are practically instantaneous. The worst case requires 30 steps to solve.
