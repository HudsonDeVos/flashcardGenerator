import tkinter as tk
import customtkinter
import os
from dictionary_fc import Dictionary
import pickle
from random import randint


class Setup:
    def __init__(self, term_entry, definition_entry, result_label,
                 study_frame, welcome_frame, add_frame,
                 root, FILENAME, theme_switch):
        self.term_entry = term_entry
        self.definition_entry = definition_entry
        self.result_label = result_label
        self.study_frame = study_frame
        self.welcome_frame = welcome_frame
        self.add_frame = add_frame
        self.root = root
        self.FILENAME = FILENAME
        self.theme_switch = theme_switch

        # initialize internal variables
        self.term_list = []
        self.definition_list = []
        self.index = None
        self.reveal_btn = None
        self.dict_window = None
        self.word_entry = None
        self.dict_result_label = None
        self.mode = None

    def add_flashcard(self):
        term = self.term_entry.get()
        definition = self.definition_entry.get()
        if term and definition:
            self.term_list.append(term)
            self.definition_list.append(definition)
            self.result_label.configure(text=f"Added {term} - {definition}")
            self.term_entry.delete(0, tk.END)
            self.definition_entry.delete(0, tk.END)
        else:
            self.result_label.configure(text="Please enter both a term and definition.")

    def show_term(self):
        for widget in self.study_frame.winfo_children():
            widget.destroy()

        if not self.term_list:
            customtkinter.CTkLabel(self.study_frame, text="No flashcards created yet.", font=("Arial", 16)).pack(pady=20)
            return

        self.index = randint(0, len(self.term_list) - 1)

        term_label = customtkinter.CTkLabel(self.study_frame, text=f"Term:\n{self.term_list[self.index]}", font=("Arial", 22))
        term_label.pack(pady=20)

        # Reveal button
        self.reveal_btn = customtkinter.CTkButton(self.study_frame, text="Show Definition", command=self.show_definition)
        self.reveal_btn.pack(pady=10)

    def show_definition(self):
        definition_label = customtkinter.CTkLabel(self.study_frame, text=f"Definition:\n{self.definition_list[self.index]}", font=("Arial", 18))
        definition_label.pack(pady=10)

        next_btn = customtkinter.CTkButton(self.study_frame, text="Next Term", command=self.show_term)
        next_btn.pack(pady=10)

    def show_frame(self, frame):
        self.welcome_frame.pack_forget()
        self.add_frame.pack_forget()
        self.study_frame.pack_forget()
        frame.pack(fill="both", expand=True)

    def add_fc_button(self):
        self.show_frame(self.add_frame)

    def welcome_button(self):
        self.show_frame(self.welcome_frame)

    def save(self):
        try:
            with open(self.FILENAME, "wb") as f:
                pickle.dump((self.term_list, self.definition_list), f)
            self.result_label.configure(text=f"Saved {len(self.term_list)} flashcards to {self.FILENAME}")
        except Exception as e:
            self.result_label.configure(text=f"Save failed: {e}")

    def reopen(self):
        if not os.path.exists(self.FILENAME):
            self.result_label.configure(text="No saved file found.")
            return
        try:
            with open(self.FILENAME, "rb") as f:
                loaded = pickle.load(f)
            if isinstance(loaded, (tuple, list)) and len(loaded) == 2:
                self.term_list, self.definition_list = loaded
                self.result_label.configure(text=f"Loaded {len(self.term_list)} flashcards.")
            else:
                raise ValueError("Saved file has unexpected format.")
        except Exception as e:
            self.result_label.configure(text=f"Load failed: {e}")

    def open_dictionary_window(self):
        self.dict_window = customtkinter.CTkToplevel(self.root)
        self.dict_window.title("Dictionary Lookup")
        self.dict_window.geometry("400x200")

        customtkinter.CTkLabel(self.dict_window, text="Enter a word:").pack(pady=5)
        self.word_entry = customtkinter.CTkEntry(self.dict_window, width=300)
        self.word_entry.pack(pady=5)

        self.dict_result_label = customtkinter.CTkLabel(self.dict_window, text="", wraplength=350)
        self.dict_result_label.pack(pady=10)

        customtkinter.CTkButton(self.dict_window, text="Search", command=self.lookup).pack(pady=5)

    def lookup(self):
        word = self.word_entry.get().strip()
        if not word:
            self.dict_result_label.configure(text="Please enter a word.")
            return
        definition = Dictionary.get_definition(word)
        if definition:
            self.dict_result_label.configure(text=f"Definition of {word}:\n{definition}")
        else:
            self.dict_result_label.configure(text="Word not found.\nPlease try again")

    def toggle_theme(self):
        self.mode = self.theme_switch.get()
        customtkinter.set_appearance_mode("dark" if self.mode else "light")
