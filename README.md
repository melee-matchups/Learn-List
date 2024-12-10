# Learn List
A basic console base application to help manage a list of things to learn by how often people tell you about it

Each item has a list of tags related to it for easy searching

## Command Line Arguments
You can pass a file as an argument to read and save from

## Input Commands
- `/[id]`
- `/inc [id]`
    > Increment the "Times Said" by one 
    > 
    > `[id]` is a positive whole number

- `/dec [id]`
    > Decrement the "Times Said" by one 
    > 
    > `[id]` is a positive whole number

- `/done [id]`
    > Mark the item as done
    > 
    > `[id]` is a positive whole number

- `/add` `#Tag` `#Tag2` `...` `#TagN` `[Item] ...`
    > Adds an item into the table, with any amount of tags

- `/edit` `[id]` `#Tag` `#Tag2` `...` `#TagN` `[Item] ...`
    > Edits an item into the table, re-enter its tags and data
    > 
    > `[id]` is a positive whole number

- `/reload`
    > Reload the file from disk, erasing any changes

- `#TAG` `...`
- `/tags` `TAG` `...`
    > Filter for tags

- `/search` `[Search option]` `...`
    > Set search options
    > 
    > `[Search option]` is one of:
    > - _r_ egex
    > - _c_ ase
    > - _e_ xplicit

- `...`
    > Any other text typed will filter the table for those words
    > 
    > Typing nothing will clear the search

- `/`
- `/next`
    > Goes to the next page, will loop around if at the last page.

- `/back`
- `/prev`
- `//`
    > Goes to the previous page, will loop around if at the first page.

- `/page` `[Page]`
    > Goes to the page number

- `/save`
- `/s`
    > Saves the file

- `/exit`
- `/quit`
    > Exits the app and saves the file
