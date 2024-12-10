import sys

from color import init, RESET
from app import App


def main():
    init()

    app = App()
    if len(sys.argv) == 2:
        app.file = sys.argv[1]

    if app.load():
        return

    app.mainloop()
    app.save()

    print(end=RESET)


if __name__ == "__main__":
    main()
