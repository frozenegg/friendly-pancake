import tkinter as tk

class EmptyUI(tk.Frame):
	def __init__(self, master=None):
		tk.Frame.__init__(self, master)

		self.master.title('Hello World')

		self.c = tk.Canvas(self, width=240, height=240, highlightthickness=0)
		self.c.pack()


f = EmptyUI()
f.pack()
f.mainloop()