import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame


root = tk.Tk()

canvas1 = tk.Canvas(root, width=800, height=300)
canvas1.pack()

label1 = tk.Label(root, text='Airbnb Database')
label1.config(font=('Arial', 20))
canvas1.create_window(400, 50, window=label1)


button1 = tk.Button(root, text='Select Database ', command=None, bg='palegreen2', font=('Arial', 11, 'bold'))
canvas1.create_window(400, 200, window=button1)


xAxis = [float(1),float(2),float(3)]
yAxis = [float(1),float(2),float(3)]

# Pyplot
figure1 = plt.Figure(figsize=(5,4), dpi=100)
ax1 = figure1.add_subplot(111)
ax1.scatter(xAxis,yAxis, color = 'b')
scatter1 = FigureCanvasTkAgg(figure1, root)
scatter1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)
ax1.legend(['Pareto front'])
ax1.set_xlabel(r'$f_1(x)$')
ax1.set_ylabel(r'$f_2(x)$')
ax1.set_title(r'Sample Scatter Plot')


if __name__ == "__main__":

    data1 = {'Suburb': ['test1','test2','test3','test4','test5'],
             'Price': [45000,42000,52000,49000,47000]
            }
    df1 = DataFrame(data1,columns=['Suburb','Price'])

    root.mainloop()