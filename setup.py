from cx_Freeze import setup, Executable

base = None    

executables = [Executable("app.py", base="Win32GUI", icon="icon.ico")]

packages = ["idna", "tkinter", "os", "ctypes"]
options = {
    'build_exe': {    
        'packages':packages,
    },    
}

setup(
    name = "Notesbook",
    options = options,
    version = "1.0",
    author="Ratius (John Memmott)",
    description = 'A simple text editor for basic tasks',
    executables = executables
)