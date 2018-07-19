import tkinter as tk
import time
count =1
text = 'abcd'
class authenticate():
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.label_ask = tk.Label(self.master, text='Give Your Pass Key To Proceed').grid(row=0)
        self.entry_passkey = tk.Entry(self.master)
        self.entry_passkey.grid(row=0, column=1)
        self.check_proceed = tk.Button(self.master, text='check', command=self.checkKey).grid(row=1,column=0)
    def checkKey(self):
        if self.entry_passkey.get() == text:
            self.label_ask = tk.Label(self.master, text='   Pass key correct you may proceed   ').grid(row=0)
            self.check_proceed = tk.Button(self.master, text='proceed', command=self.proceed).grid(row=1, column=0)
        else:
            self.label_ask = tk.Label(self.master, text='Pass key incorrect you cannot proceed').grid(row=0)
            self.check_proceed = tk.Button(self.master, text='Abort', command=self.master.destroy).grid(row=1, column=0)
    def proceed(self):
        self.master.withdraw()
        self.newWindow = tk.Toplevel(self.master)
        bb = myfunction(self.newWindow,self.master)

class myfunction():
    def __init__(self,master,grandmaster):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.name = tk.Label(self.master,text="First Name").grid(row=0, column=0)
        self.enter_name = tk.Entry(self.master)
        self.enter_name.grid(row=0, column=1)
        self.start = tk.Button(self.master, text='Begin', command=self.action).grid(row=1, column=0)
        self.finish = tk.Button(self.master, text='finish', command=grandmaster.destroy).grid(row=1, column=1)
        self.labelText = tk.StringVar()
    def action(self):
        #self.labelText.set("First Name cccc")
        self.name = tk.Label(self.master, text="Your Action")




if __name__ == '__main__':
    root = tk.Tk()
    icon = tk.PhotoImage(file='F:/untitled/index.gif')
    root.tk.call('wm', 'iconphoto', root._w, icon)
    root.title('Checking Tkinter')
    alert = authenticate(root)
    root.mainloop()
"""
def showfields():
    global count
    count+=1
    global text
    text =text + text+ str(count)
    print(e1.get())
    print(e2.get())
    tk.Label(master, text=text ).grid(row=3, column=1)
master = tk.Tk()
icon = tk.PhotoImage(file='F:/untitled/index.gif')
master.tk.call('wm', 'iconphoto', master._w, icon)
master.title('Counting Seconds')
tk.Label(master, text='First Name').grid(row=0)
tk.Label(master, text='Last Name').grid(row=1)
e1 =tk.Entry(master)
e1.grid(row=0, column=1)
e2 = tk.Entry(master)
e2.grid(row=1, column=1)
tk.Button(master, text='Stop', width=25, command=master.destroy).grid(row=2, column=0)
tk.Button(master, text='Show', width=25, command=showfields).grid(row=2, column=1)
tk.Button(master, text='Show', width=25, command=showfields).grid(row=2, column=1)
tk.Label(master, text="Hello, world!").grid(row=3, column=1)
if __name__ == '__main__':
    master.mainloop()"""