__version__ = "1.0"

import os
import ctypes
from tkinter import filedialog, Label, Toplevel, Menu, Tk, ttk, END, INSERT, SEL, SEL_FIRST, SEL_LAST, X, Listbox
from tkinter.scrolledtext import ScrolledText
import tkinter.messagebox as message_box

# Name of program
NAME = "Notesbook"
# Needed in order to display sharp on high-res monitors
ctypes.windll.shcore.SetProcessDpiAwareness(1)


# Function to display save warning
def is_saved_popup():
    return message_box.askquestion("Warning", "Would you like to save these changes to a file?")


# Unused Settings window
def settings():
    w = Toplevel(takefocus=True)
    w.geometry("300x400")
    w.wm_title("Settings")
    w.resizable(0, 0)
    title = Label(w, text="Settings", font=('Helvetica', 15), width=10, pady=10)
    title.pack(fill=X)
    button = ttk.Button(w, text="Close", command=w.destroy)
    button.pack(side='bottom', pady=20)


# About window
def about():
    # Put the help window in front of text window
    win = Toplevel(takefocus=True)
    win.grab_set()
    # Set size and undesirable and title
    win.geometry("450x250")
    win.resizable(0, 0)
    win.wm_title("About")
    # Create the title of the About window
    title = Label(win, text=NAME, font=('Helvetica', 30), width=10)
    title.pack(fill=X)
    # Create the text under the title
    title_sub = Label(win, text=("©", NAME, "2019"), font=('Helvetica', 8))
    title_sub.pack(fill=X)
    # Add some space between header and body
    space = Label(win, text="")
    space.pack(fill=X)
    # Add the body message of the About window
    text = Label(win, text=(NAME + ''' is a simple Text editor made in python.
        Please consider supporting me ♥
    '''))
    text.pack(fill=X)
    # Add a button to close the window
    button = ttk.Button(win, text="Close", command=win.destroy)
    button.pack(side='bottom', pady=20)


