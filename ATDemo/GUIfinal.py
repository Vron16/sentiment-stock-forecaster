# WebsiteTest.py - prototyping a website with multiple windows/frames in Tkinter GUI
from tkinter import *
import tkinter as tk  # python 3
from tkinter import font  as tkfont  # python 3
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import ATController as at

AT = at.AutomatedTrader(0.0, {})


class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        # container.pack(side="top", fill="both", expand=True)
        container.grid()
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid()
        button1 = tk.Button(self, text="Go to Account Info",
                            command=lambda: controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="GO AUTOTRADER Mode",
                            command=lambda: controller.show_frame("PageTwo"))
        # button1.pack()
        # button2.pack()
        button1.grid()
        button2.grid()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        def showbal():
            messagebox.showinfo("Balance", AT.print_balance())

        def withdraw():
            bal = entry_1.get()
            if float(bal) > AT.balance:
                messagebox.showinfo("Warning","Attempted to withdraw more than available Balance, please try again")
            else:
                AT.balance -= float(bal)
                messagebox.showinfo("Success", "withdrew from AutoTrade Balance")


        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.iconPath = r"kash.PNG"
        self.icon = ImageTk.PhotoImage(Image.open(self.iconPath))
        self.icon_size = Label(self)
        self.icon_size.image = self.icon
        self.icon_size.configure(image=self.icon)
        self.icon_size.grid()

        label = tk.Label(self, text="Account Info", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        label.grid()
        photo = tk.PhotoImage(file=r"kash.PNG")
        Photo_label = tk.Label(self, image=photo)
        Photo_label.grid(sticky="nsew")
        bal_label = Label(self, text="Withdraw Balance:")
        bal_label.grid()
        entry_1 = Entry(self)
        entry_1.grid()
        withdrawbutton = tk.Button(self, text="Withdraw",
                              command=lambda: withdraw())

        balbutton = tk.Button(self, text="Show Balance",
                              command=lambda: showbal())

        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        # button.pack()
        withdrawbutton.grid()
        balbutton.grid()
        button.grid()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        def run():
            print("AutoTrader has begun.")

        def stop():
            print("AutoTrader stopped.")
            print(AT.stock_portfolio.items())

        def get_Info():
            balance = entry_1.get()
            string_to_display = "Balance added is $" + balance
            AT.balance += float(balance)
            balance_label = Label(self)
            balance_label["text"] = string_to_display
            balance_label.grid()
            stock = entry_2.get()

            string_to_display = "AutoTrading for... " + stock
            time.sleep(1)
            string_to_display1 = "\nCollecting Sentiment..."
            time.sleep(1)
            string_to_display2 = "\nFetching Predictions..."

            stock_label = Label(self)
            stock_label["text"] = string_to_display1 + string_to_display2
            stock_label.grid()
            AT.search_stock_symbol(stock)
            stockprice = AT.get_stock_price(stock)
            AT.AutoTrade(520, stockprice, 362.2, stock)
            # time.sleep(5)
            # stock_label.grid_forget()
            # balance_label.grid_forget()
            string_to_display3 = "Autotrader has run\n"

            string_to_display5 = stock + "'s price is $" + str(stockprice) + "\n"
            string_to_display4 = "New Balance is $" + str(AT.balance)
            run_label = Label(self)
            run_label["text"] = string_to_display3 + string_to_display5 + string_to_display4
            run_label.grid()
        def get_stock():
            stock = entry_2.get()
            string_to_display = "AutoTrading for... " + stock
            stock_label = Label(self)
            stock_label["text"] = string_to_display
            stock_label.grid()

        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="This is page 2", font=controller.title_font)

        # "I was able to solve it by storing the image object."
        # https://stackoverflow.com/questions/50668071/how-to-display-image-on-the-tkinter-window
        self.iconPath = r"kash.PNG"
        self.icon = ImageTk.PhotoImage(Image.open(self.iconPath))
        self.icon_size = Label(self)
        self.icon_size.image = self.icon
        self.icon_size.configure(image=self.icon)
        self.icon_size.grid()

        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",
        #                   command=lambda: controller.show_frame("StartPage"))
        # button.pack()

        # '''canvas= Canvas(self,width=300,height=300)
        # img = ImageTk.PhotoImage(Image.open(r"C:\Users\Asmaa Hasan\PycharmProjects\untitled\kash.PNG"))
        # canvas.create_image(20,20,anchor=NW, image=img)
        # canvas.grid()'''

        # img = Label(self, image=photo)
        # img.grid(row=0, column=0)
        # AT_label = Label(tk, text="AutoTrader Mode", bg="red", fg="white")
        AT_label = Label(self, text="Welcome! Please enter an initial deposit for your AutoTrader account balance.\n")
        AT_label.grid()
        Balance_label = Label(self, text="Add Balance:")
        Stock_label = Label(self, text="Initial Stock Ticker:")

        # formatting
        Balance_label.grid()
        entry_1 = Entry(self)
        entry_1.grid()

        Stock_label.grid()
        entry_2 = Entry(self)
        entry_2.grid()

        button1 = tk.Button(self, text="RUN",
                            command=lambda: get_Info())
        button2 = tk.Button(self, text="STOP",
                            command=lambda: stop())
        button3 = tk.Button(self, text="Go to the start page",
                            command=lambda: controller.show_frame("StartPage"))

        button1.grid()
        button2.grid()
        button3.grid()
        # button4 = tk.Button (self, text="SELL")
        # button5 = tk.Button(self, text="BUY")
        # button6= tk.Button(self, text=" HOLD")

        ##button4.grid(row=11, column=3)
        # button5.grid(row=11, column=2)
        # button6.grid(row=11, column=1)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
