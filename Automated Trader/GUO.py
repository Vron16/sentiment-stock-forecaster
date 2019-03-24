from tkinter import *

root = Tk()  # root is main window


def run(event):
    print("AutoTrader running...")

def stop(event):
    print("AutoTrader stopped.")

photo = PhotoImage(file=r"C:\Users\Asmaa Hasan\PycharmProjects\untitled\kash.PNG")
Photo_label = Label(root, image=photo)
Photo_label.grid(row=0,column=0)

AT_label = Label(root, text="AutoTrader Mode", bg="red", fg="white")
AT_label.grid(row=1,column=0)
Balance_label = Label(root, text="ENTER BALANCE")
Stock_label = Label(root, text="ENTER STOCK")

Balance_label.grid()
entry_1 = Entry(root)
entry_1.grid()

Stock_label.grid()
entry_2= Entry(root)
entry_2.grid ()

button1 = Button(text="RUN", fg="red")

button2 = Button( text="END", fg="blue")

button1.bind("<Button-1>", run)
button2.bind("<Button-1>", stop)

button1.grid()
button2.grid()
c = Checkbutton(root, text="Notify me when session is over")
c.grid()

root.mainloop()