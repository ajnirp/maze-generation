# About

Implementations of maze generation algorithms. Some are just direct Python ports of Jamis Buck's implementations, for example the [recursive backtracking algo](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking.html).

# Setup

```
virtualenv .
. bin/activate
pip install Pillow
```

# Run

```
python main.py
```

# Notes

* `img/` contains image outputs and its contents can be safely deleted. Don't delete the folder itself

# TODO

* Triangle maze
* Add code to print the maze parameters at the bottom of the generated image, with a link to my Github?
* Factor out maze generation methods into their own class structure?
* Command-line args to specify what kind of maze and what maze generation method and what maze size
  * Check for compatibility: some mazes might permit only certain methods?
  * Ideally, user specifies maze type, size and window dimensions, and we calculate suitable values for scale and padding from those params
* Improve rendering: fill a non-white background color for the maze?
* Add demo images to the README

More long-term ideas
* Generate a maze and send it to an algorithm that does path-finding
* Implement different path finding algos like DFS, BFS, A* maybe?
* Visualize the found paths and maybe animate it with the `turtle` library?
* Smooth mazes with arbitrary degree turns? Maybe generate a rectangular maze and then smoothen it somehow? Circular maze? Crude way to model a side cartoon view of the human brain?