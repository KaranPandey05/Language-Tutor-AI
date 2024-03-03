import tkinter as tk
import subprocess

def french(voice_id, content):
    subprocess.Popen(["python", "C:\Python Projects\Hackaton\AIGUI.py", voice_id, content])  

def english(voice_id, content):
    subprocess.Popen(["python", "C:\Python Projects\Hackaton\MainAIENG.py", voice_id, content])  

def german(voice_id, content):
    subprocess.Popen(["python", "C:\Python Projects\Hackaton\MainAIGER.py", voice_id, content])  

def create_start_menu():
    start_menu = tk.Tk()
    start_menu.title("Start Menu")
    start_menu.geometry("1280x720")
    start_menu.resizable(False, False)

    start_menu.config(bg="#2C3E50")  # Set background color of the window

    title_label = tk.Label(start_menu, text="Language Learning Assistant", font=("Arial", 24), fg="white", bg="#2C3E50")
    title_label.pack(pady=20)

    # Customizing button style with darker colors
    button_style = {
        "font": ("Arial", 16),
        "width": 20,
        "height": 3,
        "bg": "#34495E",  # Darker color
        "fg": "white",    # White text color
        "borderwidth": 2,
        "relief": "groove",  # Button border style
        "cursor": "hand2",   # Hand cursor on hover
        "activebackground": "#2C3E50",  # Slightly lighter color on click
        "activeforeground": "white",     # White text color on click
    }

    french_button = tk.Button(start_menu, text="French", command=lambda: french('Isabelle', "You are a French language teacher. You will teach the user French. Since the user is an English speaker, you should talk in English. Only talk in French when translating something."), **button_style)
    french_button.pack(pady=10)

    english_button = tk.Button(start_menu, text="English", command=lambda: english('Kajal', "You are an English language teacher."), **button_style)
    english_button.pack(pady=10)

    german_button = tk.Button(start_menu, text="German", command=lambda: german('Daniel', "You are a German language tutor. You will teach the user German. Since the user is an english speaker, you should talk in english. Only talk in German when translating something."), **button_style)  
    german_button.pack(pady=10)

    start_menu.mainloop()


if __name__ == "__main__":
    create_start_menu()
