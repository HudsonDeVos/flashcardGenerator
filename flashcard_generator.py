# Version: 0.5


# Disclaimer: This code was made with the HELP of AI.

# Import randint
from random import randint 
# Import tkinter for GUI
import tkinter as tk
from tkinter import ttk
import customtkinter 
# Import Pickle 
import pickle
import os 
from dictionary_fc import Dictionary

# Crate a list 
term_list = [] 
definition_list = []

FILENAME = "data.pkl"

# Make a GUI

def add_flashcard(): # Created the add_flashcard function 
    term = term_entry.get() # Gets the term 
    definition = definition_entry.get() # Gets the definition 
    if term and definition: # Asks if both the term and definition are present 
        term_list.append(term) # Stores the term in a list
        definition_list.append(definition) # Stores the definition in a list 
        result_label.configure(text=f"added {term} {definition}") # Shows the term and definition before deleting it  
        term_entry.delete(0, tk.END) # Deletes the users term from the menu
        definition_entry.delete(0, tk.END) # Deletes the users definition from the menu
    else:
        result_label.configure(text="Please enter both a term and definition.") # Lets the user know if they did not put any term or definition


def show_term():

    # Clear previous buttons to prevent stacking
    for widget in study_frame.winfo_children():
        widget.destroy()

    # Tells if you have created flashcards to study
    if not term_list:
        result_label.configure(text="No flashcards are created.")
        return

    # Allows the user to study their flaschards 
    index = randint(0, len(term_list) - 1) # Gets a term from the flashcard list
    customtkinter.CTkLabel(study_frame, text=f"Term: {term_list[index]}", font=("Arial")).pack(pady=50) # Prints the chosen term to the screen
    
    # This creates a reaveal desinition button as well as shows the definition when the button is pressed 
    def show_definition(): 
        customtkinter.CTkLabel(study_frame, text=f"Definition: {definition_list[index]}", font=("Arial", 14)).pack(pady=10)
        customtkinter.CTkButton(study_frame, text="Next Term", command=show_term).pack(pady=0)

    customtkinter.CTkButton(study_frame, text="Show definition", command=show_definition).pack(pady=10)
    
# Creates a welcome screen so the user does not open right into making a flashcard
def show_frame(frame):
    # Use pack_forget instead of grid_forget since we’re using pack for top-level frames
    welcome_frame.pack_forget()
    add_frame.pack_forget()
    study_frame.pack_forget()
    frame.pack(fill="both", expand=True)

# Creates a button for switching to the add flashcard frame
def add_fc_button():
    show_frame(add_frame)

# Creates a button for switching to the welcome frame 
def welcome_button():
    show_frame(welcome_frame)

# Creates a list to save the flashcards 
def save():
    try:
        with open(FILENAME, "wb") as f:
            pickle.dump((term_list, definition_list), f)
        try:
           result_label.configure(text=f"Saved {len(term_list)} flashcards to {FILENAME}")
        except NameError:
            print("Saved, but GUI is not ready yet")
    except Exception as e:
        try:
            result_label.configure(text=f"Save failed: {e}")
        except NameError:
            print("Save failed")

# Creates the ability to access the saved list
def reopen():
    """Load the lists back into the global variables."""
    global term_list, definition_list
    if not os.path.exists(FILENAME):
        try:
            result_label.configure(text="No saved file found.")
        except NameError:
            print("No saved file found.")
        return

    try:
        with open(FILENAME, "rb") as f:
            loaded = pickle.load(f)
        # Expect the saved object to be a (term_list, definition_list) tuple
        if isinstance(loaded, (tuple, list)) and len(loaded) == 2:
            term_list, definition_list = loaded
            try:
                result_label.configure(text=f"Loaded {len(term_list)} flashcards.")
            except NameError:
                print(f"Loaded {len(term_list)} flashcards.")
        else:
            raise ValueError("Saved file has unexpected format.")
    except Exception as e:
        try:
            result_label.configure(text=f"Load failed: {e}")
        except NameError:
            print("Load failed:", e)

# Allows the user to use the dictionary in the code
def open_dictionary_window():
    dict_window = customtkinter.CTkToplevel(root)
    dict_window.title("Dictionary Lookup")
    dict_window.geometry("400x200")

    customtkinter.CTkLabel(dict_window, text="Enter a word:").pack(pady=5)
    word_entry = customtkinter.CTkEntry(dict_window, width=30)
    word_entry.pack(pady=5)

    result_label = customtkinter.CTkLabel(dict_window, text="", wraplength=350)
    result_label.pack(pady=10)

    def lookup():
        word = word_entry.get().strip()
        if not word:
            result_label.configure(text="Please enter a word.")
            return
        definition = Dictionary.get_definition(word)
        if definition:
            result_label.configure(text=f"Definition of {word}:\n{definition}")
        else:
            result_label.configure(text="Word not found.")

    customtkinter.CTkButton(dict_window, text="Search", command=lookup).pack(pady=5)

