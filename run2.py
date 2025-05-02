import sys
from collections import deque

keys_char = [chr(i) for i in range(ord('a'), ord('z') + 1)]
doors_char = [k.upper() for k in keys_char]


def get_input():
    grid = []
    for line in sys.stdin:
        stripped = line.rstrip('\n')
        if not stripped:
            break
        grid.append(list(stripped))
    return grid


def solve(data):
    rows = len(data)
    if rows == 0:
        return -1
    cols = len(data[0]) if rows > 0 else 0

    start_positions = []
    keys = set()
    for i in range(rows):
        for j in range(cols):
            cell = data[i][j]
            if cell == '@':
                start_positions.append((i, j))
            elif cell in keys_char:
                keys.add(cell)

    num_keys = len(keys)
    if num_keys == 0:
        return 0

    start_positions.sort()
    start_tuple = tuple(start_positions)

    key_to_bit = {key: idx for idx, key in enumerate(sorted(keys))}
    target_mask = (1 << num_keys) - 1

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    visited = set()
    queue = deque()
    initial_state = (start_tuple, 0)
    visited.add(initial_state)
    queue.append((start_tuple, 0, 0))

    while queue:
        positions, mask, steps = queue.popleft()

        if mask == target_mask:
            return steps

        for robot in range(4):
            x, y = positions[robot]
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if 0 <= nx < rows and 0 <= ny < cols:
                    cell = data[nx][ny]
                    if cell == '#':
                        continue
                    if cell in doors_char:
                        req_key = cell.lower()
                        if req_key not in key_to_bit or not (mask & (1 << key_to_bit[req_key])):
                            continue
                    new_pos = list(positions)
                    new_pos[robot] = (nx, ny)
                    new_pos_sorted = tuple(sorted(new_pos))
                    new_mask = mask
                    if cell in key_to_bit:
                        new_mask |= (1 << key_to_bit[cell])
                    state = (new_pos_sorted, new_mask)
                    if state not in visited:
                        visited.add(state)
                        queue.append((new_pos_sorted, new_mask, steps + 1))

    return -1


def main():
    data = get_input()
    result = solve(data)
    print(result)


if __name__ == '__main__':
    main()