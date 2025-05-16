import os
import time

def animate_knight_tour(board, delay=0.15, use_unicode=True):
    symbol = "🐴 " if use_unicode else " K "
    files = "abcdefgh"
    
    # Build a lookup table of positions by move number
    move_positions = [None] * (BOARD_SIZE * BOARD_SIZE)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            move = board[y][x]
            move_positions[move] = (x, y)

    for current_move in range(BOARD_SIZE * BOARD_SIZE):
        os.system('clear' if os.name == 'posix' else 'cls')

        print("   " + "  ".join(f" {f}" for f in files))
        print("  +" + "---+" * BOARD_SIZE)
        for y in range(BOARD_SIZE):
            row_str = f"{8 - y} |"
            for x in range(BOARD_SIZE):
                move = board[y][x]
                if move == current_move:
                    row_str += f"{symbol}|"
                elif move < current_move:
                    row_str += f"{move:02} |"
                else:
                    row_str += "   |"
            print(row_str + f" {8 - y}")
            print("  +" + "---+" * BOARD_SIZE)
        print("   " + "  ".join(f" {f}" for f in files))
        print(f"\nMove: {current_move:02}/63")
        time.sleep(delay)

BOARD_SIZE = 8
MOVES = [
    (-2, -1), (-1, -2), (1, -2), (2, -1),
    (2, 1),  (1, 2),  (-1, 2), (-2, 1)
]

def is_valid(x, y, board):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and board[y][x] == -1

def count_onward_moves(x, y, board):
    return sum(
        1 for dx, dy in MOVES
        if is_valid(x + dx, y + dy, board)
    )

def warnsdorff_tour(x, y):
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[y][x] = 0
    pos = (x, y)

    for move in range(1, BOARD_SIZE * BOARD_SIZE):
        x, y = pos
        next_moves = []
        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, board):
                onward = count_onward_moves(nx, ny, board)
                next_moves.append((onward, nx, ny))
        if not next_moves:
            return None
        _, nx, ny = min(next_moves)
        board[ny][nx] = move
        pos = (nx, ny)
    return board

def backtrack_tour(x, y):
    board = [[-1 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    board[y][x] = 0
    solutions = []
    def dfs(cx, cy, move):
        if move == BOARD_SIZE * BOARD_SIZE:
            return True
        next_moves = []
        for dx, dy in MOVES:
            nx, ny = cx + dx, cy + dy
            if is_valid(nx, ny, board):
                next_moves.append((nx, ny))
        # Optionally sort for Warnsdorff-style guidance
        next_moves.sort(key=lambda pos: count_onward_moves(pos[0], pos[1], board))
        for nx, ny in next_moves:
            board[ny][nx] = move
            if dfs(nx, ny, move + 1):
                return True
            board[ny][nx] = -1
        return False

    if dfs(x, y, 1):
        return board
    return None


def find_knight_tour(x, y):
    result = warnsdorff_tour(x, y)
    if result:
        return result
    print(f"⚠️ Warnsdorff's heuristic failed from {chr(x + ord('a'))}{8 - y}, falling back to backtracking...")
    return backtrack_tour(x, y)


def print_ascii_board(board):
    files = "abcdefgh"
    # Column labels (aligned)
    print("   " + "  ".join(f" {f}" for f in files))
    print("  +" + "---+" * BOARD_SIZE)

    for y in range(BOARD_SIZE):
        row_str = f"{8 - y} |"
        for x in range(BOARD_SIZE):
            row_str += f"{board[y][x]:02} |"
        print(row_str + f" {8 - y}")
        print("  +" + "---+" * BOARD_SIZE)

    print("   " + "  ".join(f" {f}" for f in files))

def parse_chess_square(square):
    if len(square) != 2:
        return None
    file, rank = square[0], square[1]
    if file not in "abcdefgh" or rank not in "12345678":
        return None
    x = ord(file) - ord('a')
    y = 8 - int(rank)
    return x, y

def validate_tour(board, verbose=True):
    positions = [None] * (BOARD_SIZE * BOARD_SIZE)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            move = board[y][x]
            if not (0 <= move < BOARD_SIZE * BOARD_SIZE):
                if verbose:
                    print(f"Invalid move number {move} at ({x}, {y})")
                return False
            if positions[move] is not None:
                if verbose:
                    print(f"Duplicate move number {move} found")
                return False
            positions[move] = (x, y)

    for i in range(1, BOARD_SIZE * BOARD_SIZE):
        x1, y1 = positions[i - 1]
        x2, y2 = positions[i]
        dx, dy = abs(x1 - x2), abs(y1 - y2)
        if not ((dx == 1 and dy == 2) or (dx == 2 and dy == 1)):
            if verbose:
                print(f"Invalid knight move from {positions[i - 1]} to {positions[i]}")
            return False
    if verbose:
        print("✅ Tour is valid.")
    return True

def test_all_start_positions():
    for rank in range(8):
        for file in range(8):
            #result = warnsdorff_tour(file, rank)
            result = find_knight_tour(file, rank)

            if not result:
                print(f"⚠️ Failed from {chr(file + ord('a'))}{8 - rank}")


def main():
    print("Knight's Tour - Warnsdorff's Heuristic")

    test_all_start_positions()

    square = input("Enter starting square (e.g., e4): ").lower().strip()
    coords = parse_chess_square(square)

    if coords is None:
        print("Invalid square. Use format like 'e4', 'a8', etc.")
        return

    x, y = coords
    result = find_knight_tour(x, y)
    if result:
        print(f"\nKnight's Tour from {square}:\n")
        print_ascii_board(result)
        print("\nValidating solution...")
        validate_tour(result)
        print("\nAnimating knight's tour...\n")
        animate_knight_tour(result, delay=0.15)

    else:
        print("No complete tour found from that position.")

if __name__ == "__main__":
    main()
