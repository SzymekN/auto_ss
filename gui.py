from tkinter import *
from tkinter.ttk import *
from turtle import position
from PIL import Image, ImageTk

#from ttkthemes import ThemedTk

root = Tk()

root.state('zoomed') #fullscreen

width = root.winfo_screenwidth()
height = root.winfo_screenheight()
#root.title('Codemy.com - Learn To Code!')
#root.iconbitmap('c:/gui/codemy.ico')

root.geometry(("%dx%d" % (width,height)))

# Create Clear Function
def clear():
	my_text.delete(1.5, END)

# darkMode
def darkstyle(root):
    ''' Return a dark style to the window'''
    
    style = Style(root)
    root.tk.call('source', 'azure dark/azure dark.tcl')
    style.theme_use('azure')
    style.configure("Accentbutton", foreground='white')
    style.configure("Togglebutton", foreground='white')
    return style

# Grab the text from the text box
def get_text():
	my_label.config(text=my_text.get(1.0, 3.0))

class Screenshoot(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.pack(fill=BOTH, expand=1)

        load = Image.open("Screenshot_1.png")
        load=load.resize((300,205),Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

darkstyle(root)
my_text = Text(root, width=width, height=10, font=("Helvetica", 16))
my_text.pack(pady=20,side=BOTTOM)

Screenshoot(root)

#button_frame = Frame(root)
#button_frame.pack()

#clear_button = Button(button_frame, text="Clear Screen", command=clear)
#clear_button.grid(row=0, column=0)

#get_text_button = Button(button_frame, text="Get Text", command=get_text)
#get_text_button.grid(row=0, column=1, padx=20)

my_label = Label(root, text='')
my_label.pack(pady=20)



root.mainloop()
