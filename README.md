# About

Implementations of maze generation algorithms. Some are just direct Python ports of Jamis Buck's implementations, for example the [recursive backtracking algo](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking.html).

# Demo

Cartesian maze
![cartesian](https://user-images.githubusercontent.com/1688456/189581144-49ea2275-cec1-4430-94ab-e2f63de04986.png)

Triangle maze
![triangle](https://user-images.githubusercontent.com/1688456/189606883-6caea441-6816-4a86-8aba-3eaac3b233e7.png)

Hex maze
![hex](https://user-images.githubusercontent.com/1688456/189581139-3d9235df-31b1-46e0-bb26-9b348e30af34.png)

# Setup

```
virtualenv .
. bin/activate
pip install Pillow
mkdir img
```

# Run

```
python main.py
```

# TODO

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
