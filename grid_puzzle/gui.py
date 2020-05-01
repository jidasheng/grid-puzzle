from tkinter import *
from tkinter import messagebox
from grid_puzzle.table import Table
from grid_puzzle.model import Model


class Window(Frame):

    # Define settings upon initialization. Here you can specify
    def __init__(self, master=None):
        # parameters that you want to send through the Frame class.
        Frame.__init__(self, master)

        # reference to the master widget, which is the tk window
        self.master = master

        self.model = Model()
        self.steps = IntVar()
        self.show_probs = IntVar()
        self._reset_data()

        self._create_menu()
        self._build_ui()

        self.on_game()

    def _reset_data(self):
        self.row = -1
        self.column = -1
        self.game_mode = True
        self.steps.set(0)
        self.labels = [[None for _ in range(4)] for _ in range(4)]

    # Creation of init_window
    def _build_ui(self):
        # changing the title of our master widget
        self.master.title("Grid Puzzle")
        self.pack(fill=BOTH, expand=True)
        self.pack()

        top = Frame(self)
        Label(top, text="Steps: ").pack(side=LEFT)
        top.grid(row=0, column=0, sticky=EW)

        Label(top, textvariable=self.steps).pack(side=LEFT)

        Checkbutton(top, text="Show Probabilities", variable=self.show_probs, command=self._load_data).pack(side=RIGHT)

        table = Table(self)
        table.grid(row=1, column=0)
        self.table = table
        self._load_data()

        self.table.bind_cell("<Button-1>", self.on_click, master=self.master)
        self.table.bind_cell("<Button-3>", self.on_right_click, master=self.master)

    def _create_menu(self):
        self.master.option_add('*tearOff', False)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)

        # create a menu
        event_menu = Menu(menu)
        menu.add_cascade(label="Game", menu=event_menu)
        event_menu.add_command(label="New Game", command=self.on_game)
        event_menu.add_command(label="New Solver", command=self.on_solver)

        popup = Menu(self, tearoff=False)
        popup.add_command(label='x', command=lambda: self.on_label(True))
        popup.add_command(label='-(None)', command=lambda: self.on_label(False))
        self.popup = popup

    def _load_data(self):
        obs = [
            [(row, col), self.labels[row][col]]
            for row in range(4) for col in range(4)
            if self.labels[row][col] is not None
        ]
        true_obs = [coord for coord, v in obs if v]
        false_obs = [coord for coord, v in obs if not v]
        probs = self.model.probabilities(true_obs=true_obs, false_obs=false_obs)
        self.table.clear()

        for row in range(4):
            for col in range(4):
                v = self.labels[row][col]
                if self.game_mode:
                    text = ("{:.3f}".format(probs[row][col]) if self.show_probs.get() else "?") \
                        if v is None else ("*" if v else " ")
                else:
                    text = "{:.3f}".format(probs[row][col]) if v is None else ("+" if v else "-")
                label = Label(self.table.content_frame, text=text, width=10, height=4)
                self.table.add_item(label, row=row, column=col, sticky=NSEW, ipadx=5)
        self.table.complete()

    def on_label(self, exist):
        self._label(self.row, self.column, exist)

        self.steps.set(self.steps.get() + 1)
        self._load_data()

    def _label(self, row, column, exist):
        self.labels[row][column] = exist

    def on_game(self):
        self._reset_data()
        self.game_mode = True
        self.group = self.model.random_group()
        self._load_data()

    def on_solver(self):
        self._reset_data()
        self.game_mode = False
        self._load_data()

    def on_click(self, event, row, column):
        # print("({}, {})".format(row, column))
        if self.game_mode and self.labels[row][column] is None:
            self.steps.set(self.steps.get() + 1)

            exist = (row, column) in self.group
            self._label(row, column, exist)
            if exist:
                exist_count = len([1 for row_labels in self.labels for label in row_labels if label is True])
                if exist_count == 4:
                    for row in range(4):
                        for col in range(4):
                            if self.labels[row][col] is None:
                                self.labels[row][col] = False

                    self._load_data()
                    messagebox.showinfo(title="You are win!")
                    return

            self._load_data()

    def on_right_click(self, event, row, column):
        # print("right: ({}, {})".format(row, column))
        if not self.game_mode:
            self.row = row
            self.column = column
            self.popup.post(event.x_root, event.y_root)


def main():
    root = Tk()
    # root.geometry("400x400")
    Window(root)
    root.mainloop()


if __name__ == '__main__':
    main()
