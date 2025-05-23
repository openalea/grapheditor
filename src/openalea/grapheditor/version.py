"""
Maintain version for this package.
"""

MAJOR = 2
"""(int) Version major component."""

MINOR = 4
"""(int) Version minor component."""

POST = 1
"""(int) Version post or bugfix component."""

__version__ = ".".join([str(s) for s in (MAJOR, MINOR, POST)])

