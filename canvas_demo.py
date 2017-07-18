import tkinter as tk
import random

# --- functions ---

def create_mines(how_many, canvas):

    bubbles = []
    w = canvas.winfo_reqwidth()
    h = canvas.winfo_reqheight()
    for __ in range(how_many):

        x = random.randint(0, w)
        y = random.randint(0, h)
        r = random.randint(5, 10)

        mine = canvas.create_oval(x-r, y-r, x+r, y+r)

        bubbles.append([mine, r])

    return bubbles




def moves_mines(canvas, bubbles):
    h = canvas.winfo_reqheight()
    for mine, r in bubbles:

        #canvas.move(mine, 0, -1)

        # get position
        x1, y1, x2, y2 = canvas.coords(mine)

        # change 
        y1 -= 1
        y2 -= 1

        # if top then move to the bottom
        if y2 <= 0:
            y1 = h
            y2 = y1 + 2*r

        # set position
        canvas.coords(mine, x1, y1, x2, y2)

    root.after(REFRESH_RATE, moves_mines, canvas, bubbles)



if __name__ == '__main__':

    root = tk.Tk()
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()
    REFRESH_RATE = 10 #ms

    bubbles = create_mines(50, canvas)

    root.after(REFRESH_RATE, moves_mines, canvas, bubbles)

    root.mainloop()