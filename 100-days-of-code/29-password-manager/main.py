import tkinter as tk
from tkinter import messagebox
import secrets
import string
import pyperclip
import json
from json.decoder import JSONDecodeError

class PasswordManager(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.db_file = './db.json'
        self.db = self.load_db()
        self.bg: str = "#fdffff"
        self.fg: str = "#090000"
        self.font_name: str = "Courier"
        self.font: tuple = (self.font_name, 15, 'normal')
        self.web_label: tk.Label = self.create_label('Website:')
        self.user_label: tk.Label = self.create_label('Username:')
        self.pass_label: tk.Label = self.create_label('Password:')
        self.web_input: tk.Entry = self.create_input(width=21)
        self.user_input: tk.Entry = self.create_input(width=39)
        self.pass_input: tk.Entry = self.create_input(width=21)

        self.search_button: tk.Button = self.create_button(text='Search', command=self.search_db, width=14)
        self.generate_button: tk.Button = self.create_button(text='Generate Password', command=self.generate_password, width=14)
        self.add_button: tk.Button = self.create_button(text='Add', command=self.add_password, width=36)

        self.image = tk.PhotoImage(file='logo.png')
        self.canvas = self.create_canvas()

        self.load_db()
        self.render_layout()

    def render_layout(self):
        self.master.title("Password Manager")
        self.master.config(padx=50, pady=50, bg=self.bg)
        self.canvas.grid(column=1, row=0)
        self.web_label.grid(column=0, row=1)
        self.web_input.grid(column=1, row=1)
        self.web_input.focus()
        self.search_button.grid(column=2, row=1)
        self.user_label.grid(column=0, row=2)
        self.user_input.grid(column=1, row=2, columnspan=2)
        self.user_input.insert(index=0, string='nathancurry@gmail.com')
        self.pass_label.grid(column=0, row=3)
        self.pass_input.grid(column=1, row=3)
        self.generate_button.grid(column=2, row=3)
        self.add_button.grid(column=1, row=4, columnspan=2)

    def create_canvas(self):
        canvas = tk.Canvas(width=200, height=200, bg=self.bg, highlightthickness=0)
        canvas.create_image(100,100,image=self.image)
        return canvas
    
    def create_label(self, text):
        return tk.Label(text=text, fg=self.fg, bg=self.bg, font=self.font, justify='right')

    def create_input(self, width):
        return tk.Entry(width=width, bg=self.bg, fg=self.fg, borderwidth=1, highlightthickness=1, highlightbackground=self.bg, highlightcolor=self.fg)

    def create_button(self, text, command, width=None):
        if width:
            return tk.Button(self.master, text=text, bg=self.bg, highlightbackground=self.bg, command=command, width=width)
        else:
            return tk.Button(self.master, text=text, bg=self.bg, highlightbackground=self.bg, command=command)

    def load_db(self):
        try:
            with open(self.db_file, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db: dict = {}
        except JSONDecodeError:
            self.db: dict = {}

    def write_db(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.db, f, indent=4)

    def search_db(self):
        search_string = self.web_input.get().lower()
        found = self.db.get(search_string)
        if found:
            messagebox.showinfo(title=f"{search_string}", message=f"Username: {found['username']}\nPassword: {found['password']}")
            pyperclip.copy(found['password'])
        else:
            messagebox.showwarning(title='Search', message=f"Not found: {search_string}")

    def generate_password(self):
        characters = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(characters) for i in range(16))
        self.pass_input.delete(0, 'end')
        self.pass_input.insert(0, password)
        pyperclip.copy(password)

    def save_password(self):
        website = self.web_input.get().strip().lower()
        username = self.user_input.get().strip()
        password = self.pass_input.get().strip()
        self.db[website] = {'username': username, 'password': password}

    def add_password(self):
        website = self.web_input.get().strip().lower()
        username = self.user_input.get().strip()
        password = self.pass_input.get().strip()
        if not website or not username or not password:
            messagebox.showerror(title="Incomplete", message='Please fill out all fields')
            return
        if website.lower() in self.db:
            confirm = messagebox.askokcancel(title=website, message=f"Overwrite existing entry?\nUsername: {username}\nPassword: {password}")
        else:
            confirm = messagebox.askokcancel(title=website, message=f"Save entry?\nUsername: {username}\nPassword: {password}")
        if confirm:
            self.save_password()
            self.write_db()


def main():
    root = tk.Tk()
    app = PasswordManager(root)
    app.mainloop()

if __name__ == "__main__":
    main()