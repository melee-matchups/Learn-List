import bisect
import re


class Search:
    def __init__(self, init_list=None):
        self.search = ""
        self.search_tags = []
        self.list = [] if init_list is None else init_list
        self.regex = False
        self.case = False
        self.explicit = False

    def get_filtered_list(self):
        """gets a new list based off of the search queries"""

        new_list = []
        if not (self.search or self.search_tags):
            return sorted(self.list, key=self.sorting_key)

        for item in self.list:
            if (self.search == "" or (
                (
                    bool(re.match(self.search, item[1], re.NOFLAG if self.case else re.IGNORECASE))
                    if self.explicit
                    else (
                        bool(re.search(self.search, item[1], re.NOFLAG if self.case else re.IGNORECASE))
                    )
                )
                if self.regex
                else (
                    (self.search == item[1]) if self.case else (self.search.lower() == item[1].lower())
                    if self.explicit
                    else (
                        (self.search in item[1]) if self.case else (self.search.lower() in item[1].lower())
                    )
                )
            )) and all(tag.lower() in [t.lower() for t in item[3]] for tag in self.search_tags):
                bisect.insort(new_list, item, key=self.sorting_key)

        return new_list

    def sorting_key(self, item):
        return -item[2]
