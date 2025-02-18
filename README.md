# SimpleMaze

A Python library for generating mazes.

## Installation

```bash
pip install simplemaze
```

## Usage

```python
from simplemaze import Maze

# generates a 10x10 maze (width, height)
maze = Maze(10, 10)

# export the maze to an html file for printing
maze.export_to_html('maze.html')

# export the maze to an image file
maze.export_to_image('maze.png')
```

## Algorithms

### Recursive Backtracker (Depth-First Search)
```python
from simplemaze import Maze

# generates a 10x10 maze (width, height) using the depth-first search algorithm
maze = Maze(10, 10, method='depth_first')
```

This algorithm is a simple depth-first search that starts at the top-left corner and randomly chooses a direction to move in. It then recursively calls itself to generate the maze.

This algorithm is very fast, and guarantees a unique solution if the maze has no cycles. However, it does not produce the most aesthetically pleasing mazes. Most of the time, it will create a maze that has a very long, winding solution with short dead ends.

### Kruskal's Algorithm
```python
from simplemaze import Maze

# generates a 10x10 maze (width, height) using Kruskal's algorithm
maze = Maze(10, 10, method='kruskal')
```

This algorithm is a more complex algorithm that guarantees a unique solution if the maze has no cycles. It works by randomly choosing two cells and removing the wall between them if they are not already connected. It then recursively calls itself to generate the maze.

It produces mazes that are much more aesthetically pleasing than the depth-first search algorithm, but are typically not as long as the depth-first search algorithm and easier to solve. However, it is slower than the depth-first search algorithm.

### Prim's Algorithm (default)
```python
from simplemaze import Maze

# generates a 10x10 maze (width, height) using Prim's algorithm
maze = Maze(10, 10, method='prim')
```

This algorithm is similar to Kruskal's algorithm, but it works by starting at a random cell and then growing the maze outward from there. It is faster than Kruskal's algorithm, but it produces mazes that are more challenging to solve with a shorter solution path but longer dead ends.

### Wilson's Algorithm
```python
from simplemaze import Maze

# generates a 10x10 maze (width, height) using Wilson's algorithm
maze = Maze(10, 10, method='wilson')
```

This algorithm is a more complex algorithm that guarantees a unique solution if the maze has no cycles (however, it is possible to generate a maze that has cycles with this algorithm). It works by starting at a random cell and then growing the maze outward from there. It is slower than Prim's algorithm, but it produces mazes that are more aesthetically pleasing and easier to solve.

## Exporting to HTML

The HTML export is designed to be printed on standard 8.5x11 inch paper with 0.39 inch margins on all sides. The HTML file will automatically scale the maze to fit the page, so it will be as large as possible without cutting off the walls. 

```python
maze.export_to_html('maze.html')
```

### Parameters

- `auto_scale`: If true, the maze will be scaled to fit the page. If false, the maze will be scaled to the specified cell size.
- `cell_size`: The size of each cell in the maze.
- `page_width`: The width of the page in inches.
- `page_height`: The height of the page in inches.
- `margin`: The margin of the page in inches.

```python
maze.export_to_html('maze.html', auto_scale=False, cell_size=20, page_width=8.5, page_height=11, margin=0.39)
```

## Exporting to Image

The image export takes in a filename and a cell size. It will create a blank image of the specified cell size and draw the maze on it.

```python
maze.export_to_image('maze.png')
```

### Parameters

- `cell_size`: The size of each cell in the maze.
- `wall_width`: The width of the walls in the maze.

```python
maze.export_to_image('maze.png', cell_size=20, wall_width=1)
```
