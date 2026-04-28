# AGENTS.md - Repository Guidelines

## Project Overview

This is a Python learning project focused on digital image processing. It contains standalone scripts demonstrating OpenCV, NumPy, and Matplotlib operations (transforms, histograms, rotation, feature matching, etc.).

**Structure:**
- `ClassLightlyTry/` — In-class exercise scripts
- `Homework/` — Homework assignments
- `images/` — Shared image assets
- `venv/` — Python virtual environment (do not commit)

## Commands

### Run a script
```bash
python ClassLightlyTry/<ScriptName>.py
python Homework/Homework01.py
```

### Run a single file
```bash
python <path/to/file>.py
```

### Testing
There is **no test framework** in this project. Scripts are run directly to verify output (images/histograms display via cv2.imshow or plt.show).

### Linting / Formatting
There is **no linter or formatter** configured. If adding one, prefer `ruff` for both linting and formatting.

### Dependencies
Managed ad-hoc via `pip install`. Core deps: `opencv-python`, `numpy`, `matplotlib`. No `requirements.txt` or `pyproject.toml` exists yet.

## Code Style

### Imports
- Group: stdlib → third-party → local, each group separated by a blank line.
- Use `import cv2`, `import numpy as np`, `from matplotlib import pyplot as plt`.
- Avoid wildcard imports (`from module import *`).

### Naming
- **Files:** PascalCase (existing convention, e.g., `GammaTransform.py`).
- **Variables/functions:** snake_case (e.g., `gray_image`, `log_transform`).
- **Classes:** PascalCase (e.g., `class Dog`).
- **Constants:** UPPER_SNAKE_CASE.

### Formatting
- 4-space indentation (no tabs).
- Max line length ~120 chars.
- Spaces around operators: `a = b + c`, not `a=b+c`.
- Trailing newline at end of file.

### Types
No type annotations are used currently. If adding new code, prefer type hints for function signatures:
```python
def log_transform(c: float, img: np.ndarray) -> np.ndarray:
```

### Error Handling
- Check file existence with `os.path.exists()` before `cv2.imread()`.
- Check `img is None` after reading.
- Use `exit()` or early return for fatal errors in scripts.
- No try/except needed for simple scripts unless handling specific exceptions.

### Comments
- Chinese comments are acceptable (this is a Chinese-language course project).
- Prefer inline comments for algorithm steps.
- Add brief header comments describing what the script demonstrates.

### Image Paths
- Use relative paths to `images/` directory when possible.
- Use raw strings for Windows paths: `r'C:\path\to\file'`.
- Never hardcode absolute user paths in shared code.

### OpenCV + Matplotlib Coexistence
- Call `cv2.waitKey(1)` before `plt.show()` to let OpenCV render.
- Call `cv2.destroyAllWindows()` after `plt.show()` returns.

## Agent Guidelines

- **Do not** modify existing scripts unless explicitly asked (they are graded coursework).
- **Do** add new files alongside existing ones following the same patterns.
- **Do not** commit `venv/`, `__pycache__/`, or image files in `images/`.
- **Do** verify scripts run without import errors before considering a change complete.
