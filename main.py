from random import shuffle
from copy import deepcopy
from time import time


class Node:
    def __init__(self, table, parent, last):
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.last = last
        self.table = table
        self.parent = parent

    def path(self, reverse=False):
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent

        if not reverse:
            return path[::-1]

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
            if not self.last == "LEFT" or self.last is None:
                self.right = Node(new_table, self, "RIGHT")

        if b[1] != 0:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[b[0]][(b[1] - 1)]
            new_table[b[0]][(b[1] - 1)] = "B"
            if not self.last == "RIGHT" or self.last is None:
                self.left = Node(new_table, self, "LEFT")

        if b[0] != 0:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[(b[0] - 1)][b[1]]
            new_table[(b[0] - 1)][b[1]] = "B"
            if not self.last == "DOWN" or self.last is None:
                self.up = Node(new_table, self, "UP")

        if b[0] != len(self.table[0]) - 1:
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[(b[0] + 1)][b[1]]
            new_table[(b[0] + 1)][b[1]] = "B"
            if not self.last == "UP" or self.last is None:
                self.down = Node(new_table, self, "DOWN")


def solvable(puzzle):
    inversions = 0
    flattened = [num for row in puzzle for num in row if num != "B"]
    for i in range(len(flattened)):
        for j in range(i+1, len(flattened)):
            if flattened[i] > flattened[j]:
                inversions += 1
    if len(puzzle[0]) % 2 == 1:  # Odd width
        return inversions % 2 == 0
    else:  # Even width
        blank_row = len(puzzle) - puzzle.index([0]*len(puzzle[0])) - 1
        return (inversions + blank_row) % 2 == 0


def table_gen(n=3, m=3, random=True):
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


def print_node(node):
    def ciferny_maximum(number):
        cif = 0
        try:
            while 10 ** cif <= number:
                cif += 1
            return cif
        except TypeError:
            return 1

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


def addon(node, object_queue, object_visited):
    if node.left is None and node.right is None and node.up is None and node.down is None:
        node.actions()

    for obj in [node.right, node.left, node.up, node.down]:
        if obj is not None:
            object_queue.append(obj)

    object_visited.add(node)


def bidirectional_search(start, final):
    forward_queue = []
    backward_queue = []
    forward_visited = set()
    backward_visited = set()

    forward_queue.append(start)
    backward_queue.append(final)

    iteration = 2
    while not len(forward_queue) == 0 and not len(backward_queue) == 0:
        forward_current = forward_queue.pop(0)
        backward_current = backward_queue.pop(0)

        for state in backward_visited:
            if state.table == forward_current.table:
                return forward_current.path()[:-1] + state.path(True), iteration

        for state in forward_visited:
            if state.table == backward_current.table:
                return state.path()[:-1] + backward_current.path(True), iteration

        addon(forward_current, forward_queue, forward_visited)
        addon(backward_current, backward_queue, backward_visited)
        iteration += 2


while True:
    generated_table = table_gen()
    if solvable(generated_table):

        first_state = Node(generated_table, None, None)
        end_state = Node(table_gen(random=False), None, None)

        start_time = time()
        ui_path, iterations = bidirectional_search(first_state, end_state)
        end_time = time()

        for turn in ui_path:
            print_node(turn)

        print(f"Iterations: {iterations}")
        print(f"Time of execution: {end_time - start_time}")
        print(f"Length of path: {len(ui_path) - 1}")
        break
