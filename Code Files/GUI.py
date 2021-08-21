from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
from content_aware_resizing import *
import cv2

"""Function to get the filename of a file"""
def openfilename():
    global filename
    filename= filedialog.askopenfilename(title='Image')
    return filename

"""Function to open an image"""
def open_img():
    c.delete("all")
    x = openfilename()
    img = Image.open(x)
    img = img.resize((250, 250), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    c.create_image(0,0,anchor=NW,image=img)
    panel = Label(root, anchor = CENTER, image=img)
    panel.image = img

"""Function to save an image as final(index)"""
def save_img():
    global img1
    global win
    global i

    r, g, b = img1.split()
    img1 = Image.merge("RGB", (b, g, r))
    m = np.array(img1)
    file="Saved/final"+str(i)+".jpg"
    cv2.imwrite(file,m)
    i+=1
    win=Toplevel()
    win.title("Success")
    Label(win,text= "The image has been saved successfully!").pack()
    Button(win, text='Ok', command=win.destroy).pack()


"""Function to reduce the height or width of an image"""
def resize_img():
    global img1
    global L

    c1.delete("all")

    img=cv2.imread(filename=filename)
    img=cv2.resize(img,(250,250))

    try:
        cd=CAIR(img,n1.get())
        if (radio.get() == 1):
            m = cd.reduceHeight()
            c1.delete("all")
            img1 = Image.fromarray(m)
            r, g, b = img1.split()
            img1 = Image.merge("RGB", (b, g, r))
            img2 = ImageTk.PhotoImage(img1)
            c1.create_image(0, 0, anchor=NW, image=img2)
            panelA = Label(root, anchor=W, image=img2)
            panelA.image = img2

        if(radio.get()==2):
            m=cd.reduceWidth()
            c1.delete("all")
            img1=Image.fromarray(m)
            r,g,b = img1.split()
            img1 = Image.merge("RGB", (b,g,r))
            img2 = ImageTk.PhotoImage(img1)
            c1.create_image(0, 0, anchor=NW, image=img2)
            panelA = Label(root, anchor=CENTER, image=img2)
            panelA.image = img2
    except :
        messagebox.showinfo("Error", "Please enter a floating point value")




root = Tk() #Main window
n1=DoubleVar() #Stores Height or Width
radio = IntVar() #Stores value of the radio button

"""Initializing the Canvas -> Original image & Resized image"""
c = Canvas(root,bg = "white",height = 250,width = 250)
c1=Canvas(root,bg = "white",height = 250,width = 250)

"""Initializing the labels"""
l0= Label(root, text = "Resize Dimensions").place(x=280, y=200)
l=Label(root, text = "WELCOME TO CAIR!",font=("Times New Roman",35)).pack()
l1=Label(root, text = "Content Aware Image Resizing performed using Dynamic Programming").place(x=150, y=60)
l2= Label(root, text = "Scale").place(x=270, y=290)

"""Initializing the radio buttons"""
R1 = Radiobutton(root, text="Resize Height", variable=radio, value=1).place(x=280, y=220)
R2= Radiobutton(root, text="Resize Width", variable=radio, value=2).place(x=280, y=240)

"""Value for height or width"""
e2 = Entry(root,textvariable=n1).place(x=270, y= 310)

"""Formatting the main window"""
root.title("CAIR Project")
root.geometry("670x550")
root.resizable(width=True, height=True)

"""Creating buttons and placing it"""
btn1 = Button(root, text='Open', command=open_img)
btn1.place(x=125, y=430)

btn2 = Button(root, text='Save',command=save_img)
btn2.place(x=515, y=430)

btn3 = Button(root, text='Resize', command=resize_img)
btn3.place(x=310,y=430)

"""Placing the canvas"""
c.pack(side="left")
c1.pack(side="right")
c.place(x=10,y=150)
c1.place(x=405,y=150)

"""Assigning global variables"""
filename=""
win=None
i=0

"""Running the main window"""
root.mainloop()

