# import matplotlib.pyplot as plt
import random

# import networkx as nx
from graphviz import Digraph

# Define GameState constants
OK = 1
WON = 2
LOST = 3


class Fly:
    def __init__(self, board: list = None, verbose=False):
        self.board = [2, 2, 2, 2] if board is None else list(board)
        self._state = None
        self.verbose = verbose

    def explore(self, index):
        new_board = self.board[:]
        if Fly.check_board(new_board) != OK:
            raise ValueError("Game is already over")

        if index < 0 or index > 3:
            raise ValueError("Index must be between 0 and 3")

        new_board[index] += 1

        # Check for contiguous equal values and set them to 0 only if the move concerns one of them
        if index > 0 and new_board[index] == new_board[index - 1]:
            new_board[index] = 0
            new_board[index - 1] = 0
        if index < 3 and new_board[index] == new_board[index + 1]:
            new_board[index] = 0
            new_board[index + 1] = 0

        return new_board, Fly.check_board(new_board)

    def play(self, index):
        self.board, self._state = self.explore(index)

    def is_lost(self):
        return any(value == 5 for value in self.board)

    def is_won(self):
        return all(value == 0 for value in self.board)

    def get_board(self):
        return self.board

    @property
    def state(self):
        if self.is_won():
            self._state = WON
        elif self.is_lost():
            self._state = LOST
        else:
            self._state = OK
        return self._state

    @staticmethod
    def check_board(board: list):
        if all(value == 0 for value in board):
            return WON
        elif any(value == 5 for value in board):
            return LOST
        else:
            return OK


def run(fly: Fly) -> None:
    moves = 0
    while fly.state == OK and moves < 100:
        index = random.randint(0, 3)
        try:
            fly.play(index)
        except ValueError as e:
            print(e)
        moves += 1
    print(f"Game ended after {moves} moves.")
    print(f"Final board: {fly.get_board()}")
    print(f"Game state: {fly.state}")


def brute_force(max_paths: int, max_depth: int, verbose: bool = False) -> list:
    chemins = []

    def dfs(fly: Fly, path: list, depth: int) -> bool:
        if len(chemins) >= max_paths or depth > max_depth:
            return False
        if fly.state != OK:
            if fly.state == WON or fly.state == LOST:
                path_result = "won" if fly.state == WON else "fail"
                chemins.append((path[:], path_result))
                if verbose:
                    print(f"Path when {path_result}: {[move[0] for move in path]}")
            return fly.state == WON

        for i in range(4):
            new_fly = Fly(verbose=False)
            new_fly.board = fly.board[:]
            new_fly.state = fly.state
            new_fly.play(i)
            path.append((i, new_fly.board[:]))
            dfs(new_fly, path, depth + 1)
            path.pop()
        return False

    fly = Fly(verbose=verbose)
    if dfs(fly, [], 0):
        print("Found a winning sequence within the path limit.")
    else:
        print("No winning sequence found within the path limit.")

    return chemins


def build_graph(chemins):
    dot = Digraph()
    for path, result in chemins:
        for i in range(len(path) - 1):
            move, board = path[i]
            next_move, next_board = path[i + 1]
            dot.node(str(board), str(board))
            dot.node(str(next_board), str(next_board))
            dot.edge(str(board), str(next_board), label=str(move))
    return dot


def visualize_graph(graph, chemins):
    graph.attr("node", shape="circle")
    for path, result in chemins:
        color = "blue" if result == "won" else "red"
        for move, board in path:
            graph.node(str(board), style="filled", fillcolor=color)
    graph.view()


if __name__ == "__main__":
    chemins = brute_force(100, 10, verbose=True)
    graph = build_graph(chemins)
    visualize_graph(graph, chemins)