# Main window class
class Window(Listbox):

    # Initializes the variables and settings for the project. Finally
    # executes the create_menu for the menu bar, and the create_notepad
    # for the text window
    def __init__(self, master, **kw):
        # Sets master, or root
        super().__init__(master, **kw)
        self.master = master
        # Set some variables
        self.current_file_path = ''
        self.current_file_text = ''
        self.is_saved = True
        # Set up the context menu and the text box
        self.context_popup_menu = Menu(self.master, tearoff=0)
        self.text_window = ScrolledText(self.master, undo=True)
        self.text_window.focus()
        self.user_data = self.text_window.get('1.0', END + '-1c')
        # Name the window, icon, and start the create functions
        self.master.title(NAME)
        # self.master.iconbitmap('./tk/images/icon.ico')
        self.initiate_shortcuts()
        self.create_menu()
        self.create_notepad()
        self.create_context_menu()

    # Creates the context menu
    def create_context_menu(self):
        # Adds a command for button, separator for separator
        self.context_popup_menu.add_command(label="Undo", command=lambda: self.undo())
        self.context_popup_menu.add_command(label="Redo", command=lambda: self.redo())
        self.context_popup_menu.add_separator()
        self.context_popup_menu.add_command(label="Cut", command=lambda: self.text_window.event_generate("<<Cut>>"))
        self.context_popup_menu.add_command(label="Copy", command=lambda: self.text_window.event_generate("<<Copy>>"))
        self.context_popup_menu.add_command(label="Paste", command=lambda: self.text_window.event_generate("<<Paste>>"))
        self.context_popup_menu.add_separator()
        self.context_popup_menu.add_command(label="Delete", command=lambda: self.clear())
        self.context_popup_menu.add_separator()
        self.context_popup_menu.add_command(label="Select All", command=lambda: self.select_all())

    # Creates the top bar menu
    def create_menu(self):
        # Creating menu bar and adding it to master
        menu_bar = Menu(self.master)
        text = self.text_window
        # Telling root that menu_bar is the Window's menu
        self.master.config(menu=menu_bar)
        # Creating the File menu dropdown
        file_menu = Menu(menu_bar, tearoff=False)
        file_menu.add_command(label="New Document...", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open Document...", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save...", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save as...", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Quit", command=self.exit, accelerator="Ctrl+Q")
        # Adding it to the menu_bar
        menu_bar.add_cascade(label="File", menu=file_menu, underline=0)
        # Creating the Edit menu dropdown
        edit_menu = Menu(menu_bar, tearoff=False)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: text.event_generate("<<Cut>>"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: text.event_generate("<<Copy>>"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: text.event_generate("<<Paste>>"), accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=lambda: self.select_all(), accelerator="Ctrl+A")
        edit_menu.add_command(label="Delete", command=self.clear, accelerator="Del")
        # edit_menu.add_separator()
        # edit_menu.add_command(label="Settings...", command=settings, accelerator="Ctrl+S")
        # Adding it to the menu_bar
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        # Creating the Help menu
        help_menu = Menu(menu_bar, tearoff=False)
        help_menu.add_command(label="About...", command=about)
        # Adding it to the menu_bar
        menu_bar.add_cascade(label="Help", menu=help_menu)

    # Bind the shortcuts to their specified functions
    def initiate_shortcuts(self):
        self.master.bind("<KeyRelease>", lambda event: self.on_text_change())
        self.master.bind("<Control-n>", lambda event: self.new_file())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-s>", lambda event: self.save_file())
        self.master.bind("<Control-Shift-s>", lambda event: self.save_as_file())
        self.master.bind("<Control-q>", lambda event: self.exit())
        self.master.bind("<Control-z>", lambda event: self.undo())
        self.master.bind("<Control-y>", lambda event: self.redo())
        self.text_window.bind("<Control-a>", lambda event: self.select_all())
        # self.master.bind("<Control-s>", lambda event: settings())
        self.master.bind("<Button-3>", lambda event: self.right_click_popup(event))

    # Display context menu popup
    def right_click_popup(self, event):
        try:
            # Used +45 and + 12 to corner it
            self.context_popup_menu.tk_popup(event.x_root+45, event.y_root+12, 0)
        finally:
            self.context_popup_menu.grab_release()

    # Scaling the text_window to fit the screen
    def create_notepad(self):
        self.text_window.pack(fill="both", expand=True)

    # Returns the value of the text field
    def get_text_data(self):
        return self.text_window.get('1.0', END + '-1c')

    # Clears the text off the screen, resets the variables
    def clear_text(self):
        self.text_window.delete('1.0', END)
        self.current_file_path = ''
        self.current_file_text = ''

    # Called when typing, sets the is_saved variable
    def on_text_change(self):
        # If the text in the textbox is equal to the saved text in the variable
        # This is used when opening a file, changing something, then undoing that change
        if self.get_text_data() == self.current_file_text:
            self.is_saved = True
        else:
            # If the saved file exists or is valid
            if os.path.isfile(self.current_file_path):
                # Open the file, save it's data to this_file
                with open(self.current_file_path, "r") as f:
                    this_file = f.read()
                    # If this_file is equal to the same text in the textbox
                    # Used if no changes were made, and if they were, set to False
                self.is_saved = True if this_file == self.get_text_data() else False
            else:
                # If the data is not equal to variable, and no file, then changes
                # must have been made
                self.is_saved = False

    # MENU CONTROL FUNCTIONS

    # Clear current selection, erase the current file if saved
    def new_file(self):
        # If it's saved, clear it and set the file to saved
        if self.is_saved is True:
            self.clear_text()
            self.is_saved = True
        else:
            # Popup the saved popup
            popup_value = is_saved_popup()
            if popup_value == "yes":
                # Save the file, clear it and set the is_saved to True
                if self.save_file() is True:
                    self.clear_text()
                    self.is_saved = True
            elif popup_value == "no":
                # Don't save the file, but clear it and set the is_saved to True
                self.clear_text()
                self.is_saved = True
            else:
                # Something went wrong
                print("Error: new_file error")

    # Open a file if the current file is saved, then insert new file data
    def open_file(self):
        # If file is saved, open the open_file window
        if self.is_saved is True:
            self.open_file_popup()
        else:
            # Save the file, if it's saved, open the open_file window
            popup_value = is_saved_popup()
            if popup_value == "yes":
                if self.save_file() is True:
                    self.is_saved = True
                    self.open_file_popup()
            # Open the open_file window
            elif popup_value == "no":
                self.open_file_popup()
            else:
                # An error occurred
                print("Error: open_file error")

    # The function that displays the open_file popup
    def open_file_popup(self):
        # Gets old data from current file
        old_file = self.current_file_path
        # Opens the file location, stores it in file_name
        file_name = filedialog.askopenfilename(title="Open", filetypes=(("Text files", "*.txt"),
                                                                        ("All files", "*.*")))
        # If a file was actually selected, open it
        if file_name is not '':
            with open(file_name) as f:
                data = f.read()
            # Clear current text
            self.clear_text()
            # Set the path variable of the new file
            self.current_file_path = file_name if os.path.isfile(file_name) else old_file
            # Add the file data to the text_box
            self.text_window.insert(INSERT, data)
            # Add the file data to the variable
            self.current_file_text = data
            # is_saved is True
            self.is_saved = True

    # Save file, if file exists, overwrite it, otherwise, call save_as_file function
    def save_file(self):
        # If the file path exists
        if os.path.isfile(self.current_file_path):
            # Stores the current text data into the variable
            self.current_file_text = self.get_text_data()
            # Saves the data to the existing file (overwriting)
            with open(self.current_file_path, "w") as f:
                return True if f.writelines(self.get_text_data()) is True else False
        else:
            # File doesn't exist, call save_as_file
            if self.save_as_file() is True:
                return True

    # Saves file with asksaveasfile to open a save as window.
    def save_as_file(self):
        # Gets old file path
        old_file = self.current_file_path
        # Opens save_as window
        file_name = filedialog.asksaveasfilename(title="Save As", defaultextension=".txt",
                                                 filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        # Set current file path
        self.current_file_path = old_file if file_name is None else file_name

        # If the file_path already exists
        if os.path.isfile(self.current_file_path):
            # Copy the current text to the variable
            self.current_file_text = self.get_text_data()
            # Writes to the named file
            with open(self.current_file_path, "w") as f:
                f.writelines(self.get_text_data())
                return True
        else:
            # A file wasn't selected
            if file_name is '':
                print("Error: File is none")
                return False
            # Create a new file to store the data
            self.current_file_text = self.get_text_data()
            with open(file_name, 'w'):
                pass
            self.is_saved = True
            return True

    # Exit override command
    def exit(self):
        # If the file is saved, exit
        if self.is_saved is True:
            self.master.quit()
        else:
            # If the file is not saved, call the saved_popup
            popup_value = is_saved_popup()
            if popup_value == "yes":
                # Save and then quit
                if self.save_file() is True:
                    self.is_saved = True
                    self.quit()
            elif popup_value == "no":
                # Don't save, just quit
                self.master.quit()
            else:
                # An error occurred
                print("Error: open_file error")

    # Undo last action
    def undo(self):
        self.text_window.edit_undo()

    # Redo last action
    def redo(self):
        self.text_window.edit_redo()

    # Clear (delete) the selected text
    def clear(self):
        self.text_window.delete(SEL_FIRST, SEL_LAST)
        self.text_window.update()

    # Select the selected text (without new line)
    def select_all(self):
        self.text_window.tag_add(SEL, "1.0", END + '-1c')
        self.text_window.mark_set(INSERT, "1.0")
        self.text_window.see(INSERT)
        return 'break'


# Create the GUI

root = Tk()

Window = Window(root)
root.wm_protocol('WM_DELETE_WINDOW', Window.exit)

# Loop so it won't close
root.mainloop()
