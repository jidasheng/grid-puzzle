import tkinter as tk


class Table(tk.Frame):
    def __init__(self, master, line_with=1, xscroll=False, yscroll=False,
                 line_color="#dfe2e5", row_colors=("#f6f8fa", "#ffffff"), title_color="#e6e8ea", bg_color=None,
                 widths=None):
        tk.Frame.__init__(self, master, bd=0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.line_with = line_with
        self.line_color = line_color
        self.row_colors = row_colors
        self.title_color = title_color
        self.bg_color = bg_color
        self.xscroll = xscroll
        self.yscroll = yscroll

        self.__build_framework()
        self.__children = []
        self.horizontal_lines = []
        self.vertical_lines = []
        self.widths = widths

    def __build_framework(self):
        self.grid_propagate(False)
        canvas = tk.Canvas(self)
        canvas.grid(row=0, column=0, sticky=tk.NSEW)

        self.content_frame = tk.Frame(canvas, bg=self.bg_color)
        canvas.create_window((0, 0), window=self.content_frame, anchor='nw')

        if self.xscroll:
            self.horizontal_sb = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
            self.horizontal_sb.grid(row=1, column=0, sticky=tk.EW)
            canvas.config(xscrollcommand=self.horizontal_sb.set)

        if self.yscroll:
            self.vertical_sb = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
            self.vertical_sb.grid(row=0, column=1, sticky=tk.NS)
            canvas.config(yscrollcommand=self.vertical_sb.set)

        self.canvas = canvas

    def load_data(self, data):
        for row, texts in enumerate(data):
            for column, text in enumerate(texts):
                self.add_item(str(text), row, column)
        self.complete()
        return self

    def add_item(self, widget, row, column, rowspan=1, columnspan=1, sticky=tk.NSEW, ipadx=5, ipady=3):
        if isinstance(widget, str):
            width = self.widths[column] if columnspan == 1 and self.widths and column < len(self.widths) else None
            color = self.title_color if row == 0 and rowspan == 1 else self.row_colors[row % 2]
            widget = tk.Label(self.content_frame, text=widget, bg=color, width=width)

        self.__children.append((widget, row, column, rowspan, columnspan))
        widget.grid(row=row * 2 + 1, column=column * 2 + 1,
                    rowspan=rowspan * 2 - 1, columnspan=columnspan * 2 - 1,
                    sticky=sticky, ipadx=ipadx, ipady=ipady)

    def clear(self):
        for c in list(self.content_frame.children.values()):
            c.destroy()
        self.content_frame.children.clear()

        del self.__children[:]
        del self.horizontal_lines[:]
        del self.vertical_lines[:]

    def complete(self):
        max_row, max_column = 0, 0
        for widget, row, column, rowspan, columnspan in self.__children:
            max_row = max(max_row, row + rowspan)
            max_column = max(max_column, column + columnspan)

        self.__build_separator_lines(max_row, max_column)
        self.relayout()

    def relayout(self):
        self.content_frame.update_idletasks()

        width = self.content_frame.winfo_width() + (20 if self.yscroll else 4)
        height = self.content_frame.winfo_height() + (20 if self.xscroll else 4)
        self.config(width=width, height=height)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def __build_separator_lines(self, max_row, max_column):
        # horizontal lines
        self.horizontal_lines = []
        for i in range(0, max_row * 2 + 1, 2):
            f = tk.Frame(self.content_frame, height=self.line_with, bg=self.line_color)
            f.grid(row=i, column=0, columnspan=max_column * 2, sticky=tk.EW)
            f.lower()
            self.horizontal_lines.append(f)

        # vertical lines
        self.vertical_lines = []
        for j in range(0, max_column * 2 + 1, 2):
            f = tk.Frame(self.content_frame, width=self.line_with, bg=self.line_color)
            f.grid(row=0, column=j, rowspan=max_row * 2, sticky=tk.NS)
            f.lower()
            self.vertical_lines.append(f)

    def __coordinate_from_event(self, event):
        xs = [line.winfo_rootx() for line in self.vertical_lines]
        ys = [line.winfo_rooty() for line in self.horizontal_lines]
        x, y = event.x_root, event.y_root
        row, column = -1, -1
        for i, y_ in enumerate(ys):
            if y < y_:
                row = i - 1
                break
        for i, x_ in enumerate(xs):
            if x < x_:
                column = i - 1
                break
        return (row, column) if row >= 0 and column >= 0 else None

    def bind_cell(self, event, fn, master=None):
        """
        :param event: <Button-3>, <Double-Button-1>
        :param fn: fn(event, row, column)
        :param master: the root
        """

        def _callback(event):
            coor = self.__coordinate_from_event(event)
            if coor:
                fn(event, *coor)

        master = master if master else self.master
        master.bind(event, _callback)


def test_complicated():
    root = tk.Tk()
    table = Table(root, xscroll=False, yscroll=True)
    table.pack(fill=tk.BOTH, expand=True)

    words = "In first quarter 2018, the Company repurchased 50.6 million shares of its common stock".split()
    for idx, w in enumerate(words):
        table.add_item(w, row=0, column=idx)

    for row in range(1, len(words) - 1):
        for col in range(1, len(words) - 1, 2):
            c = tk.Checkbutton(table.content_frame, text="test")
            # c = tk.Button(table.content_frame, text="asdf")
            table.add_item(c, row=row, column=col, rowspan=1, columnspan=2, sticky=tk.NSEW)

    table.complete()
    root.mainloop()


def test_simple():
    import numpy as np
    root = tk.Tk()
    table = Table(root, xscroll=True, yscroll=True).load_data(np.random.randn(10, 6))
    table.pack(fill=tk.BOTH, expand=True)
    table.bind_cell("<Double-Button-1>", lambda event, r, c: print(r, c))
    root.mainloop()


if __name__ == "__main__":
    # test_complicated()
    test_simple()
