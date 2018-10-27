from maze import Maze

maze = Maze("./mazes/combo400.png")
path = maze.solve()
maze.save_path_to_img(path)
