import json

from color import Fg, Style
import os

from search import Search
from terminal_table import TerminalTable

GOTO_TOP = "\033[0;0f"


def clear():
    """Clears the screen"""

    os.system("cls" if os.name == "nt" else "clear")


class App:
    def __init__(self, file: str = "./learn_list.json"):
        """
        Creates an App

        Parameters:
            file: str / PathLike
                The file path to the file
        """

        self.message = ""
        self.file = file
        self.data = None

        self.search = Search()
        self.table = TerminalTable(headings=[
            ("ID ", 3, "c"),
            ("Name ", 0.75, "l"),
            ("Times Said ", 11, "c"),
            ("Tags ", 0.25, "l"),
        ], h=-2)

    def save(self) -> bool | None:
        """
        Saves the data to a file

        Returns:
            True on failure
        """

        try:
            json.dump(self.data, open(self.file, "w"), indent=4)
        except Exception as err:
            print(Fg.BRIGHT_RED + "Cannot save file:", err, Fg.BRIGHT_WHITE)
            return True

    def load(self) -> bool | None:
        """
        Saves the data to a file

        Returns:
            True on failure
        """

        if not os.path.exists(self.file):
            if self.save():
                print(Fg.BRIGHT_RED + "Cannot create new file", Fg.BRIGHT_WHITE)
                return True

        try:
            self.data = json.load(open(self.file))
        except Exception as err:
            print("Cannot open file:", err)
            return True

        self.update_search()

    def output(self):
        """Prints the UI to the screen"""

        clear()

        # Blank Line for input
        print(Style.BOLD + Fg.BRIGHT_WHITE)

        # Status bar
        tags_string = ("#" + (" #".join(self.search.search_tags))) if self.search.search_tags else ""
        search_string = "\t" + self.search.search if self.search.search else ""
        print(f"Page[{self.table.page + 1:>3}/{self.table.pages:>3}]\t| ", tags_string, " | ", search_string, sep="", end="\n")

        # Table
        self.table.print(update=True)

    def get_input(self) -> str | None:
        """
        Gets the users input

        Returns:
            The user input as a string
            Returns None on KeyboardInterrupt
        """

        try:
            inp = input(GOTO_TOP + self.message + Fg.BRIGHT_WHITE + ">>: ")
            self.message = ""

            return inp
        except KeyboardInterrupt:
            return None

    def input(self):
        inp = self.get_input()

        if inp is None:
            return True

        if inp.startswith("#"):
            inp = "/tags " + inp[1:]

        if inp.startswith("/"):
            args = "" if inp.find(" ") == -1 else inp[inp.find(" ") + 1:]
            cmd = inp[1:] if inp.find(" ") == -1 else inp[1:inp.find(" ")]

            return self.handle_command(cmd, args)
        else:
            self.search.search = inp

            self.update_search()

    def handle_command(self, cmd: str, args: str) -> bool | None:
        """
        Handle input commands

        Parameters:
            cmd: str
                The command

            args: str
                The rest of the input after the command

        Returns:
            True on failure
        """

        if cmd in ["exit", "quit"]:
            return True

        elif cmd == "page":
            if not args.isdigit():
                self.message = Fg.BRIGHT_RED + "Page number must be integer"
                return

            self.table.page = min(max(int(args) - 1, 0), table.pages - 1)

        elif cmd in ["", "next"] and args == "":
            self.table.page += 1
            if self.table.page == self.table.pages:
                self.table.page = 0

        elif (cmd in ["/", "back", "prev", "-"]) and args == "":
            if self.table.page == 0:
                self.table.page = self.table.pages
            self.table.page -= 1

        elif cmd in ["tags", "tag"]:
            if args == "":
                self.search.search_tags.clear()
            else:
                self.search.search_tags = [arg[1:] if arg.startswith("#") else arg for arg in args.split(" ")]

            self.update_search()

        elif cmd in ["search", "?"]:
            if args == "":
                self.search.regex = False
                self.search.case = False
                self.search.explicit = False

            for arg in args.split(" "):
                if arg in ["e", "exp", "explicit"]:
                    self.search.explicit = not self.search.explicit
                elif arg in ["r", "re", "regex"]:
                    self.search.regex = not self.search.regex
                elif arg in ["c", "case"]:
                    self.search.case = not self.search.case

            self.update_search()

        elif cmd in ["save", "s"]:
            self.save()

        elif cmd in ["reload", "refresh", "re"]:
            self.load()
            self.update_search()

        elif cmd in ["edit", "e", "add", "a"]:
            if cmd in ["edit", "e"]:
                if " " not in args:
                    self.message = Fg.BRIGHT_RED + "Malformed input"
                    return

                index, args = args.split(" ", 1)
                if not index.isdigit():
                    self.message = Fg.BRIGHT_RED + "ID is not a number"
                    return

                index = int(index)

                if index >= len(self.data) or index < 0:
                    self.message = Fg.BRIGHT_RED + "ID is out of range"
                    return
            else:
                index = len(self.data)
                self.data.append(["", 1, []])

            tags = []
            while len(args) and args[0] == "#":
                if " " not in args:
                    tags.append(args[1:])
                    args = ""

                tag, args = args.split(" ", 1)
                tags.append(tag[1:])

            self.data[index] = [args, self.data[index][1], tags]

            self.update_search()

        elif cmd in ["done", "check", "d", "undone", "flip", "undo", "uncheck", "un"]:
            if not args.isdigit():
                self.message = Fg.BRIGHT_RED + "ID is not a number"
                return

            index = int(args)
            if index >= len(self.data) or index < 0:
                self.message = Fg.BRIGHT_RED + "ID is out of range"
                return

            self.data[index][1] = -self.data[index][1]

            self.update_search()

        elif cmd in ["dec", "-", "minus"]:
            if not args.isdigit():
                self.message = Fg.BRIGHT_RED + "ID is not a number"
                return

            index = int(args)
            if index >= len(self.data) or index < 0:
                self.message = Fg.BRIGHT_RED + "ID is out of range"
                return

            self.data[index][1] -= 1

            self.update_search()

        elif cmd in ["inc", "+"] or (cmd.isdigit() and args == ""):
            if cmd.isdigit():
                index = int(cmd)
            elif args.isdigit():
                index = int(args)
            else:
                self.message = Fg.BRIGHT_RED + "ID is not a number"
                return

            if index >= len(self.data) or index < 0:
                self.message = Fg.BRIGHT_RED + "ID is out of range"
                return

            self.data[index][1] += 1

            self.update_search()

        else:
            self.message = Fg.BRIGHT_RED + f"Unknown command: {cmd} {args}"

    def update_search(self):
        """Updates the search values and table values"""

        self.search.list = [(i, d[0], d[1], d[2]) for i, d in enumerate(self.data)]
        self.table.set_content([[d[0], d[1], d[2], "#" + (" #".join(d[3])) if d[3] else ""] for d in self.search.get_filtered_list()])

    def mainloop(self):
        """Enters a input loop with the user until they choose to exit"""

        clear()
        self.update_search()
        self.output()

        while not self.input():
            self.output()

        clear()
