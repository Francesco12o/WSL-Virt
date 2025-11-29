"""
Tkinter + Xming Wizard Setup Guide

Step 1: Install Python — Begin Your Journey
    - Download the latest Python installer: https://www.python.org/downloads/
    - During installation, check "Add Python to PATH" to unlock your coding powers.

Step 2: Install Xming — Harness Window Magic (for graphical output with WSL/SSH on Windows)
    - Download Xming from: https://sourceforge.net/projects/xming/
    - Complete installation and launch Xming. The 'X' icon in your system tray means your display magic is ready.

Step 3: Clone Your First GitHub Spellbook (Project)
    - Open your terminal (PowerShell, CMD, WSL, Bash).
    - Run: 
        git clone https://github.com/username/projectname.git
    - Step into the project:
        cd projectname

Step 4: Summon the Tkinter Wizard (Run the Script)
    - Be sure Xming is running if using WSL/SSH.
    - In your project directory, cast your spell:
        python tkinte-howto.py
    - Or replace with any wizard script from your project.

Step 5: Troubleshooting Curses
    - If faced with: _tkinter.TclError: no display name and no $DISPLAY environment variable
    - In Bash, conjure:
        export DISPLAY=:0
    - Then repeat your spell: python tkinte-howto.py

Step 6: Transform the Code — Make it Your Own
    - Edit and improve your script to customize your wizard GUI!
    - Add buttons, dialogs, effects as desired.

Step 7: Steps to Make a GUI with Tkinter
    1. Import tkinter
       import tkinter as tk

    2. Create a main window
       root = tk.Tk()

    3. Add GUI elements (widgets)
       - Label, Entry, Button, etc.

    4. Set window properties (title, size)
       root.title("Your GUI Title")
       root.geometry("widthxheight")

    5. Define widget behaviors with functions

    6. Use pack, grid, or place to position your widgets

    7. Run the main event loop
       root.mainloop()

Below awaits your wizard portal, crafted in Tkinter:
"""

import tkinter as tk

def main():
    root = tk.Tk()
    root.title("Tkinter Wizard Portal")
    root.geometry("400x250")

    steps = [
        "Step 1: Install Python",
        "Step 2: Install Xming",
        "Step 3: Clone a GitHub Project",
        "Step 4: Run the Tkinter Script",
        "Step 5: Troubleshooting",
        "Step 6: Customize Your GUI!",
        "Step 7: Learn GUI steps (see above)"
    ]

    label = tk.Label(root, text="🪄 Tkinter Setup Wizard Steps:", font=("Arial", 14))
    label.pack(pady=10)

    for step in steps:
        step_label = tk.Label(root, text=step, font=("Arial", 11), anchor="w", justify="left")
        step_label.pack(fill="x", padx=20)

    entry = tk.Entry(root, width=30)
    entry.pack(pady=10)
    entry.insert(0, "Type your wizard name...")

    def on_button_click():
        wizard_name = entry.get().strip() or "mysterious one"
        label.config(text=f"🪄 Welcome, {wizard_name}! Follow your portal steps above.")

    button = tk.Button(root, text="Cast Spell", command=on_button_click)
    button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()