# Creates the GUI window
root = customtkinter.CTk()
root.title("Flashcard Creator")
root.geometry("500x500")

customtkinter.set_appearance_mode("Dark")

customtkinter.set_default_color_theme("blue")

'''Creating and working with frames and buttons:'''

# Creates a grid system for the welcome frame
welcome_frame = customtkinter.CTkFrame(root)
for r in range(10):
    welcome_frame.grid_rowconfigure(r, weight=1)
for c in range(10):
    welcome_frame.grid_columnconfigure(c, weight=1)

# Creates a frame for adding flashcards
add_frame = customtkinter.CTkFrame(root)

global result_label
result_label = customtkinter.CTkLabel(add_frame, text="")
result_label.grid(row=5, column=5, pady=0)

# Creates a frame for studying flashcards
study_frame = customtkinter.CTkFrame(root)
study_label = customtkinter.CTkLabel(study_frame, text="", font=("Arial", 14))
study_label.grid(pady=50)

# Creates a label for the welcome frame
welcome_label = customtkinter.CTkLabel(welcome_frame, text="Welcome to the Flashcard Generator", font=("Arial", 16))
welcome_label.grid(row=0, column=5, pady=0)

# Creates buttons for switching to the add flashcard frame
switch_to_add_fc = customtkinter.CTkButton(welcome_frame, text="Add Flashcards", command=add_fc_button)
switch_to_add_fc.grid(row=1, column=5, pady=0)

# Creates buttons for switching to the study frame
switch_to_study_fc = customtkinter.CTkButton(welcome_frame, text="Study Flashcards", command=lambda: [show_frame(study_frame), show_term()])
switch_to_study_fc.grid(row=2, column=5, pady=0)

# Creates a grid system for the add fc frame
for r in range(10):
    add_frame.grid_rowconfigure(r, weight=1)
for c in range(10):
    add_frame.grid_columnconfigure(c, weight=1)

# Creates label for entering a term
enter_term = customtkinter.CTkLabel(add_frame, text="Enter Term:")
enter_term.grid(row=0, column=5, pady=0)

# Creates a box for inputing a term
term_entry = customtkinter.CTkEntry(add_frame,  width=30)
term_entry.grid(row=1, column=5, pady=0)

# Creates a label for entering a definition
enter_definition = customtkinter.CTkLabel(add_frame, text="Enter Definition:")
enter_definition.grid(row=2, column=5, pady=0)

# Creates a box for inputing a definition
definition_entry = customtkinter.CTkEntry(add_frame, width=30) 
definition_entry.grid(row=3, column=5, pady=0)

# Creates a button for adding a flashcard
add_button = customtkinter.CTkButton(add_frame, text="Add Flashcard", command=add_flashcard)
add_button.grid(row=4, column=5, pady=0)

# Creates a label for showing results
result_label = customtkinter.CTkLabel(add_frame, text="")
result_label.grid(row=5, column=5, pady=0)

# Creates buttons for switching to the welcome frame from the add fc frame
back_to_welcome_frame = customtkinter.CTkButton(add_frame, text="Back to Menu", command=welcome_button)
back_to_welcome_frame.grid(row=6, column=5, pady=0)

# Creates buttons for switching to the study frame
switch_to_study_fc = customtkinter.CTkButton(add_frame, text="Study Flashcards", command=lambda: [show_frame(study_frame), show_term()])
switch_to_study_fc.grid(row=7, column=5, pady=0)


for r in range(10):
    study_frame.grid_rowconfigure(r, weight=1)
for c in range(10):
    study_frame.grid_columnconfigure(c, weight=1)

# Creates buttons for switching to the add flashcard frame
switch_to_add_fc = customtkinter.CTkButton(study_frame, text="Add Flashcards", command=add_fc_button)
switch_to_add_fc.grid(row=1, column=5, pady=0)

'''Ends the creation and use of frames and buttons'''

# Creates a drop down menu
menu = tk.Menu(root)
root.configure(menu=menu)


# Creates a drop down menu
# Create a top frame to act as a menu bar
menu_frame = customtkinter.CTkFrame(root, height=40)
menu_frame.pack(side="top", fill="x", padx=5, pady=5)

# Create a segmented button for menu options
seg_btn = customtkinter.CTkSegmentedButton(
    menu_frame,
    values=["Add Flashcards", "Study Flashcards", "Dictionary"],
    command=lambda choice: {
        "Add Flashcards": lambda: show_frame(add_frame),
        "Study Flashcards": lambda: [show_frame(study_frame), show_term()],
        "Dictionary": open_dictionary_window,
        "Save": save
    }[choice]()
)
seg_btn.pack(padx=5, pady=5)


save_button = customtkinter.CTkButton(menu_frame, text="Save", command=save)
save_button.pack(side="left", padx=5, pady=5)

load_button = customtkinter.CTkButton(menu_frame, text="Load", command=reopen)
load_button.pack(side="left", padx=5, pady=5)

welcome_frame.pack(fill="both", expand=True)


root.mainloop()
