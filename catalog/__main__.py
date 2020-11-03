""" Main module of the application."""

from .catalog import TheMenu


def main():
    """Main entry point."""
    test = TheMenu()
    test.start()


if __name__ == "__main__":
    main()
