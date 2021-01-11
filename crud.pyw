from tkinter import*
from tkinter import messagebox
import sqlite3

root=Tk()
root.title("CRUD Interface")
root.resizable(0,0)
menuBar=Menu(root)
root.config(menu=menuBar)
myFrame=Frame(root)
myFrame.grid()
myFrame2=Frame(root)
myFrame2.grid()
# variables
buttons_width=7
id_number=IntVar()
username=StringVar()
password=StringVar()

# functions
def bbddConnect(): #tested
    try:
        myConex=sqlite3.connect("Users")
        myCursor=myConex.cursor()
        myCursor.execute('''CREATE TABLE USER_DATA(
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        USER_NAME VARCHAR(20),
        PASSWORD VARCHAR(20),
        BIOGRAPHY VARCHAR(100))
        ''')
    except:
        messagebox.showwarning("Warning","The database does already exist")

def bbddExit(): #tested
    valor=messagebox.askokcancel("Exit", "Are you sure you want to exit?")
    if valor==True:
        root.destroy()
    else:
        pass

def clearFields(): #tested
    username.set("")
    password.set("")
    biographyText.delete(1.0, END)

def crudCreate(): #tested
    myConex=sqlite3.connect("Users")
    myCursor=myConex.cursor()
    if username.get()=="" or password.get()=="":
        messagebox.showwarning("Error", "There are empty fields")

    else:
        try:
            myCursor.execute("INSERT INTO USER_DATA VALUES(NULL,'"+username.get()+"','"+password.get()+"','"+biographyText.get(1.0, END)+"')")
            myConex.commit()
            messagebox.showinfo("Database", "You have been succesfully registered")
            id_number.set(0)
            username.set("")
            password.set("")
            biographyText.delete(1.0, END)
        except:
            messagebox.showwarning("Error", "An error has occured, please try again. If the problem continues contact the developer")

def crudRead(): #tested
    myConex=sqlite3.connect("Users")
    myCursor=myConex.cursor()
    myCursor.execute("SELECT * FROM USER_DATA WHERE ID=?", (id_number.get(),))
    theUser=myCursor.fetchall()
    for user in theUser:
        id_number.set(user[0])
        username.set(user[1])
        password.set(user[2])
        biographyText.insert(1.0, user[3])

    myConex.commit()

def crudUpload():
    myConex=sqlite3.connect("Users")
    myCursor=myConex.cursor()
    myCursor.execute("UPDATE USER_DATA SET USER_NAME='" + username.get() +
    "', PASSWORD='" + password.get() +
    "', BIOGRAPHY='"+biographyText.get(1.0, END)+
    "' WHERE ID=?",(id_number.get(),))
    myConex.commit()
    messagebox.showinfo("Database", "Succesfully Updated")
    id_number.set(0)
    username.set("")
    password.set("")
    biographyText.delete(1.0, END)

def crudDelete():
    myConex=sqlite3.connect("Users")
    myCursor=myConex.cursor()
    myCursor.execute("DELETE FROM USER_DATA WHERE ID=?", (id_number.get(),))
    myConex.commit()
    messagebox.showinfo("Database", "Succesfully deleted")

# menu
bbddMenu=Menu(menuBar, tearoff=0)
bbddMenu.add_command(label="Connect", command=bbddConnect)
bbddMenu.add_command(label="Exit", command=bbddExit)

deleteMenu=Menu(menuBar, tearoff=0)
deleteMenu.add_command(label="Clear fields", command=clearFields)

crudMenu=Menu(menuBar, tearoff=0)
crudMenu.add_command(label="Create", command=crudCreate)
crudMenu.add_command(label="Read", command=crudRead)
crudMenu.add_command(label="Update", command=crudUpload)
crudMenu.add_command(label="Delete", command=crudDelete)

helpMenu=Menu(menuBar, tearoff=0)
helpMenu.add_command(label="License")
helpMenu.add_command(label="About")

menuBar.add_cascade(label="Database", menu=bbddMenu)
menuBar.add_cascade(label="Delete", menu=deleteMenu)
menuBar.add_cascade(label="CRUD", menu=crudMenu)
menuBar.add_cascade(label="Help", menu=helpMenu)

# interface
idLabel=Label(myFrame, text="ID:")
idLabel.grid(row=0, column=0)
idEntry=Entry(myFrame, textvariable=id_number)
idEntry.config(justify=RIGHT)
idEntry.grid(row=0, column=1)

usernameLabel=Label(myFrame, text="USERNAME:")
usernameLabel.grid(row=1, column=0)
usernameEntry=Entry(myFrame, textvariable=username)
usernameEntry.config(justify=RIGHT)
usernameEntry.grid(row=1, column=1)

passwordLabel=Label(myFrame, text="PASSWORD:")
passwordLabel.grid(row=2, column=0)
passwordEntry=Entry(myFrame, textvariable=password)
passwordEntry.config(justify=RIGHT, show="*")
passwordEntry.grid(row=2, column=1)

biographyLabel=Label(myFrame, text="BIOGRAPHY:", anchor="ne")
biographyLabel.grid(row=3, column=0)
biographyText=Text(myFrame)
biographyText.config(height=5, width=15)
biographyText.grid(row=3, column=1)

scrollvert=Scrollbar(myFrame, command=biographyText.yview)
scrollvert.grid(row=3, column=2, sticky="nsew")

biographyText.config(yscrollcommand=scrollvert.set)

createButton=Button(myFrame2, text="CREATE", width=buttons_width, command=crudCreate)
createButton.grid(row=0, column=0)

readButton=Button(myFrame2, text="READ", width=buttons_width, command=crudRead)
readButton.grid(row=0, column=1)

uploadButton=Button(myFrame2, text="UPLOAD", width=buttons_width, command=crudUpload)
uploadButton.grid(row=0, column=2)

deleteButton=Button(myFrame2, text="DELETE", width=buttons_width, command=crudDelete)
deleteButton.grid(row=0, column=3)

root.mainloop()
