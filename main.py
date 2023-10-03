class Node:
    def __init__(self, table, parent):
        self.right = None
        self.left = None
        self.up = None
        self.down = None
        self.depth = 1
        self.table = table
        self.parent = parent

    def path(self):
        path = []
        node = self
        while node is not None:
            path.append(node)
            node = node.parent
        return path

    def right(self):
        new_node = Node(self, self.depth)
        return new_node

    def left(self):
        new_node = Node(self, self.depth)
        return new_node

    def up(self):
        new_node = Node(self, self.depth)
        if "B" not in self.table[0]:
            print(1)

        return new_node

    def down(self):
        new_node = Node(self, self.depth)
        return new_node


def table_gen(n, m):
    node = []
    index = 1
    for i in range(n):
        inside_node = []
        for j in range(m):
            inside_node.append(index)
            index += 1
        node.append(inside_node)
    node[-1][-1] = "B"
    return node


def ciferny_maximum(number):
    cif_max = 0
    try:
        while 10 ** cif_max <= number:
            cif_max += 1
        return cif_max
    except TypeError:
        return 1


def print_node(node, scale):
    n = len(node.table)
    m = len(node.table[0])
    cif_max = ciferny_maximum(n*m)

    for i in range(n):
        print((("-" * (scale + cif_max)) * m) + "-")
        print((("|" + " " * (scale + cif_max - 1)) * m) + "|")
        for j in range(m):
            cif_local = ciferny_maximum(node.table[i][j])
            print(("|" + " " * (scale // 2) + str(node.table[i][j])) + " " * (scale // 2 + cif_max - cif_local), end="")
        print("|")
        print((("|" + " " * (scale + cif_max - 1)) * m) + "|")
    print((("_" * (scale + cif_max)) * m) + "_")


stav = Node(table_gen(3, 3), None)
print(stav.table)
print_node(stav, 5)
