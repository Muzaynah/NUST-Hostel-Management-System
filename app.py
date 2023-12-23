#write code test
#write Code maheen test



#write code isra testtttttts

#hi isra

from tkinter import *
import time
from PIL import Image,ImageTk

root =Tk() #main screen

page1 = Frame(root) #the login page
page2 = Frame(root) #admin page
page3 = Frame(root) #student page

page1.grid(row=0,column=0,sticky=NSEW)
page2.grid(row=0,column=0,sticky=NSEW)
page3.grid(row=0,column=0,sticky=NSEW)

for frame in (page1, page2, page3):
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    frame.grid(row=0, column=0, sticky="nsew")

page1.configure(bg='white')

# lb1 = Label(page1,text='page 1')
# lb1.pack(pady=20)
lb2 = Label(page2,text='page 2/admin')
lb2.pack(pady=20)
lb3 = Label(page3,text='page 3/student')
lb3.pack(pady=20)

 #putting login page on top

# variables for screen width, height, x and y offsets, and computer screen size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
print(screen_height,screen_width)
window_height = 600
window_width = 1200
window_offsetx = 50
window_offsety = 20

root.title('NUST Hostel Management System')
root.config(bg='white')
root.geometry(f'{window_width}x{window_height}+{window_offsetx}+{window_offsety}')
root.iconbitmap('nust_logo.ico')
root.resizable(False,False)

# when sign in pressed -------------------------------
def signIn():
    username=user.get()
    pw=password.get()

    if(username == 'admin' and pw == '1234' ):
        page2.tkraise()
    elif(username =='user' and pw == '1234'):
        page3.tkraise()

#image -----------------------------------------------
loginImg = Image.open('hostel.png')
resize = loginImg.resize((500,358))
resizedLoginImg = ImageTk.PhotoImage(resize)
yLoc =  150    #window_height/2 - (358/2) = which is 121
xLoc = 100
Label(page1,image=resizedLoginImg,bg='white').place(x=xLoc,y=yLoc)

#login frame------------------------------------------
loginFrame = Frame(page1,width=350,height=350,bg='white')
loginFrame.place(x=650,y=150)

heading=Label(loginFrame,text='Sign In',fg='#408eed',bg='white',font=('Microsoft YaHei UI Light',23,'bold'))
heading.place(x=100,y=5)

#username --------------------------------------------

def on_enter(e):
    name=user.get()
    if(name=='Username'):
        user.delete(0,'end')
def on_leave(e):
    name=user.get()
    if name =='':
        user.insert(0,'Username')

user=Entry(loginFrame,width=35,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
user.place(x=30,y=80)
user.insert(0,'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(loginFrame,width=295,height=2,bg='black').place(x=25,y=107)

#password ------------------------------------------\

def on_enter(e):
    pw=password.get()
    if(pw=='Password'):
        password.delete(0,'end')
def on_leave(e):
    pw=password.get()
    if pw =='':
        password.insert(0,'Password')

password=Entry(loginFrame,width=35,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
password.place(x=30,y=150)
password.insert(0,'Password')
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)

Frame(loginFrame,width=295,height=2,bg='black').place(x=25,y=177)

#button ---------------------------------------------
Button(loginFrame,width=39,pady=7,text='Sign In',bg='#408eed',fg='white',border=0,command=signIn).place(x=35,y=220)

####################################################
page1.tkraise()
root.mainloop()
