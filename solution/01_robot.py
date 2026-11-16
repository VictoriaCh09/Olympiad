import sys

def solve():
    sys.setrecursionlimit(10000)
    prog = sys.stdin.readline().strip()
    if not prog:
        return

    DIR = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def parse(s, i):
        nodes = []
        while i < len(s):
            c = s[i]
            if c == ')':
                break
            elif c == '(':
                nodes.append(('turn', c))
                i += 1
            elif c in 'FBLR':
                nodes.append(('move', c))
                i += 1
            elif c.isdigit():
                j = i
                while j < len(s) and s[j].isdigit():
                    j += 1
                count = int(s[i:j])
                body, j = parse(s, j + 1)
                nodes.append(('loop', count, body))
                i = j + 1
            else:
                i += 1
        return nodes, i

    tree, _ = parse(prog, 0)

    memo = {}

    def eval_subtree(nodes):
        node_id = id(nodes)
        if node_id in memo:
            return memo[node_id]

        results = []
        for start_d in range(4):
            x, y, d = 0, 0, start_d
            for node in nodes:
                if node[0] == 'move':
                    c = node[1]
                    if c == 'F':
                        dx, dy = DIR[d]
                        x += dx; y += dy
                    elif c == 'B':
                        dx, dy = DIR[d]
                        x -= dx; y -= dy
                    elif c == 'R':
                        dx, dy = DIR[(d + 1) % 4]
                        x += dx; y += dy
                    elif c == 'L':
                        dx, dy = DIR[(d - 1) % 4]
                        x += dx; y += dy
                elif node[0] == 'turn':
                    d = (d + 1) % 4 if node[1] == ')' else (d - 1) % 4
                elif node[0] == 'loop':
                    count, body = node[1], node[2]
                    body_res = eval_subtree(body)
                    
                    rot = (body_res[0][2] - 0) % 4
                    
                    if rot == 0:
                        dx, dy, fd = body_res[d]
                        x += count * dx
                        y += count * dy
                        d = fd
                    else:
                        cur_d = d
                        disps = []
                        for _ in range(4):
                            bdx, bdy, bfd = body_res[cur_d]
                            disps.append((bdx, bdy))
                            cur_d = bfd
                        
                        cycle_dx = sum(p[0] for p in disps)
                        cycle_dy = sum(p[1] for p in disps)
                        
                        q, r = divmod(count, 4)
                        x += q * cycle_dx
                        y += q * cycle_dy
                        
                        cur_d = d
                        for _ in range(r):
                            bdx, bdy, bfd = body_res[cur_d]
                            x += bdx
                            y += bdy
                            cur_d = bfd
                        d = cur_d
            results.append((x, y, d))
        
        memo[node_id] = results
        return results

    x, y, _ = eval_subtree(tree)[0]
    print(x, y)

if __name__ == '__main__':
    solve()