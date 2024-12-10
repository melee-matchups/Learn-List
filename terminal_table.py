import os
from color import Fg, Style


class TerminalTable:
    def __init__(self, headings: list[tuple[str, int | float, str]] = None, w: int | float = 1.0, h: int | float = 1.0,
                 sep: str = "▏"):
        """
        Creates a table for terminal

        Parameters:
            headings: list[tuple[str, int | float, str?]]
                A list of headings with a string title and width
                Width can be an integer, witch will be interpolated as a constant value
                Width and be a float, witch will be times by the remaining width of the table.
                The final string is optional and can be one of "l" "r" or "c" for alignment

            w: int | float
                The width of the table
                If the value a float, it will be multiplied by the terminal width.

            h: int | float
                The width of the table
                If the value a float, it will be multiplied by the terminal height.

            sep: str
                The seperator character
        """

        self.page = 0
        self.width = 0
        self.height = 0
        self.headings = [] if headings is None else headings
        self.width = w
        self.height = h
        self.data = []
        self.sep = sep
        self.pages = 1
        self.text = ""

        self.update()

    def set_content(self, data: list):
        """Sets the content of the table"""

        self.data = [
            d.copy()
            if len(d) == len(self.headings)
            else
            d[:len(self.headings)]
            if len(d) > len(self.headings)
            else
            d + ([""] * (len(self.headings) - len(d)))

            for d in data
        ]
        self.page = 0

        self.update()

    def update(self):
        """Updates the table"""

        w, h = os.get_terminal_size()

        width = int(
            w * self.width
            if type(self.width) == float
            else
            w - self.width
            if self.width < 0
            else
            self.width
        )
        height = int(
            h * self.height
            if type(self.height) == float
            else
            h + self.height
            if self.height < 0
            else
            self.height
        )

        rows = height - 1
        self.pages = (len(self.data) // rows) + 1

        if self.page >= self.pages:
            self.page = self.pages - 1

        left_space = width - (1 + sum([
            (heading[1] + 1)
            if type(heading[1]) == int
            else 1
            for heading in self.headings
        ]))

        column_sizes = [
            (heading[1] + 1)
            if type(heading[1]) == int
            else round(heading[1] * left_space) + 1
            for heading in self.headings
        ]

        content = ""
        table_data = [[heading[0] for heading in self.headings]] + self.data[self.page * rows: (self.page + 1) * rows]
        for row, data in enumerate(table_data):
            for i, size in enumerate(column_sizes):
                size -= 1
                datum = str(data[i])
                if len(datum) <= size:
                    datum = (
                        datum.ljust(size, " ")
                        if self.headings[i][-1] == "l"
                        else
                        datum.rjust(size, " ")
                        if self.headings[i][-1] == "r"
                        else
                        datum.center(size, " ")
                    )
                else:
                    datum = datum[: size]
                content += self.style(self.sep, row, None, rows, len(column_sizes)) + self.style(datum, row, i, rows,
                                                                                                 len(column_sizes))
            content += self.style(self.sep, row, len(column_sizes), rows, len(column_sizes)) + "\n"

        self.text = content[:-1]

    def print(self, update: bool = False):
        """Displays the table"""

        if update:
            self.update()

        print(self.text, end="")

    def style(self, string, row, column, rows, columns):
        """Override to customise the look of each item within the table"""

        color = (Fg.BLUE if row % 2 == 1 else Fg.BRIGHT_WHITE)

        if column is None:
            return Style.UNDERLINE + color + string
        elif column >= columns:
            return Style.UNDERLINE_OFF + string + Fg.BRIGHT_WHITE

        return Style.BOLD + color + string
