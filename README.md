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

* Make private most methods except ones like `generate` and `render_*`
* Add code to print the maze parameters at the bottom of the generated image, with a link to my Github?
* Factor out maze generation methods into their own class structure?
* Command-line args to specify what kind of maze and what maze generation method and what maze size
  * Check for compatibility: some mazes might permit only certain methods?
* Improve rendering: use the padding param, and fill a non-white background color for the maze?