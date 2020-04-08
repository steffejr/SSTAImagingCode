import tkinter as tk
from tkinter import simpledialog

application_window = tk.Tk()

PartID = simpledialog.askstring("Input", "What is the participant ID?",
                                parent=application_window)

VisitID = simpledialog.askinteger("Input", "What is the visit ID?",
                                 parent=application_window,
                                 minvalue=0, maxvalue=10)
application_window.destroy()