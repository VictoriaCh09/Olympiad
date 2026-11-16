import sys

def solve():
    input_data = """8
1 2
5
2 2
5 5
1 3
10
2 2
5 6
1 3
4
2 2
3 4
3 2
5 5 6
3 2
7 7 7
"""
    data = input_data.split()
    it = iter(data)
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it)); k = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        maxm = max(arr)
        g = [0]*(maxm+1)
        for m in range(1, maxm+1):
            seen = set()
            lo = (m + k) // (k+1)
            if lo < 1: lo = 1
            hi = (m-1)//2
            for b in range(lo, hi+1):
                a = m - b
                seen.add(g[b] ^ g[a])
            mex = 0
            while mex in seen: mex += 1
            g[m] = mex
        X = 0
        for v in arr: X ^= g[v]
        if X == 0:
            out.append("Lose 0")
            continue
        uniq_m = set(arr)
        wins = set()
        for m in uniq_m:
            target = X ^ g[m]
            lo = (m + k)//(k+1)
            if lo < 1: lo = 1
            hi = (m-1)//2
            for b in range(lo, hi+1):
                a = m - b
                if (g[b] ^ g[a]) == target:
                    wins.add((m, b))
        out.append(f"Win {len(wins)}")
    print("\n".join(out))

solve()