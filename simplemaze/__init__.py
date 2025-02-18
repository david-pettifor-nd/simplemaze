import random
from PIL import Image, ImageDraw

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.path = False   # used for wilson's algorithm
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    
    def __repr__(self):
        return f"Cell({self.x}, {self.y}: {self.visited}, {self.path})"

class Maze:
    def __init__(self, width, height, method='prim'):
        self.width = width
        self.height = height
        self.CELL_SIZE = 15
        self.maze = [[Cell(x, y) for x in range(width)] for y in range(height)]

        if method == 'depth_first':
            self.depth_first_cell_pass(self.maze[0][0])
        if method == 'kruskal':
            self.kruskal()
        if method == 'prim':
            self.prim()
        if method == 'wilson':
            self.wilson()

        # install doors (remove the top wall of the first cell and the bottom wall of the last cell)
        self.maze[0][0].walls['top'] = False
        self.maze[height - 1][width - 1].walls['bottom'] = False
    
    """
    Common functions used by multiple methods.
    """
    def _remove_wall(self, cell, neighbor):
        """
        Remove the wall between two cells.
        """
        # remove the wall between the cell and the neighbor
        if cell.x == neighbor.x:
            if cell.y < neighbor.y:
                cell.walls['bottom'] = False
                neighbor.walls['top'] = False
            else:
                cell.walls['top'] = False
                neighbor.walls['bottom'] = False
        else:
            if cell.x < neighbor.x:
                cell.walls['right'] = False
                neighbor.walls['left'] = False
            else:
                cell.walls['left'] = False
                neighbor.walls['right'] = False
    
  
    def _get_neighbors(self, cell):
        """
        Get the neighbors of a cell.
        """
        neighbors = []
        if cell.x > 0:
            neighbors.append(self.maze[cell.y][cell.x - 1])
        if cell.x < self.width - 1:
            neighbors.append(self.maze[cell.y][cell.x + 1])
        if cell.y > 0:
            neighbors.append(self.maze[cell.y - 1][cell.x])
        if cell.y < self.height - 1:
            neighbors.append(self.maze[cell.y + 1][cell.x])
        return neighbors

    def _get_random_neighbor(self, cell, previous_cell):
        """
        Get a random neighbor of the cell that is not the previous cell.
        """
        neighbors = self._get_neighbors(cell)

        # remove any neighbors that are part of the path
        neighbor_list = []
        for neighbor in neighbors:
            if neighbor != previous_cell:
                neighbor_list.append(neighbor)
            
        if len(neighbor_list) == 0:
            return None
        return neighbor_list[random.randint(0, len(neighbor_list) - 1)]

    def _get_unvisited_cells(self):
        """
        Get a list of all unvisited cells.
        """
        unvisited_cells = []
        for row in self.maze:
            for cell in row:
                if not cell.visited:
                    unvisited_cells.append(cell)
        return unvisited_cells
    
    def _get_random_unvisited_cell(self):
        """
        Get a random unvisited cell.
        """
        unvisited_cells = self._get_unvisited_cells()
        return unvisited_cells[random.randint(0, len(unvisited_cells) - 1)]
    
    def _has_unvisited_cells(self):
        """
        Check if there are any unvisited cells.
        """
        return len(self._get_unvisited_cells()) > 0
    
    def _get_previous_cell(self, path, neighbor):
        """
        Get the previous cell in the path.
        """
        previous_cell = None
        if len(path) <= 1:
            return None
        previous_cell = path[0]
        for cell in path[1:]:
            if cell == neighbor:
                return previous_cell
            previous_cell = cell
        return None
    
    """
    Wilson's algorithm for generating a maze.
    """
    def wilson(self):
        # choose a random cell
        cell = self.maze[random.randint(0, self.height - 1)][random.randint(0, self.width - 1)]
        cell.visited = True

        while self._has_unvisited_cells():
            """
            This section of code is to generate a random path from a new unvisited cell until we hit a cell that is part of the maze.
            """
            # initialize a new path to walk
            next_path = []

            path_complete = False

            # choose another random cell to begin the path
            path_cell = self._get_random_unvisited_cell()
            path_cell.path = True
            next_path.append(path_cell)
            previous_cell = None

            while not path_complete:
                # get a random neighbor of the path cell
                neighbor = self._get_random_neighbor(path_cell, previous_cell)

                # is the neighbor part of the maze (visited)?
                if neighbor.visited:
                    # remove wall
                    self._remove_wall(path_cell, neighbor)
                    # if so, then mark all of the cells in the path as visited as they are now part of the maze
                    for cell in next_path:
                        cell.visited = True
                        cell.path = False
                        path_complete = True
                        continue
                # if the neighbor is not part of the maze but is part of the path, then we've hit a loop. We need to remove the loop.
                if neighbor.path:
                    # remove the loop
                    next_path = self._remove_loop(next_path, neighbor)
                    previous_cell = self._get_previous_cell(next_path, neighbor)
                    path_cell = next_path[-1]

                # otherwise, add the neighbor to the path
                elif not path_complete:
                    next_path.append(neighbor)
                    neighbor.path = True
                    # remove the wall between the path cell and the neighbor
                    self._remove_wall(path_cell, neighbor)
                    # set the path cell to the neighbor
                    previous_cell = path_cell
                    path_cell = neighbor

    def _get_neighbor_in_path(self, cell):
        """
        Get a neighbor of the cell that is part of the path.
        """
        neighbors = []
        for neighbor in self._get_neighbors(cell):
            if neighbor.path:
                neighbors.append(neighbor)
        return neighbors
    
    def _remove_loop(self, path, starting_cell):
        """
        Remove the loop from the path. This resets the walls of the cells in the path to their original state.
        """
        # simply traverse the path in reverse until we reach the starting cell
        last_cell = path[-1]
        while path[-1] != starting_cell:
            cell = path[-1]
            # reset the walls of the cell
            cell.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}

            # remove this from being a path
            cell.path = False
            cell.visited = False
            # keep track of the last cell so we know how to rebuild the walls of the starting cell once we get there
            last_cell = cell
            path.remove(cell)
        
        # rebuild the walls of the starting cell
        if last_cell.x == starting_cell.x:
            if last_cell.y < starting_cell.y:
                starting_cell.walls['top'] = True
            else:
                starting_cell.walls['bottom'] = True
        else:
            if last_cell.x < starting_cell.x:
                starting_cell.walls['right'] = True
            else:
                starting_cell.walls['left'] = True
        path[-1] = starting_cell
        return path            

    """
    Prim's algorithm for generating a maze.
    """
    def prim(self):
        # pick a random cell
        cell = self.maze[random.randint(0, self.height - 1)][random.randint(0, self.width - 1)]
        cell.visited = True

        # add the walls of the cell to the list
        walls = []
        for neighbor in self._get_neighbors(cell):
            walls.append((cell, neighbor))

        while len(walls) > 0:
            # pick a random wall from the list
            wall = walls[random.randint(0, len(walls) - 1)]
            cell1, cell2 = wall

            # if one of the cells is unvisited, but the other is visited, remove the wall between the two cells
            if cell1.visited ^ cell2.visited:
                self._remove_wall(cell1, cell2)
                cell1.visited = True
                cell2.visited = True

                # add the walls of the cell to the list
                for neighbor in self._get_neighbors(cell2):
                    if not neighbor.visited:
                        walls.append((cell2, neighbor))
            # remove the wall from the list
            walls.remove(wall)

    """
    Kruskal's algorithm for generating a maze.
    """
    def kruskal(self):
        walls = []
        sets = []

        # add walls to the list and sets to the list
        for y in range(self.height):
            for x in range(self.width):
                if y > 0:
                    walls.append((self.maze[y][x], self.maze[y - 1][x]))
                if x > 0:
                    walls.append((self.maze[y][x], self.maze[y][x - 1]))
                sets.append([self.maze[y][x]])
        
        # shuffle the walls
        random.shuffle(walls)

        for wall in walls:
            cell1, cell2 = wall
            set1 = self._get_set(cell1, sets)
            set2 = self._get_set(cell2, sets)
            if set1 != set2:
                self._remove_wall(cell1, cell2)
                self._merge_sets(set1, set2, sets)
    
    def _get_set(self, cell, sets):
        """
        Get the set that the cell belongs to.
        """
        for set in sets:
            if cell in set:
                return set
        return None
    
    def _merge_sets(self, set1, set2, sets):
        """
        Merge two sets.
        """
        for cell in set2:
            set1.append(cell)
            self.maze[cell.y][cell.x] = cell
        sets.remove(set2)
    
    """
    Depth-first search for generating a maze.
    """
    def depth_first_cell_pass(self, cell):
        """
        Depth-first search for generating a maze.
        Uses recursion to visit each cell. Fast, but may create long corridors and run into max recursion depth for large mazes.
        """
        # mark the cell as visited
        cell.visited = True

        # get a list of neighbors
        neighbors = self._get_neighbors(cell)

        # shuffle the neighbors
        random.shuffle(neighbors)

        # for each neighbor, if it's not visited, remove the wall between the cell and the neighbor
        for neighbor in neighbors:
            if not neighbor.visited:
                self._remove_wall(cell, neighbor)
                self.depth_first_cell_pass(neighbor)
    
    """
    Export the maze to an HTML file.
    """
    def _compute_cell_size(self, page_width, page_height, margin, dpi):
        """
        Compute the cell size based on the size of the maze, paper, margins, and DPI.
        """
        # first try to calculate max cell size based on the width of the maze, considering we have 1px between each cell
        total_width = page_width - (margin * 2)

        # compute the dpi of the remaining width
        printable_dpi = (total_width * dpi)
        target_width_size = (printable_dpi / self.width) - ((dpi / 2) / self.height)


        total_height = page_height - (margin * 2)
        printable_dpi = (total_height * dpi)
        target_height_size = (printable_dpi / self.height) - ((dpi / 2) / self.height)

        return min(target_width_size, target_height_size)


    def export_to_html(self, filename, auto_scale=True, cell_size=None, page_width=8.5, page_height=11, margin=0.39, dpi=100):
        """
        Export the maze to an HTML file.
        """
        if auto_scale:
            # calculate the cell size based on the size of the maze
            # this makes a lot of assumptions about the printer setup...
            # 1. the printer is printing on 8.5x11 paper
            # 2. the printer is printing 0.39" inch margins on all sides
            # 4. the printer is printing 100 DPI
            # 5. the printer is printing 100% scale
            cell_size = self._compute_cell_size(page_width, page_height, margin, dpi)
            
        with open(filename, 'w') as file:
            file.write('<html><body><div style="display:table; border-collapse:collapse;">')
            for row in self.maze:
                file.write('<div style="display:table-row;">')
                for cell in row:
                    style = f'display:table-cell;width:{cell_size}px;height:{cell_size}px;border:1px solid black;'
                    if not cell.walls['top']:
                        style += 'border-top-style:hidden;'
                    if not cell.walls['right']:
                        style += 'border-right-style:hidden;'
                    if not cell.walls['bottom']:
                        style += 'border-bottom-style:hidden;'
                    if not cell.walls['left']:
                        style += 'border-left-style:hidden;'
                    file.write(f'<div style="{style}"></div>')
                file.write('</div>')
            file.write('</div></body></html>')


    def export_to_image(self, filename, cell_size=None, wall_width=1):
        """
        Export the maze to an image file.
        """
        if cell_size is None:   
            cell_size = self.CELL_SIZE

        # create a blank image
        image = Image.new('RGB', (self.width * cell_size, self.height * cell_size), 'white')

        # create a draw object
        draw = ImageDraw.Draw(image)

        # draw the maze
        for row in self.maze:
            for cell in row:
                if cell.walls['top']:
                    draw.line((cell.x * cell_size, cell.y * cell_size, (cell.x + 1) * cell_size, cell.y * cell_size), fill='black', width=wall_width)
                if cell.walls['right']:
                    draw.line(((cell.x + 1) * cell_size, cell.y * cell_size, (cell.x + 1) * cell_size, (cell.y + 1) * cell_size), fill='black', width=wall_width)
                if cell.walls['bottom']:
                    draw.line((cell.x * cell_size, (cell.y + 1) * cell_size, (cell.x + 1) * cell_size, (cell.y + 1) * cell_size), fill='black', width=wall_width)
                if cell.walls['left']:
                    draw.line((cell.x * cell_size, cell.y * cell_size, cell.x * cell_size, (cell.y + 1) * cell_size), fill='black', width=wall_width)

        # save the image
        image.save(filename)
