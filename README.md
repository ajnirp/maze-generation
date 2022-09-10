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
* Factor out maze generation methods into their own class structure?
* Command-line args to specify what kind of maze and what maze generation method
  * Check for compatibility: some mazes might permit only certain methods?