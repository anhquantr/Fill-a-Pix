import numpy as np
from pysat.solvers import Glucose3
from itertools import combinations
from tkinter import *


def get_neighbours(m, i, j):
    return [m[x][y] for x in [i-1, i, i+1] for y in [j-1, j, j+1] if x in range(0, len(m)) and y in range(0, len(m[x]))]


def get_combinations(a, k):
    return [list(i) for i in combinations(a, k)]


def get_clauses(sample, i, j, k):
    if k > 0:
    # Đổi qua mảng string
      board = sample.astype(str)
      neighbours = get_neighbours(board, i, j)
      negative_neighbours = []
      for i in range(len(neighbours)):
          negative_neighbours.append("-" + neighbours[i])
      n = len(neighbours)
      clauses = get_combinations(neighbours, n-k+1) + get_combinations(negative_neighbours, k+1)
      return clauses


def read_file(file_name):  # read .txt file
    with open(file_name, 'r') as filename:
        l = []
        for i in filename.readlines():
            l.append([ii for ii in i.rstrip().split()])
        return l


def convert_matrix(a):  # convert character '-' into '0'
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] == '-':
                a[i][j] = '0'
    return a


def convert_to_int(a):  # convert matrix to integer
    for n, i in enumerate(a):
        for k, j in enumerate(i):
            a[n][k] = int(j)
    return a


if __name__ == '__main__':
    file = input("Enter file (ex: input.txt): ")
    try:
        arr = read_file(file)
        copy = read_file(file)
    except:
        print("File is not available!")
        exit()
    convert_to_int(convert_matrix(arr))

    col = len(arr)
    row = len(arr[0])
    puzzle = np.array(arr)
    sample = np.reshape(range(1, row * col + 1, 1), (row, col))
    clauses = []
    for i in range(row):
        for j in range(col):
            if puzzle[i][j] > 0:
                clauses += get_clauses(sample, i, j, puzzle[i][j])
    print('#clauses:', len(clauses))
    g = Glucose3()
    for it in clauses:
        g.add_clause([int(k) for k in it])
    if g.solve() == True:
        model = g.get_model()
        # print(model)
        result = []
        for i in range(row):
            temp = []
            for j in range(col):
                if sample[i][j] in model:
                    print('-', end=' ')
                    temp.append('- ')
                else:
                    print('x', end=' ')
                    temp.append('x ')
            print('')
            result.append(temp)
    else:
        print("Puzzle khong hop le")
        exit()


    # GUI
    win = Tk()
    win.title('Puzzle')
    for i in range(row):
        for j in range(col):
            if result[i][j] == "- ":
                if copy[i][j] == '-':
                    l1 = Label(win,text="",bg='green',height=1,width=2,borderwidth=1,relief='groove')
                    l1.grid(row=i,column=j,sticky="NSEW")
                else:
                    l1 = Label(win, text=copy[i][j], bg='green', height=1, width=2, borderwidth=1, relief='groove')
                    l1.grid(row=i, column=j, sticky="NSEW")
            else:
                if copy[i][j] == '-':
                    l1 = Label(win,text="", bg='red', height=1, width=2, borderwidth=1, relief='groove')
                    l1.grid(row=i, column=j, sticky="NSEW")
                else:
                    l1 = Label(win, text=copy[i][j], bg='red', height=1, width=2, borderwidth=1, relief='groove')
                    l1.grid(row=i, column=j, sticky="NSEW")
    win.mainloop()
