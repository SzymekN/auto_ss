from email.mime import image
from re import T
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


class app:

    def load_images(self, image_frame):

        px, py = 5, 5

        image1 = Image.open("ss2.png")
        image1.thumbnail((1920/4 - 2*px, 1080/3 - 2*py))
        self.photo1 = ImageTk.PhotoImage(image1)
        prevous_ss = Label(image_frame, image=self.photo1)
        prevous_ss.grid(sticky=E+W+S, padx = px, row=0, column=0, rowspan=3)

        image2 = Image.open("ss1.png")
        image2.thumbnail((1920/2 - 2*px, 1080/2 - 2*py))
        self.photo2 = ImageTk.PhotoImage(image2)
        current_ss = Label(image_frame, image=self.photo2)
        current_ss.grid(sticky=E+W, row=0, column=1, rowspan=4)

        image3 = Image.open("ss2.png")
        image3.thumbnail((1920/4 - 2*px, 1080/3 - 2*py))
        self.photo3 = ImageTk.PhotoImage(image3)
        next_ss = Label(image_frame, image=self.photo3)
        next_ss.grid(sticky=E+W+S, padx = px, row=0, column=2,rowspan=3)


    def build_app(self):
        root = Tk()
        root.title("Auto_ss")
            # width = root.winfo_screenwidth()
            # height = root.winfo_screenheight()
        self.width, self.height = 1920, 1080
            #root.title('Codemy.com - Learn To Code!')
            #root.iconbitmap('c:/gui/codemy.ico')

        style = Style(root)
        root.tk.call('source', 'azure dark/azure dark.tcl')
        style.theme_use('azure')
        style.configure("Accentbutton", foreground='white')
        style.configure("Togglebutton", foreground='white')

        px,py = 5,5

        root.geometry(("%dx%d" % (self.width,self.height)))
        image_frame = Frame(root, height=self.height/2-2*py, width=self.width)
        image_frame.grid_propagate(False)
        self.load_images(image_frame)


        options_frame = Frame(image_frame, height=self.height / 2 / 4, width=self.width / 3)

        frequency_label = Label(options_frame, text="Frequency: ")
        freq = StringVar()
        freq.set("95%")
        frequency_entry = Entry(options_frame, textvariable=freq)
        frequency_label.grid(row=0,column=0)
        frequency_entry.grid(row=0,column=1)

        delay_label = Label(options_frame, text="Delay: ")
        delay_time = StringVar()
        delay_time.set("1s")
        delay_entry = Entry(options_frame, textvariable=delay_time)
        delay_label.grid(row=1,column=0)
        delay_entry.grid(row=1,column=1)

        options_frame.grid(sticky=W,column=2, row=3, padx=5)

        image_frame.grid(row=0, column=0,pady=25)

        button_frame = Frame(root, height=self.height/10-2*py, width=self.width)

        previous_btn = Button(button_frame, text="Previous")
        previous_btn.grid(padx =px, pady=py, row=0, column=0)

        next_btn = Button(button_frame, text="Next")
        next_btn.grid(padx =px, pady=py, row=0, column=1)

        previous_btn = Button(button_frame, text="Resize")
        previous_btn.grid(padx =px, pady=py, row=0, column=2)

        next_btn = Button(button_frame, text="Screenshot")
        next_btn.grid(padx =px, pady=py, row=0, column=3)

        del_btn = Button(button_frame, text="Delete")
        del_btn.grid(padx =px, pady=py, row=0, column=4)

        previous_btn = Button(button_frame, text="Start")
        previous_btn.grid(padx =px, pady=py, row=0, column=5)

        next_btn = Button(button_frame, text="Stop")
        next_btn.grid(padx =px, pady=py, row=0, column=6)

        button_frame.grid(row=1, column=0)

        text_frame = Frame(root, height= self.height / 2 , width=self.width-2*px)
        text_frame.columnconfigure(0,weight=10)
        text_frame.grid_propagate(False)
        text_box = Text(text_frame)
        text_box.grid(sticky=W+E)
        text_frame.grid(row=2,column=0, pady=25)

        root.mainloop()

aplikacja = app()
aplikacja.build_app()

