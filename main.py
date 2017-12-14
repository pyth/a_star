#!/bin/python

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

import math
from enum import Enum
from time import sleep
from random import randint


class NodeType(Enum):
    NORMAL = 0
    START = 1
    GOAL = 2
    WAYPOINT = 3




class Node:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas

        self.type = NodeType.NORMAL
        self.x = x
        self.y = y
        self.size = size
        self.difficulty = randint(0, 10)

        self.parent = None

        """cost from start node"""
        self.g_cost = -1
        """cost to goal node"""
        self.h_cost = -1
        """g_cost + h_cost"""
        self.f_cost = -1

        color = "#" + 3 * ("%02x" % int(255 - self.difficulty * 25.5))

        self.pic = self.canvas.create_polygon(self.x * self.size, self.y * self.size,\
                                              self.x * self.size, self.y * self.size + self.size,\
                                              self.x * self.size + self.size, self.y * self.size + self.size,\
                                              self.x * self.size + self.size, self.y * self.size,\
                                              fill = color, outline = "black")


    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


    def set_tint(self, color):
        try:
            rgb = self.canvas.winfo_rgb(color)
            r = max(int(rgb[0] / 256.0 - self.difficulty * 25.5), 15)
            g = max(int(rgb[1] / 256.0 - self.difficulty * 25.5), 15)
            b = max(int(rgb[2] / 256.0 - self.difficulty * 25.5), 15)
            col = ("#" + 3 * "%02x") % (r, g, b)
            self.canvas.itemconfig(self.pic, fill = col)
            self.canvas.update()
        except:
            pass


    def set_color(self, color):
        try:
            self.canvas.itemconfig(self.pic, fill = color)
            self.canvas.update()
        except:
            pass


    def update_cost(self, parent, goal):
        if self.h_cost == -1:
            self.h_cost = ((self.x - goal.x) ** 2 + (self.y - goal.y) ** 2) ** 0.5 * 4
        g_cost = parent.g_cost + self.difficulty
        if self.g_cost < 0 or g_cost < self.g_cost:
            self.parent = parent
            self.g_cost = g_cost
            self.f_cost = self.g_cost + self.h_cost




class Field(tk.Tk):
    def __init__(self, num_nodes):
        tk.Tk.__init__(self)

        """all nodes"""
        self.nodes = []
        """seen nodes"""
        self.open_set = []
        """visited nodes"""
        self.closed_set = []

        self.title("A*       PRESS SPACE TO START!")
        self.geometry("+50+50")
        self.resizable(False, False)
        self.bind("<Escape>", self.quit)
        self.bind("<space>", self.solve)
        self.bind("<Button-1>", self.onclick)
        self.protocol("WM_DELETE_WINDOW", self.quit)

        width = self.winfo_screenheight() * 0.9
        height = self.winfo_screenheight() * 0.9
        self.canvas = tk.Canvas(self, bg = "white", width = width, height = height)
        self.canvas.pack()

        self.num_nodes = num_nodes
        self.cell_size = float(width) / self.num_nodes
        for x in range(self.num_nodes):
            self.nodes.append([])
            for y in range(self.num_nodes):
                self.nodes[x].append(Node(self.canvas, x, y, self.cell_size))

        self.start = self.nodes[randint(0, self.num_nodes - 1)][randint(0, self.num_nodes - 1)]
        self.start.set_color("red")
        self.start.g_cost = 0
        self.start.type = NodeType.START
        self.open_set.append(self.start)

        goal = (randint(0, self.num_nodes - 1), randint(0, self.num_nodes - 1))
        while self.start.x == goal[0] and self.start.y == goal[1] or ((self.start.x - goal[0]) ** 2 + (self.start.y - goal[1]) ** 2) ** 0.5 < 0.6 * num_nodes:
            goal = (randint(0, self.num_nodes - 1), randint(0, self.num_nodes - 1))

        self.goal = self.nodes[goal[0]][goal[1]]
        self.goal.set_color("green")
        self.start.f_cost = 0
        self.goal.type = NodeType.GOAL

        #self.loop()
        #self.solve()


    def get_node(self, x, y):
        return self.nodes[math.floor(x / self.cell_size)][math.floor(y / self.cell_size)]


    def onclick(self, event):
        #self.solve()
        pass


    def solve(self, event = None):
        self.unbind("<space>")
        node = None
        while True:
            if len(self.open_set) == 0:
                break

            node = self.open_set[0]
            for e in self.open_set:
                if e.f_cost < node.f_cost:
                    node = e

            if node.type == NodeType.GOAL:
                break

            for x in range(-1, 2):
                for y in range(-1, 2):

                    #"""
                    #diagonal movement not allowed
                    if abs(x) == abs(y):
                        continue
                    """
                    #diagonal movement allowed
                    if x == 0 and y == 0:
                        continue
                    """

                    x_tmp = node.x + x
                    y_tmp = node.y + y

                    if x_tmp < 0 or x_tmp >= self.num_nodes or y_tmp < 0 or y_tmp >= self.num_nodes:
                        continue

                    child = self.nodes[x_tmp][y_tmp]
                    child.update_cost(node, self.goal)

                    if child not in self.open_set and child not in self.closed_set:
                        self.open_set.append(child)
                        if child.type != NodeType.START and child.type != NodeType.GOAL:
                            child.set_tint("yellow")
                            sleep(0.01)

            self.closed_set.append(node)
            self.open_set.remove(node)

        node = self.goal
        while node.parent.type != NodeType.START:
            node = node.parent
            node.set_tint("cyan")
            sleep(0.01)


    def loop(self):
        self._loop = self.after(math.floor(1000 / 60), self.loop)


    def quit(self, event = None):
        #self.after_cancel(self._loop)
        self.destroy()




if __name__ == "__main__":
    field = Field(100)
    field.mainloop()
