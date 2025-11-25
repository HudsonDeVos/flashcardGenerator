import tkinter as tk
import flashcard_generator as fcg
import customtkinter
import os
from dictionary_fc import Dictionary
import pickle

term_list = [] 
definition_list = []



class Setup:
    def add_flashcard(): # Created the add_flashcard function 
        fcg.term = fcg.term_entry.get() # Gets the term 
    definition = fcg.definition_entry.get() # Gets the definition 
    if fcg.term and definition: # Asks if both the term and definition are present 
        term_list.append(fcg.term) # Stores the term in a list
        definition_list.append(definition) # Stores the definition in a list 
        fcg.result_label.configure(text=f"added {fcg.term} {definition}") # Shows the term and definition before deleting it  
        fcg.term_entry.delete(0, tk.END) # Deletes the users term from the menu
        fcg.definition_entry.delete(0, tk.END) # Deletes the users definition from the menu
    else:
        fcg.result_label.configure(text="Please enter both a term and definition.") # Lets the user know if they did not put any term or definition


def show_term():
    # Wipe the study frame
    for widget in fcg.study_frame.winfo_children():
        widget.destroy()

    # Stop if no flashcards
    if not term_list:
        customtkinter.CTkLabel(
            fcg.study_frame,
            text="No flashcards created yet.",
            font=("Arial", 16)
        ).pack(pady=20)
        return

    # Pick a random flashcard
    index = fcg.randint(0, len(term_list) - 1)

    # Term label (centered)
    term_label = customtkinter.CTkLabel(
        fcg.study_frame,
        text=f"Term:\n{term_list[index]}",
        font=("Arial", 22)
    )
    term_label.pack(pady=20)

    # Function to reveal definition
    def show_definition():
        definition_label = customtkinter.CTkLabel(
            fcg.study_frame,
            text=f"Definition:\n{definition_list[index]}",
            font=("Arial", 18)
        )
        definition_label.pack(pady=10)

        next_btn = customtkinter.CTkButton(
            fcg.study_frame,
            text="Next Term",
            command=show_term
        )
        next_btn.pack(pady=10)

    # Reveal definition button (centered)
    reveal_btn = customtkinter.CTkButton(
        fcg.study_frame,
        text="Show Definition",
        command=show_definition
    )
    reveal_btn.pack(pady=10)

    
# Creates a welcome screen so the user does not open right into making a flashcard
def show_frame(frame):
    # Use pack_forget instead of grid_forget since we’re using pack for top-level frames
    fcg.welcome_frame.pack_forget()
    fcg.add_frame.pack_forget()
    fcg.study_frame.pack_forget()
    frame.pack(fill="both", expand=True)

# Creates a button for switching to the add flashcard frame
def add_fc_button():
    show_frame(fcg.add_frame)

# Creates a button for switching to the welcome frame 
def welcome_button():
    show_frame(fcg.welcome_frame)

# Creates a list to save the flashcards 
def save():
    try:
        with open(fcg.FILENAME, "wb") as f:
            fcg.pickle.dump((term_list, definition_list), f)
        try:
           fcg.result_label.configure(text=f"Saved {len(term_list)} flashcards to {fcg.FILENAME}")
        except NameError:
            print("Saved, but GUI is not ready yet")
    except Exception as e:
        try:
            fcg.result_label.configure(text=f"Save failed: {e}")
        except NameError:
            print("Save failed")

# Creates the ability to access the saved list
def reopen():
    """Load the lists back into the global variables."""
    global term_list, definition_list
    if not os.path.exists(fcg.FILENAME):
        try:
            fcg.result_label.configure(text="No saved file found.")
        except NameError:
            print("No saved file found.")
        return

    try:
        with open(fcg.FILENAME, "rb") as f:
            loaded = pickle.load(f)
        # Expect the saved object to be a (term_list, definition_list) tuple
        if isinstance(loaded, (tuple, list)) and len(loaded) == 2:
            term_list, definition_list = loaded
            try:
                fcg.result_label.configure(text=f"Loaded {len(term_list)} flashcards.")
            except NameError:
                print(f"Loaded {len(term_list)} flashcards.")
        else:
            raise ValueError("Saved file has unexpected format.")
    except Exception as e:
        try:
            fcg.result_label.configure(text=f"Load failed: {e}")
        except NameError:
            print("Load failed:", e)

# Allows the user to use the dictionary in the code
def open_dictionary_window():
    dict_window = customtkinter.CTkToplevel(fcg.root)
    dict_window.title("Dictionary Lookup")
    dict_window.geometry("400x200")

    customtkinter.CTkLabel(dict_window, text="Enter a word:").pack(pady=5)
    word_entry = customtkinter.CTkEntry(dict_window, width=300)
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

def toggle_theme():
    # read directly from the switch’s get() method, which returns True/False
    mode = fcg.theme_switch.get()  # True if on, False if off
    customtkinter.set_appearance_mode("dark" if mode else "light")
