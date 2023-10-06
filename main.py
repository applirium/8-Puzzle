from random import shuffle
from copy import deepcopy
from time import time
import pandas


class Node:
    def __init__(self, table, parent, last):        # Initialize a node with table configuration,
        self.right = None                           # parent node, and last move direction.
        self.left = None                            # Set up, down, left, and right pointers to other nodes.
        self.up = None
        self.down = None
        self.last = last
        self.table = table
        self.parent = parent

    def path(self, reverse=False):                  # Return a list representing the path from the root to this node.
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent

        if not reverse:
            return path[::-1]

        return path

    def actions(self):                              # Generate possible moves based on the current configuration.
        b = []

        for row in self.table:
            for i in row:
                if i == "B":
                    b = [self.table.index(row), row.index(i)]

        if b[1] != len(self.table[0]) - 1:          # Create a new node for the right move
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[b[0]][(b[1] + 1)]
            new_table[b[0]][(b[1] + 1)] = "B"
            if not self.last == "LEFT" or self.last is None:
                self.right = Node(new_table, self, "RIGHT")

        if b[1] != 0:                               # Create a new node for the left move
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[b[0]][(b[1] - 1)]
            new_table[b[0]][(b[1] - 1)] = "B"
            if not self.last == "RIGHT" or self.last is None:
                self.left = Node(new_table, self, "LEFT")

        if b[0] != 0:                               # Create a new node for the up move
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[(b[0] - 1)][b[1]]
            new_table[(b[0] - 1)][b[1]] = "B"
            if not self.last == "DOWN" or self.last is None:
                self.up = Node(new_table, self, "UP")

        if b[0] != len(self.table) - 1:             # Create a new node for the down move
            new_table = deepcopy(self.table)
            new_table[b[0]][b[1]] = new_table[(b[0] + 1)][b[1]]
            new_table[(b[0] + 1)][b[1]] = "B"
            if not self.last == "UP" or self.last is None:
                self.down = Node(new_table, self, "DOWN")


def solvable(puzzle):                               # Determine if 3x3 puzzle is solvable by counting inversions.
    inversions = 0
    flattened = [num for row in puzzle for num in row if num != "B"]
    for i in range(len(flattened)):
        for j in range(i+1, len(flattened)):
            if flattened[i] > flattened[j]:
                inversions += 1
    return inversions % 2 == 0


def table_gen(n=3, m=3, random=True):               # Generate a random or ordered table for the puzzle.
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


def print_node(node):                               # Print the node in a formatted manner.
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


def addon(node, object_queue, object_visited):      # Add valid child nodes to the queue for further exploration.
    if node.left is None and node.right is None and node.up is None and node.down is None:
        node.actions()

    for obj in [node.right, node.left, node.up, node.down]:
        if obj is not None:
            object_queue.append(obj)

    object_visited.add(node)


def bidirectional_search(start, final):             # Perform bidirectional search to find a solution.
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


def one_iteration():
    while True:
        generated_table = table_gen()
        if solvable(generated_table):                   # Generate a solvable puzzle and create start and end states.

            first_state = Node(generated_table, None, None)
            end_state = Node(table_gen(random=False), None, None)

            start_time = time()                         # Measure execution time and find the solution path.
            ui_path, iterations = bidirectional_search(first_state, end_state)
            end_time = time()

            return [ui_path, iterations, round(end_time - start_time,3), len(ui_path) - 1]


def avg(lst, index, num):                               # Calculate average of a specific index in a list of lists.
    temp = 0
    for i in lst:
        temp += i[index]

    return temp/num


def test(number):                                       # Run tests and save results to an Excel file.
    results = []
    for i in range(number):
        results.append(one_iteration())
    df = pandas.DataFrame(results, columns=["object","iterations", "time", "path length"])
    df.to_excel('xls/list.xlsx', index=False)

    print("Write help to get list of commands")
    while True:
        decision = input("Action: ").lower()
        if decision == "average":
            print(f"Average iterations: {int(avg(results,1,number))}")
            print(f"Average time of execution: {round(avg(results,2,number),2)}")
            print(f"Average length of path: {round(avg(results,3,number),2)}")

        elif decision == "path":
            decision_number = 0
            while True:
                try:
                    decision_number = int(input("Number of test: "))
                except ValueError:
                    print("Enter integer")
                    continue

                if number > decision_number > -1:
                    break

                print("Enter integer in range of test")

            for turn in results[decision_number][0]:
                print_node(turn)

            print(f"Iterations: {results[decision_number][1]}")
            print(f"Time of execution: {results[decision_number][2]}")
            print(f"Length of path: {results[decision_number][3]}")

        elif decision == "help":
            print("average returns statistics of all paths")
            print("path returns solution of puzzle with statistics")
            print("exit will end the program")

        elif decision == "exit":
            break

        else:
            print("Wrong input")


test(1000)
