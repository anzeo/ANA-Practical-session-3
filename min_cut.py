import os
import random
import time

import networkx as nx


class UnionFind:
    parent = {}
    rank = {}

    def make_set(self, nodes):
        for n in nodes:
            self.parent[n] = n
            self.rank[n] = 0

    def find(self, k):
        if self.parent[k] != k:
            self.parent[k] = self.find(self.parent[k])
        return self.parent[k]

    def union(self, a, b):
        x_root = self.find(a)
        y_root = self.find(b)

        if x_root == y_root:
            return

        if self.rank[x_root] > self.rank[y_root]:
            self.parent[y_root] = x_root
        elif self.rank[x_root] < self.rank[y_root]:
            self.parent[x_root] = y_root
        else:
            self.parent[y_root] = x_root
            self.rank[x_root] += 1


def min_cut(G):
    union_find = UnionFind()
    union_find.make_set(G.nodes)

    permuted_edges = list(G.edges)
    random.shuffle(permuted_edges)

    n = 0
    while n < len(G.nodes) - 2:
        (u, v) = permuted_edges.pop()

        if union_find.find(u) != union_find.find(v):
            union_find.union(u, v)
            n += 1

    cut = set()

    for edge in permuted_edges:
        (u, v) = edge
        if union_find.find(u) != union_find.find(v):
            cut.add(edge)

    return cut


if __name__ == '__main__':
    directory = 'tests'
    REPEATS = 5  # število ponovitev iskanja optimalne rešitve
    # start = time.time()
    print("{:<15}|{:>15} |{:>11} |{:>11} ".format('name', '(n,m)', 'opt', 'avg. runs'))
    for filename in sorted(os.listdir(directory)):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            fo = open(f, "rb")
            G = nx.read_edgelist(fo, nodetype=int)
            n_m = len(G.nodes()), len(G.edges())

            if n_m[1] < 200000:
                # za manjše grafe, optimum poiščemo kar z networkX
                opt = len(nx.minimum_edge_cut(G))
            else:
                # za večje grafe, čim večkrat poženemo min_cut algoritem in iščemo najmanjšo velikost rešitve
                opt = n_m[1]
                for i in range(50):
                    opt = min(opt, len(min_cut(G)))

            avg_runs = 0
            for i in range(REPEATS):
                runs_counter = 0
                while True:
                    runs_counter += 1
                    if opt == len(min_cut(G)):
                        break
                avg_runs += runs_counter

            avg_runs /= REPEATS

            fo.close()
            print('{:<15}|{:>15} |{:>11} |{:>11} '.format(filename, str(n_m), opt, avg_runs))
    # end = time.time()
    # print(end - start)
