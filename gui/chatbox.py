import tkinter as tk
from tkinter import scrolledtext

class ChatBox(tk.Frame):
    def __init__(self, master=None,**kwargs):
        super().__init__(master, **kwargs)
        self.chat = scrolledtext.ScrolledText(self)
        self.text_entry = tk.Entry(self)
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_message)
        
        self.text_entry.pack(side="bottom", fill="x")
        self.submit_button.pack(side="bottom")
        self.chat.pack(side="top", fill="both", expand=True)
        self.texts = []

    def submit_message(self):
        message = self.text_entry.get()
        if message:
            self.texts.append(message)
            self.text_entry.delete(0, 'end')
        
if __name__ == '__main__':
    root = tk.Tk()
    chatbox = ChatBox(root)
    root.mainloop()