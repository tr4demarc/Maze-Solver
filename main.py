from maze import Maze

maze = Maze("./mazes/small.png")
path = maze.solve()
maze.save_path_to_img(path)
