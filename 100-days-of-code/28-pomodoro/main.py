import tkinter as tk

class Pomodoro(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # resources
        self.fg: str = "#9bdeac"
        self.bg: str = "#f7f5dd"
        self.accent_hi: str = "#e7305b"
        self.accent_lo: str = "#e2979c"
        self.font_name: str = "Courier"
        self.font: tuple = (self.font_name, 35, 'bold')
        self.check_mark_char: str = '✓'
        self.check_box_char: str = '-'
        self.image = tk.PhotoImage(file='tomato.png')
        self.work_min: int = 25
        self.short_break_min: int = 5
        self.long_break_min: int = 15

        # display elements
        self.canvas = self.create_canvas()
        self.start_button = self.create_button('Start', self.start_timer)
        self.reset_button = self.create_button('Reset', self.reset_timer)

        # timer
        self.time_int: int = None
        self.time_string: str = None
        self.active: bool = None
        self.on_break: bool = None
        self.progress_counter: int = None
        self.progress_string: str = None
        self.timer_text = None
        
        self.label = tk.Label(text='', fg=self.fg, bg=self.bg, font=self.font)
        self.timer_text = self.canvas.create_text(100, 130, text='',fill='white', font=self.font)
        self.progress = self.progress = tk.Label(text='', fg=self.fg, bg=self.bg, font=self.font)

        self.reset_timer()
        self.render_layout()

    def create_canvas(self):
        canvas = tk.Canvas(width=200, height=224, bg=self.bg, highlightthickness=0)
        canvas.create_image(100,112,image=self.image)
        return canvas

    def create_button(self, text, command):
        return tk.Button(self.master, text=text, bg=self.bg, highlightbackground=self.bg, command=command)

    def render_layout(self):
        self.master.title("Pomodoro")
        self.master.config(padx=100, pady=50, bg=self.bg)
        self.label.grid(column=1, row=0)
        self.canvas.grid(column=1, row=1)
        self.start_button.grid(column=0, row=2)
        self.reset_button.grid(column=2, row=2)
        self.progress.grid(column=1, row=3)
        self.canvas.itemconfig(self.timer_text, text=self.time_string)

    def format_time(self):
        minute = str(self.time_int // 60)
        second = str(self.time_int % 60)
        pad_minute = minute.rjust(2, '0')
        pad_second = second.rjust(2, '0')
        self.time_string = f"{pad_minute}:{pad_second}"

    def reset_timer(self):
        self.active = False
        self.on_break = False

        self.progress_counter = 0
        self.update_progress()

        self.time_int = self.work_min * 60
        self.format_time()
        self.canvas.itemconfig(self.timer_text, text=self.time_string)
        self.label.config(text="Press Start")
        self.start_button.configure(text='Start', command=self.start_timer)

    def start_timer(self):
        self.update_labels()
        self.start_button.configure(text='Pause', command=self.pause_timer)
        self.active = True
        self.run_timer()
            
    def pause_timer(self):
        self.start_button.configure(text='Start', command=self.start_timer)
        self.active = False

    def run_timer(self):
        self.canvas.itemconfig(self.timer_text, text=self.time_string)
        if not self.active:
            return
        if self.time_int > 0:
            self.time_int -= 1
            self.format_time()
            self.master.after(1000, self.run_timer)
        else:
            self.timer_complete()

    def timer_complete(self):
        if self.on_break:
            self.time_int = self.work_min * 60
        else:
            self.progress_counter += 1
            if self.progress_counter < 5:
                self.update_progress()
                self.time_int = self.short_break_min * 60
            else:
                self.time_int = self.long_break_min * 60
                self.progress_counter = 0
        self.on_break = not self.on_break
        self.update_labels()
        self.run_timer()

    def update_labels(self):
        if self.on_break:
            self.label.config(text="Break")
            self.update_progress() 
        else:
            self.label.config(text="Work")

    def update_progress(self):
        self.break_counter_string = ' ' + f"{self.check_mark_char} " * self.progress_counter + f"{self.check_box_char} " * (5 - self.progress_counter)
        self.progress['text'] = self.break_counter_string


def main():
    root = tk.Tk()
    app = Pomodoro(root)
    app.mainloop()

if __name__ == "__main__":
    main()