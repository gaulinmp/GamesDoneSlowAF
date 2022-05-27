#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path

print("\n"*10)

def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

    from django.core.management import execute_from_command_line

    # This allows easy placement of apps within the interior
    # gdsaf directory.
    ROOT_PATH = Path(__file__).parent.resolve()
    print(ROOT_PATH)
    sys.path.append(str(ROOT_PATH))
    # sys.path.append(str(ROOT_PATH / "apps"))

    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
