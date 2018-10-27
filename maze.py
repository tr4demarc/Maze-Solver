from PIL import Image
import random

class Maze:

    def __init__(self, img_path):
        self.img = Image.open(img_path)
        self.width, self.height = self.img.size
        self.pix = self.img.load()
        self.maze = self.get_maze()
        self.start = self.get_start()
        self.end = self.get_end()


    def get_maze(self):
        pixel_array = []
        for i in range(self.height):
            row = []
            for j in range(self.height):
                row.append(self.pix[j, i])
            pixel_array.append(row)
        return pixel_array


    def get_start(self):
        for i in range(self.width):
            if self.maze[0][i]:
                return (0, i)
        return False


    def get_end(self):
        for i in range(self.width):
            if self.maze[self.height - 1][i]:
                return (self.height - 1, i)
        return False


    def show(self, maze=None):
        """Prints out readable version Maze. Default is
        standard maze but can print any mazes"""
        maze = self.maze if maze is None else maze
        for line in maze:
            print(*line)
        return True


    def solve(self):
        """
        Solves maze and returns path.
        """

        def random_path():
            """Tries a random path and returns path and dead end
            encountered."""

            def random_neighbour(coords):
                """Return a random neighbour that has not been
                visisted yet and that is not in the dead ends list.
                Returns None if there aren't any available."""

                row, col = coords
                neighbours = []

                if not row + 1 == self.height:
                    down = (row + 1, col) if self.maze[row + 1][col] else None
                else:
                    down = None
                if not col + 1 == self.width:
                    right = (row, col + 1) if self.maze[row][col + 1] else None
                else:
                    right = None

                up = (row - 1, col) if self.maze[row - 1][col] else None
                left = (row, col - 1) if self.maze[row][col - 1] else None

                for element in [up, down, left, right]:
                    if element and not element in visited + dead_ends:
                         neighbours.append(element)

                if len(neighbours) == 0:
                    return None, 0
                else:
                    random_choice = random.choice(neighbours)
                    return random_choice, len(neighbours)

            path = [self.start]
            visited = [self.start]
            neighbour_counts = []
            next_neighbour, no_of_neighbours = random_neighbour(path[-1])

            while next_neighbour:
                path.append(next_neighbour)
                neighbour_counts.append(no_of_neighbours)
                visited.append(path[-1])
                next_neighbour, no_of_neighbours = random_neighbour(next_neighbour)

            neighbour_counts.append(0)

            # Find dead end, i.e. from the end of the list find the first item
            # that is not 1.
            for i in range(1, len(neighbour_counts) + 1):
                if neighbour_counts[-i] > 1:
                    dead_end = path[-i + 1]
                    break

            return path, dead_end


        dead_ends = []
        path, dead_end = random_path()
        while not path[-1] == self.end:
            dead_ends.append(dead_end)
            path, dead_end  = random_path()

        return path


    def draw_path(self, path):
        maze_with_path = self.maze

        for cell in path:
            row, col = cell
            maze_with_path[row][col] = "X"

        visual_maze = []
        for row in maze_with_path:
            visual_maze.append(["#" if cell == 0 else cell for cell in row])

        self.show(visual_maze)
        return True


    def save_path_to_img(self, path):
        img = self.img.convert("RGB")
        pix = img.load()
        for cell in path:
            x, y = cell
            pix[y, x] = (255, 0, 0)
        img.save("solution.png", "PNG")
