import tkinter as tk
import customtkinter
from GUI_setup import Setup   # your class file
import os

FILENAME = "data.pkl"

# Create root window
root = customtkinter.CTk()
root.title("Flashcard Creator")
root.geometry("500x500")
customtkinter.set_default_color_theme("blue")

# --- Frames ---
welcome_frame = customtkinter.CTkFrame(root)
add_frame = customtkinter.CTkFrame(root)
study_frame = customtkinter.CTkFrame(root)

# --- Widgets for add_frame ---
term_entry = customtkinter.CTkEntry(add_frame, width=300)
definition_entry = customtkinter.CTkEntry(add_frame, width=300)
result_label = customtkinter.CTkLabel(add_frame, text="")

# --- Theme switch ---
theme_switch = customtkinter.CTkSwitch(
    welcome_frame,
    text="Dark Mode"
)

# --- Instantiate Setup with all widgets ---
app = Setup(
    term_entry,
    definition_entry,
    result_label,
    study_frame,
    welcome_frame,
    add_frame,
    root,
    FILENAME,
    theme_switch
)

# --- Layout for welcome_frame ---
welcome_label = customtkinter.CTkLabel(
    welcome_frame,
    text="Welcome to the Flashcard Generator",
    font=("Arial", 16)
)
welcome_label.grid(row=0, column=5, pady=10)

switch_to_add_fc = customtkinter.CTkButton(
    welcome_frame,
    text="Add Flashcards",
    command=app.add_fc_button
)
switch_to_add_fc.grid(row=1, column=5, pady=10)

switch_to_study_fc = customtkinter.CTkButton(
    welcome_frame,
    text="Study Flashcards",
    command=lambda: [app.show_frame(study_frame), app.show_term()]
)
switch_to_study_fc.grid(row=2, column=5, pady=10)

theme_switch.configure(command=app.toggle_theme)
theme_switch.grid(row=3, column=5, pady=10)

# --- Layout for add_frame ---
customtkinter.CTkLabel(add_frame, text="Enter Term:").grid(row=0, column=5, pady=5)
term_entry.grid(row=1, column=5, pady=5)

customtkinter.CTkLabel(add_frame, text="Enter Definition:").grid(row=2, column=5, pady=5)
definition_entry.grid(row=3, column=5, pady=5)

add_button = customtkinter.CTkButton(add_frame, text="Add Flashcard", command=app.add_flashcard)
add_button.grid(row=4, column=5, pady=5)

result_label.grid(row=5, column=5, pady=5)

back_to_welcome = customtkinter.CTkButton(add_frame, text="Back to Menu", command=app.welcome_button)
back_to_welcome.grid(row=6, column=5, pady=5)

switch_to_study_fc2 = customtkinter.CTkButton(
    add_frame,
    text="Study Flashcards",
    command=lambda: [app.show_frame(study_frame), app.show_term()]
)
switch_to_study_fc2.grid(row=7, column=5, pady=5)

# --- Menu bar (segmented button) ---
menu_frame = customtkinter.CTkFrame(root, height=40)
menu_frame.pack(side="top", fill="x", padx=5, pady=5)

seg_btn = customtkinter.CTkSegmentedButton(
    menu_frame,
    values=["Menu", "Add Flashcards", "Study Flashcards", "Dictionary", "Save", "Load"],
    command=lambda choice: {
        "Menu": app.welcome_button,
        "Add Flashcards": app.add_fc_button,
        "Study Flashcards": lambda: [app.show_frame(study_frame), app.show_term()],
        "Dictionary": app.open_dictionary_window,
        "Save": app.save,
        "Load": app.reopen
    }[choice]()
)
seg_btn.pack(padx=5, pady=5)

# --- Start with welcome frame ---
welcome_frame.pack(fill="both", expand=True)

root.mainloop()
