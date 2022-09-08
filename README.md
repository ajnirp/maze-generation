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
python recursive-backtracking.py
python iterative-backtracking.py # currently broken
```

# Notes

* `img/` contains image outputs and its contents can be safely deleted. Don't delete the folder itself