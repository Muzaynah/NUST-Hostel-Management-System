#write code test
#write Code maheen test



#write code isra testtttttts

#hi isra

from tkinter import *
import time
from PIL import Image,ImageTk

root =Tk()

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

# def signIn():
#     username=user.get()
#     pw=password.get()

#     if(username == 'admin' and pw == '1234' ):
        

#image -----------------------------------------------
loginImg = Image.open('hostel.png')
resize = loginImg.resize((500,358))
resizedLoginImg = ImageTk.PhotoImage(resize)
yLoc = window_height/2 - (358/2)
xLoc = 100
Label(root,image=resizedLoginImg,bg='white').place(x=xLoc,y=yLoc)

#login frame------------------------------------------
loginFrame = Frame(root,width=350,height=350,bg='white')
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

user=Entry(loginFrame,width=30,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
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

password=Entry(loginFrame,width=30,fg='black',border=0,bg='white',font=('Microsoft YaHei UI Light',11))
password.place(x=30,y=150)
password.insert(0,'Password')
password.bind('<FocusIn>', on_enter)
password.bind('<FocusOut>', on_leave)

Frame(loginFrame,width=295,height=2,bg='black').place(x=25,y=177)

#button ---------------------------------------------
Button(loginFrame,width=39,pady=7,text='Sign In',bg='#408eed',fg='white',border=0,command=signIn).place(x=35,y=220)


####################################################
root.mainloop()
