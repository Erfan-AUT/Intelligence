from time import sleep


class Map:
    def __init__(self, n, m):
        self.cells = [["0" for _ in range(m)] for _ in range(n)]
        self.m = m
        self.n = n
        self.mario: Mario

    def add_item(self, lst, item):
        # Because the file is one-indexed
        x = self.n - lst[0]
        y = lst[1] - 1
        self.cells[x][y] = item
        if type(item) is Mario:
            self.mario = item

    def __getitem__(self, key):
        return self.cells[key]

    def print(self):
        for i in range(n):
            line_str = ""
            for j in range(m):
                if type(self.cells[i][j]) is Mario:
                    line_str += "M "
                else:
                    line_str += self.cells[i][j] + " "
            print(line_str)
        print()


class Mario:
    def __init__(self, k, x_y_list):
        # Is at least 1x1 because it allowed Mario to exist.
        self.remaining_blues = k
        self.remaining_reds = k
        self.x = n - x_y_list[0]
        self.y = x_y_list[1] - 1
        self.frontier = {}
        self.visited = {(self.x, self.y)}
        self.h_function = None

    def update_frontier(self, real_map):
        if self.y < real_map.m - 1:
            if (
                real_map[self.x][self.y + 1] != "c"
                and (self.x, self.y + 1) not in self.visited
            ):
                self.frontier.update(
                    {(self.x, self.y + 1): 1 + self.h_function(self.x, self.y + 1)}
                )
        if self.y > 0:
            if (
                real_map[self.x][self.y - 1] != "c"
                and (self.x, self.y - 1) not in self.visited
            ):
                self.frontier.update(
                    {(self.x, self.y - 1): 1 + self.h_function(self.x, self.y - 1)}
                )
        if self.x < real_map.n - 1:
            if (
                real_map[self.x + 1][self.y] != "c"
                and (self.x + 1, self.y) not in self.visited
            ):
                self.frontier.update(
                    {(self.x + 1, self.y): 1 + self.h_function(self.x + 1, self.y)}
                )
        if self.x > 0:
            if (
                real_map[self.x - 1][self.y] != "c"
                and (self.x - 1, self.y) not in self.visited
            ):
                self.frontier.update(
                    {(self.x - 1, self.y): 1 + self.h_function(self.x - 1, self.y)}
                )

        self.sort_frontier()
        return self.frontier.popitem()

    def reset_frontier_values(self, real_map):
        old_keys = self.frontier.keys()
        for key in old_keys:
            self.frontier.update({key: 1 + self.h_function(*key)})
        self.sort_frontier()

    def sort_frontier(self):
        self.frontier = {
            k: v
            for k, v in sorted(
                self.frontier.items(), key=lambda item: item[1], reverse=True
            )
        }


n, m, k = 0, 0, 0
game_map = None


def read_file():
    global n, m, k, game_map
    with open("Mario.txt", "r") as f:
        n = int(f.readline())
        m = int(f.readline())
        x_y = [int(x) for x in f.readline().split(" ")]
        k = int(f.readline())
        game_map = Map(n, m)
        # m for Mario
        game_map.add_item(x_y, Mario(k, x_y))
        for _ in range(k):
            # r for Red
            mush_xy = [int(x) for x in f.readline().split(" ")]
            game_map.add_item(mush_xy, "r")
        for _ in range(k):
            # b for Blue
            mush_xy = [int(x) for x in f.readline().split(" ")]
            game_map.add_item(mush_xy, "b")
        for line in f:
            try:
                # c for construction block: 🚧
                game_map.add_item([int(x) for x in f.readline().split(" ")], "c")
            except:
                pass


def is_mushroom(x, y):
    return game_map[x][y] == "r" or game_map[x][y] == "b"


def manhattan(x, i, y, j):
    return abs(x - i) + abs(y - j)


h_1 = lambda x, y: game_map.mario.remaining_reds + game_map.mario.remaining_blues
h_2 = lambda x, y: min(
    [
        manhattan(x, i, y, j) if is_mushroom(i, j) else float("inf")
        for j in range(m)
        for i in range(n)
    ]
)


def h_3(x, y):
    max_dis = 0
    for i in range(n):
        for j in range(m):
            for k in range(n):
                for l in range(m):
                    if (i != k or l != j) and is_mushroom(i, j) and is_mushroom(k, l):
                        dis = manhattan(i, k, j, l)
                        if dis > max_dis:
                            max_dis = dis
    return max_dis


def next_move(mario: Mario, h_function) -> (int, int):
    result = mario.update_frontier(game_map)
    mario.visited.add(result[0])
    return result[0]


read_file()


def print_state():
    print("The game's current map is: ")
    game_map.print()
    print("Mario's current frontier is: ")
    print(game_map.mario.frontier)
    print()


def main():
    steps = 0
    mario = game_map.mario
    mario.h_function = h_1
    while True:
        steps += 1
        print("Step " + str(steps) + ": ")
        print_state()
        new_x, new_y = next_move(mario, h_3)
        old_x, old_y = mario.x, mario.y
        mario.x = new_x
        mario.y = new_y
        if game_map[mario.x][mario.y] == "b":
            mario.reset_frontier_values(game_map)
            mario.remaining_blues -= 1
        elif game_map[mario.x][mario.y] == "r":
            mario.reset_frontier_values(game_map)
            mario.remaining_reds -= 1
        game_map[old_x][old_y] = "0"
        game_map[new_x][new_y] = mario
        if mario.remaining_blues < k and mario.remaining_reds < k:
            print_state()
            break
        # sleep(2)
    print("Number of steps taken: " + str(steps))


if __name__ == "__main__":
    main()
