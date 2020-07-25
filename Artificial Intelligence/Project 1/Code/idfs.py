import re, copy


class Person:
    def __init__(self, height: int, row: str):
        self.height = height
        self.row = row


class Jafar:
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y


class Node:
    def __init__(
        self,
        iteration: list,
        jafar: Jafar,
        depth: int = 0,
        last_move: str = None,
        parent=None,
    ):
        self.iteration = iteration
        self.jafar = jafar
        self.parent = parent
        self.last_move = last_move
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0


m, n = 0, 0


def read_input():
    grid = []
    location = None
    with open("twomove.txt", "r") as f:
        global m, n
        n, m = (int(x) for x in f.readline().split(" ") if x != "\n")
        split_str = "[0-9]+"
        for i in range(n):
            row = []
            raw_row = f.readline()[:-1].split(" ")[:m]
            for index, item in enumerate(raw_row):
                if item != "#":
                    x = re.split(split_str, item)
                    row.append(Person(int(item[: item.find(x[1])]), x[1]))
                else:
                    row.append(Person(float("inf"), "#"))
                    location = Jafar(index, i)
            grid.append(row)
    start = Node(grid, location)
    return start


def same_as_grandparent(parent: Node, current: list):
    if parent.parent != None:
        grand_iter = parent.parent.iteration
        for i in range(n):
            for j in range(m):
                if (
                    grand_iter[i][j].height != current[i][j].height
                    or grand_iter[i][j].row != current[i][j].row
                ):
                    return False
        return True

    return False


def move(node: Node, deltaX, deltaY, child_nodes: list, move_str):
    X, Y = node.jafar.X, node.jafar.Y
    new_iter = copy.deepcopy(node.iteration)
    new_iter[Y + deltaY][X + deltaX], new_iter[Y][X] = (
        new_iter[Y][X],
        new_iter[Y + deltaY][X + deltaX],
    )
    if not same_as_grandparent(node, new_iter):
        child_nodes.append(
            Node(
                new_iter, Jafar(X + deltaX, Y + deltaY), last_move=move_str, parent=node
            )
        )


def generate_children(node: Node):
    child_nodes = []
    X, Y = node.jafar.X, node.jafar.Y
    if Y < n - 1:
        move(node, 0, 1, child_nodes, "up")
    if Y > 0:
        move(node, 0, -1, child_nodes, "down")
    if X < m - 1:
        move(node, 1, 0, child_nodes, "right")
    if X > 0:
        move(node, -1, 0, child_nodes, "left")

    return child_nodes


def check_goal(node: Node):
    it = node.iteration
    in_order = all(
        it[i][j].height > it[i][j + 1].height for i in range(n) for j in range(m - 1)
    )
    in_row = all(
        it[i][j].row == chr(i + 97) or it[i][j].row == "#"
        for i in range(n)
        for j in range(m)
    )
    return node.jafar.X == 0 and in_order and in_row


def new_level(list_of_nodes):
    next = []
    for node in list_of_nodes:
        next += generate_children(node)
    return next


def print_iteration(node: Node):
    it = node.iteration
    for i in range(n):
        print_str = ""
        for j in range(m):
            if it[i][j].row == "#":
                print_str += "# "
            else:
                print_str += str(it[i][j].height) + it[i][j].row + " "
        print(print_str)
    if node.last_move:
        print(node.last_move)
    print()


def dls(node, depth):
    if depth == 0:
        if check_goal(node):
            return node, True
        else:
            return None, True
    elif depth > 0:
        any_remaining = False
        for child in generate_children(node):
            found, remaining = dls(child, depth - 1)
            if found:
                return found, True
            if remaining:
                any_remaining = True
        return None, any_remaining


def idfs(root: Node, base_levels: int = 0):
    for depth in range(base_levels, 1000):
        found, remaining = dls(root, depth)
        if found:
            return found
        elif not remaining:
            return None


def print_result(result: Node):
    if result:
        print("depth: " + str(result.depth))
        while result.parent:
            print_iteration(result)
            result = result.parent
    else:
        print("NO ANSWER FOUND")

def print_result_forwards(result: Node):
    if result:
        print("Depth: " + str(result.depth))
        nodes_list = []
        while result.parent:
            nodes_list.insert(0, result)
            result = result.parent
        nodes_list.insert(0, result)
        for node in nodes_list:
            print_iteration(node)
    else:
        print("NO ANSWER FOUND")

def main():
    root = read_input()
    result = idfs(root, 0)

    print_result_forwards(result)


if __name__ == "__main__":
    main()
