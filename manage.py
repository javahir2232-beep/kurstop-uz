#!/usr/bin/env python
import os
import sys

def main():
    # kurstop_all o'zi settings.configure + django.setup qiladi
    import kurstop_all  # noqa: F401
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
