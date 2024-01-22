"""
Maintain version for this package.
"""

MAJOR = 2
"""(int) Version major component."""

MINOR = 3
"""(int) Version minor component."""

POST = 0
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (MAJOR, MINOR, POST)])

