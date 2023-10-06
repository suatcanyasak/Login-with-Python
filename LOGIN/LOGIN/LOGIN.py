import tkinter as tk
from turtle import bgcolor
import bcrypt
import sqlite3
from tkinter import messagebox
from tkinter import ttk

class Main(tk.Tk):
    def __init__(self):
        super().__init__()  
        self.title("Desktop Application") 
        self.geometry("1680x960+100+40") 
        self.resizable(False,False)
        

        self.page_stack = [] 
        self.show_page(LoginPage)
    
    def show_page(self, page_class):
        
        if self.page_stack:
            current_page = self.page_stack[-1] 
            current_page.pack_forget()
        
        new_page = page_class(self)
        new_page.pack(expand=True, fill="both")
        
        self.page_stack.append(new_page)


class LoginPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        name_label = ttk.Label(self, text = "Username: ")
        name_label.place(x = 720, y = 300, width = 70, height = 30)
        
        self.username = ttk.Entry(self)
        self.username.place(x = 800, y = 300, width = 100, height = 30)
        
        self.password_label = ttk.Label(self, text = "Password: ")
        self.password_label.place(x = 720, y = 350, width = 70, height = 30)
        
        self.password = ttk.Entry(self, show = "*")
        self.password.place(x = 800, y = 350, width = 100, height = 30)
        
        self.style = ttk.Style()
        self.style.configure('TButton', background='light blue')  
        
        login_button = ttk.Button(text="Login", command=self.login, style="TButton")
        login_button.place(x=800, y=400, width=100, height=50)
    
    def verify_password(self, hashed, password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed)
        
    def hash_password(self, password):
      
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed
    
    def login(self):

        username1 = self.username.get()
        password1 = self.password.get()
    

        conn = sqlite3.connect(r"users.pdb") #A database path containing username and password must be entered.
        cursor = conn.cursor()
    

        cursor.execute("SELECT * FROM users WHERE username=?", (username1,))
        user = cursor.fetchone()
    

        conn.close()
    

        if user:

            hashed = user[2]

            if self.verify_password(hashed, password1):
                messagebox.showinfo("Logged In", "Welcome")
            else:
                messagebox.showerror("Login Failed", "Invalid Password")
        else:
            messagebox.showerror("Login Failed", "Invalid Username")

if __name__ == "__main__":
    app = Main()
    app.mainloop()  