from collections import deque


def main():
    try:
        maze = input_read('InputMaze.txt')
        path = BidirectionalMaze(maze)
        if isinstance(path, list):  # Checking if the path is a list before marking
            print("This is the input maze!")
            for row in maze:
                print(' '.join(map(str, row)))
            mark_path(maze, path)
            printing_maze(maze)    # displays output on the console
            OutputMaze(maze, '../OutputMaze.txt')  # writing to the new file
        else:
            print(path)
    except FileNotFoundError:
        print("Error: The file 'InputMaze.txt' could not be found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def input_read(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        maze = []
        # Processing each line in the file
        for line in data.splitlines():
            # Converting each character in the line to an integer and appending to the maze list
            maze.append([int(i) for i in line.strip()])
    return maze


# marking the path traversal with 2
def mark_path(maze, path):
    for x, y in path:
        maze[x][y] = 2


# OutputMaze on console
def printing_maze(maze):
    print("This is the output maze!")
    for row in maze:
        print(' '.join(map(str, row)))


# creates output file  OutputMaze.text
def OutputMaze(maze, filename):
    with open(filename, 'w') as file:
        for row in maze:
            file.write(' '.join(map(str, row)) + '\n')


def BidirectionalMaze(maze):
    # Assuming the maze only contains 0's and 1's
    if maze[0][0] == 1 or maze[-1][-1] == 1:
        return "No available entry or exit!"

    rows, cols = len(maze), len(maze[0])

    front_visited_nodes = set([(0, 0)])
    back_visited_nodes = set([(rows - 1, cols - 1)])

    front_q = deque([((0, 0), [(0, 0)])])
    back_q = deque([((rows - 1, cols - 1), [(rows - 1, cols - 1)])])

    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]  # up down right left

    while front_q and back_q:
        if front_q:
            # current position is a tuple of two items and fpath contains the path traversed
            current_fpos, fpath = front_q.popleft()
            # print("current node popped from the deque is :", current_fpos)
            if current_fpos in back_visited_nodes:
                for bpos, bpath in back_q:
                    if bpos == current_fpos:
                        print("Yayy! Path intersection found at:", bpos)
                        return fpath + bpath[::-1]  # reversing back the path and appending
            for x, y in directions:
                nx, ny = current_fpos[0] + x, current_fpos[1] + y
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in front_visited_nodes:
                    # print("The front node now currently is at : ", nx, ny)
                    front_q.append(((nx, ny), fpath + [(nx, ny)]))
                    front_visited_nodes.add((nx, ny))
                    # print("front visited nodes so far : ", front_visited_nodes)
            # print("Path covered so far from the front: ", fpath)

        # From the back
        if back_q:
            current_bpos, bpath = back_q.popleft()
            # print("current node popped from the deque is :", current_bpos)
            if current_bpos in front_visited_nodes:
                # finding the intersecting path from front queue
                for fpos, fpath in front_q:
                    if fpos == current_bpos:
                        print("Yayy! Path intersection found at:", fpos)
                        return fpath + bpath[::-1]

            # iterating through the directions to find the possible path
            for x, y in directions:
                nx, ny = current_bpos[0] + x, current_bpos[1] + y
                if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] == 0 and (nx, ny) not in back_visited_nodes:
                    # print("The back node now currently is at : ", nx, ny)
                    back_q.append(((nx, ny), bpath + [(nx, ny)]))
                    back_visited_nodes.add((nx, ny))
                    # print("back visited nodes so far : ", back_visited_nodes)
            # print("Path covered so far from the back: ", bpath)
    return "Oops!! No path found"


if __name__ == '__main__':
    main()
