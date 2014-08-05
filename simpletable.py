#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
simpletable.py - v0.1 2014-07-31 Matheus Vieira Portela

This module provides simple classes and interfaces to generate simple HTML
tables based on Python native types, such as lists.

Author's website: http://matheusvportela.wordpress.com/
"""

__version__ = '0.2'
__date__    = '2014-08-05'
__author__  = 'Matheus Vieira Portela'

### CHANGES ###
# 2014-07-31: v0.1 MVP:
#   - First version
# 2014-08-05: v0.2 MVP:
#   - Method for defining header rows
#   - HTMLTable method to create a HTMLTable from lists

### TODO ###
# - Method to create a table from a simple list of elements and a column size
#   Example:
#   data = ['one','two','three','four','five','six','seven','eight','nine']
#   table = HTMLTable.table_from_list(data, cols=3)
#   
#   Result:
#   one     two    three
#   four    five   six
#   seven   eight  nine

### REFERENCES ###
# Decalage HTML.py module: http://www.decalage.info/python/html

import codecs

class HTMLTableCell(object):
    """A table class to create HTML table cells.

    Usage:
    cell = HTMLTableCell('Hello, world!')
    """

    def __init__(self, text, header=False):
        """Table cell constructor.

        Keyword arguments:
        text -- text to be displayed
        header -- flag to indicate this cell is a header cell.
        """
        self.text = text
        self.header = header
        
    def __str__(self):
        """Return the HTML code for the table cell."""
        if self.header:
            return '<th>%s</th>' %(self.text)
        else:    
            return '<td>%s</td>' %(self.text)

class HTMLTableRow(object):
    """A table class to create HTML table rows, populated by HTML table
    cell.

    Usage:
    # Row from list
    row = HTMLTableRow(['Hello,', 'world!'])

    # Row from HTMLTableCell
    cell1 = HTMLTableCell('Hello,')
    cell2 = HTMLTableCell('world!')
    row = HTMLTableRow([cell1, cell2])
    """
    def __init__(self, cells=[], header=False):
        """Table row constructor.

        Keyword arguments:
        cells -- iterable of HTMLTableCell (default None)
        header -- flag to indicate this row is a header row.
                  if the cells are HTMLTableCell, it is the programmer's
                  responsibility to verify whether it was created with the
                  header flag set to True.
        """
        if isinstance(cells[0], HTMLTableCell):
            self.cells = cells
        else:
            self.cells = [HTMLTableCell(cell, header=header) for cell in cells]
        
        self.header = header
        
    def __str__(self):
        """Return the HTML code for the table row and its cells as a string."""
        row = []

        row.append('<tr>')

        for cell in self.cells:
            row.append(str(cell))

        row.append('</tr>')
        
        return '\n'.join(row)

    def __iter__(self):
        """Iterate through row cells"""
        for cell in self.cells:
            yield cell

    def add_cell(self, cell):
        """Add a HTMLTableCell object to the list of cells."""
        self.cells.append(cell)

    def add_cells(self, cells):
        """Add a list of HTMLTableCell objects to the list of cells."""
        for cell in cells:
            self.cells.append(cell)


class HTMLTable(object):
    """A table class to create HTML tables, populated by HTML table rows.

    Usage:
    # Table from lists
    table = HTMLTable([['Hello,', 'world!'], ['How', 'are', 'you?']])

    # Table with header row
    table = HTMLTable([['Hello,', 'world!'], ['How', 'are', 'you?']],
                      header_row=['Header1', 'Header2', 'Header3'])

    # Table from HTMLTableRow
    rows = HTMLTableRow(['Hello,', 'world!'])
    table = HTMLTable(rows)
    """
    def __init__(self, rows=[], header_row=None, css_class=None):
        """Table constructor.

        Keyword arguments:
        rows -- iterable of HTMLTableRow
        header_row -- row that will be displayed at the beginning of the table.
                      if this row is HTMLTableRow, it is the programmer's
                      responsibility to verify whether it was created with the
                      header flag set to True.
        css_class -- table CSS class
        """
        if isinstance(rows[0], HTMLTableRow):
            self.rows = rows
        else:
            self.rows = [HTMLTableRow(row) for row in rows]

        if header_row is None:
            self.header_row = None
        elif isinstance(header_row, HTMLTableRow):
            self.header_row = header_row
        else:
            self.header_row = HTMLTableRow(header_row, header=True)

        self.css_class = css_class

    def __str__(self):
        """Return the HTML code for the table as a string."""
        table = []

        if self.css_class:
            table.append('<table class=%s>' % self.css_class)
        else:
            table.append('<table>')

        if self.header_row:
            table.append(str(self.header_row))

        for row in self.rows:
            table.append(str(row))

        table.append('</table>')
        
        return '\n'.join(table)

    def __iter__(self):
        """Iterate through table rows"""
        for row in self.rows:
            yield row

    def add_row(self, row):
        """Add a HTMLTableRow object to the list of rows."""
        self.rows.append(row)

    def add_rows(self, rows):
        """Add a list of HTMLTableRow objects to the list of rows."""
        for row in rows:
            self.rows.append(row)


class HTMLPage(object):
    """A class to create HTML pages containing CSS and tables."""
    def __init__(self, table=None, css=None, encoding="utf-8"):
        """HTML page constructor.

        Keyword arguments:
        table -- HTMLTable object
        css -- Cascading Style Sheet specification that is appended before the
               table string
        encoding -- Characters encoding. Default: UTF-8
        """
        self.table = table
        self.css = css
        self.encoding = encoding
        
    def __str__(self):
        """Return the HTML page as a string."""
        page = []

        if self.css:
            page.append('<style type="text/css">\n%s\n</style>' % self.css)

        # Set encoding
        page.append('<meta http-equiv="Content-Type" content="text/html;'
            'charset=%s">' % self.encoding)

        if self.table:
            page.append(str(table))

        return '\n'.join(page)

    def save(self, filename):
        """Save HTML page to a file using the proper encoding"""
        with codecs.open(filename, 'w', self.encoding) as outfile:
            for line in str(self):
                outfile.write(line)


### Example usage ###
if __name__ == "__main__":
    css = """
    table.mytable {
        font-family: times;
        font-size:12px;
        color:#000000;
        border-width: 1px;
        border-color: #eeeeee;
        border-collapse: collapse;
        background-color: #ffffff;
        width=100%;
        max-width:550px;
        table-layout:fixed;
    }
    table.mytable th {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #eeeeee;
        background-color: #e6eed6;
        color:#000000;
    }
    table.mytable td {
        border-width: 1px;
        padding: 8px;
        border-style: solid;
        border-color: #eeeeee;
    }
    #code {
        display:inline;
        font-family: courier;
        color: #3d9400;
    }
    #string {
        display:inline;
        font-weight: bold;
    }
    """
    table = HTMLTable([['Hello,', 'world!'], ['How', 'are', 'you?']],
            header_row=['Header1', 'Header2', 'Header3'],
            css_class='mytable')
    page = HTMLPage(table, css=css)
    page.save("test.html")
    print page