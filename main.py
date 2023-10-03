from random import shuffle
from copy import deepcopy


class Node:
    def __init__(self, table, parent, depth=1):
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.depth = depth
        self.table = table
        self.parent = parent

    def path(self):
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent
        return path

    def actions(self):
        b = []

        for row in self.table:
            for i in row:
                if i == "B":
                    b = [self.table.index(row), row.index(i)]

        if b[1] != len(self.table) - 1:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[b[0]][(b[1] + 1)]
            new_table[b[0]][(b[1] + 1)] = "B"
            self.right = Node(new_table, self, self.depth + 1)

        if b[1] != 0:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[b[0]][(b[1] - 1)]
            new_table[b[0]][(b[1] - 1)] = "B"
            self.left = Node(new_table, self, self.depth + 1)

        if b[0] != 0:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[(b[0] - 1)][b[1]]
            new_table[(b[0] - 1)][b[1]] = "B"
            self.up = Node(new_table, self, self.depth + 1)

        if b[0] != len(self.table[0]) - 1:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[(b[0] + 1)][b[1]]
            new_table[(b[0] + 1)][b[1]] = "B"
            self.down = Node(new_table, self, self.depth + 1)


def table_gen(n, m, random=True):
    temp = []
    node = []
    index = 0
    for i in range(1, m * n + 1):
        temp.append(i)
        if i == m * n:
            temp[-1] = "B"

    if random:
        shuffle(temp)

    for i in range(n):
        inside_node = []
        for j in range(m):
            inside_node.append(temp[index])
            index += 1
        node.append(inside_node)
    return node


def ciferny_maximum(number):
    cif_max = 0
    try:
        while 10 ** cif_max <= number:
            cif_max += 1
        return cif_max
    except TypeError:
        return 1


def print_node(node):
    n = len(node.table)
    m = len(node.table[0])
    cif_max = ciferny_maximum(n * m)

    for i in range(n):
        print((("-" * (5 + cif_max)) * m) + "-")
        print((("|" + " " * (5 + cif_max - 1)) * m) + "|")
        for j in range(m):
            cif_local = ciferny_maximum(node.table[i][j])
            print(("|  " + str(node.table[i][j])) + " " * (2 + cif_max - cif_local), end="")
        print("|")
        print((("|" + " " * (5 + cif_max - 1)) * m) + "|")
    print((("_" * (5 + cif_max)) * m) + "_")


stav = Node(table_gen(3, 3), None)
final_stav = Node(table_gen(3, 3, False), None)

print_node(stav)
stav.actions()
final_stav.actions()

print(1)