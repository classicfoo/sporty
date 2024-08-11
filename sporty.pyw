import tkinter as tk
from tkinter import Menu, PanedWindow
import pickle
import re
from tkinter import filedialog
import os

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sporty Notes")

        self.config_file = "last_database.txt"
        self.current_pickle_file = self.load_last_database()  # Load the last used database

        
        self.notes = self.load_notes()

        self.paned_window = PanedWindow(root, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True)

        self.note_list_frame = tk.Frame(self.paned_window)
        self.note_list_frame.pack(fill=tk.BOTH, expand=True)

        self.note_editor_frame = tk.Frame(self.paned_window)
        self.note_editor_frame.pack(fill=tk.BOTH, expand=True)

        self.paned_window.add(self.note_list_frame, minsize=200)
        self.paned_window.add(self.note_editor_frame, minsize=300)

        self.search_entry = tk.Entry(self.note_list_frame)
        self.search_entry.pack(fill=tk.X, padx=10, pady=5)
        self.search_entry.bind('<KeyRelease>', self.search_notes)

        self.note_listbox = tk.Listbox(self.note_list_frame, selectmode=tk.EXTENDED)
        self.note_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.title_entry = tk.Entry(self.note_editor_frame, font=("Arial", 14))
        self.title_entry.pack(fill=tk.X, padx=10, pady=5)

        self.content_text = tk.Text(self.note_editor_frame, wrap=tk.WORD, font=("Arial", 12))
        self.content_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.load_note_list()

        self.note_listbox.bind('<Double-1>', self.load_note_from_list)
        self.note_listbox.bind('<Button-3>', self.show_context_menu)  # Bind right-click event
        
        self.title_entry.bind('<KeyRelease>', self.update_note)
        self.content_text.bind('<KeyRelease>', self.update_note)
        self.content_text.bind('<Button-1>', self.on_click)  # Bind click event
        
        self.root.bind('<Control-n>', self.new_note)
        
        self.current_note_title = ""

        self.create_context_menu()

        self.root.bind('<Control-o>', self.open_note_file)
    
        self.root.bind('<Control-S>', self.create_new_pickle_file)

        # Bind the delete_word function to Control + Backspace key combination
        self.content_text.bind('<Control-BackSpace>', self.delete_word)

    def load_notes(self):
        try:
            with open(self.current_pickle_file, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}


    def save_notes(self, event=None):
        with open(self.current_pickle_file, "wb") as f:
            pickle.dump(self.notes, f)

    def load_last_database(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, "r") as f:
                return f.read().strip()
        return "notes.pkl"  # Default pickle file if config file doesn't exist

    def save_last_database(self):
        with open(self.config_file, "w") as f:
            f.write(self.current_pickle_file)


    def load_note_list(self):
        self.note_listbox.delete(0, tk.END)
        for note in self.notes.keys():
            self.note_listbox.insert(tk.END, note)
        self.update_note_list_bold()

    def update_note_list_bold(self):
        for i in range(self.note_listbox.size()):
            note_title = self.note_listbox.get(i)
            self.note_listbox.itemconfig(i, {'bg': 'white'})

            content = self.content_text.get("1.0", tk.END)
            if re.search(re.escape(note_title), content, re.IGNORECASE):
                self.note_listbox.itemconfig(i, {'bg': 'lightgray'})

    def update_note(self, event=None):
        title = self.title_entry.get().strip()
        # Capitalise every word in the title
        capitalized_title = title.title()
        content = self.content_text.get("1.0", tk.END).strip()
        
        if not capitalized_title or not content:
            return

        if self.current_note_title and self.current_note_title in self.notes:
            del self.notes[self.current_note_title]
            
        self.notes[capitalized_title] = content
        self.current_note_title = capitalized_title
        self.auto_link()
        self.save_notes()
        self.load_note_list()
        self.search_entry.delete(0, tk.END)  # Clear the search field

        self.select_note_in_list()

    def delete_word(self, event):
        text = self.content_text
        cursor_position = text.index("insert")

        # Find the end of the current word by searching for the next space character
        word_end = text.search(r"\S", cursor_position, backwards=True, regexp=True)
        word_end= text.index(f"{word_end}+1c") # Move word_end one character forward

        word_start = text.search(r"\s", f"{word_end}", backwards=True, regexp=True)

        if word_start==cursor_position:
            word_start= 0.0
        
        word_start= text.index(f"{word_start}+2c") # Move word_start one character forward

        text.delete(word_start, cursor_position)

    def auto_link(self):
        self.content_text.tag_remove("all_tags", "1.0", tk.END)  # Remove all existing tags

        # Prepare a dictionary to store start and end positions for each title
        tag_positions = {}

        for title in sorted(self.notes.keys(), key=len, reverse=True):  # Sort by length, longest first
            pattern = title  # Ensure the pattern is properly escaped

            # Normalize spaces in the pattern and content
            pattern = re.sub(r'\s+', ' ', pattern)
            content = self.content_text.get("1.0", tk.END)
            content = re.sub(r'\s+', ' ', content)

            print(f"Searching for pattern: '{pattern}'")  # Debug: See the pattern being searched

            start = "1.0"
            while True:
                start = self.content_text.search(pattern, start, stopindex=tk.END, nocase=True)
                if not start:
                    break

                # Calculate the end position using the start index and the length of the title
                start_index = self.content_text.index(start)
                end_index = f"{start_index}+{len(pattern)}c"

                print(f"Tagging '{title}' from {start_index} to {end_index}")  # Debug: See if tagging occurs

                # Check if the current range overlaps with an existing tag
                overlap = False
                for existing_title, positions in tag_positions.items():
                    for pos_start, pos_end in positions:
                        if self.content_text.compare(start_index, "<", pos_end) and self.content_text.compare(end_index, ">", pos_start):
                            overlap = True
                            break
                    if overlap:
                        break

                if not overlap:
                    # If there's no overlap, add the tag
                    self.content_text.tag_add(title, start_index, end_index)
                    self.content_text.tag_config(title, foreground="blue", underline=1)

                    # Store the tag positions
                    if title not in tag_positions:
                        tag_positions[title] = []
                    tag_positions[title].append((start_index, end_index))

                start = end_index








    def search_notes(self, event):
        search_term = self.search_entry.get().strip().lower()
        self.note_listbox.delete(0, tk.END)
        for note in self.notes.keys():
            if search_term in note.lower():
                self.note_listbox.insert(tk.END, note)
        self.update_note_list_bold()

    def load_note_from_list(self, event):
        selected_note = self.note_listbox.get(self.note_listbox.curselection()[0])
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, selected_note)
        self.content_text.delete("1.0", tk.END)
        self.content_text.insert("1.0", self.notes[selected_note])
        self.current_note_title = selected_note
        self.auto_link()
        self.update_note_list_bold()
        self.search_entry.delete(0, tk.END)  # Clear the search field


    def new_note(self, event=None):
        # Get the selected text in the content_text widget
        try:
            selected_text = self.content_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
        except tk.TclError:
            # No text is selected
            selected_text = ""

        if selected_text:
            # Set the selected text as the new note title
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, selected_text)
        else:
            # Clear the title entry if no text was selected
            self.title_entry.delete(0, tk.END)

        # Clear the content_text widget
        self.content_text.delete("1.0", tk.END)
        self.current_note_title = ""
        self.title_entry.focus_set()


    def on_click(self, event):
        # Find the index of the clicked position
        index = self.content_text.index("@{},{}".format(event.x, event.y))

        # Get the tags at that index
        tags = self.content_text.tag_names(index)

        # Check if any tag matches a note title
        for tag in tags:
            if tag in self.notes:
                # Load the note with the corresponding title
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, tag)
                self.content_text.delete("1.0", tk.END)
                self.content_text.insert("1.0", self.notes[tag])
                self.current_note_title = tag
                self.auto_link()  # Reapply hyperlink tags for the new note
                self.update_note_list_bold()
                # Select the corresponding note in the note list
                selected_index = list(self.notes.keys()).index(tag)
                self.note_listbox.selection_clear(0, tk.END)
                self.note_listbox.selection_set(selected_index)
                self.note_listbox.see(selected_index)  # Scroll to the selected note
                break
    
    def select_note_in_list(self):
        # Get the current note title
        current_title = self.current_note_title

        # Check if the current note title exists in the notes
        if current_title in self.notes:
            # Find the index of the current note title in the note list
            selected_index = list(self.notes.keys()).index(current_title)

            # Clear any existing selection in the note list
            self.note_listbox.selection_clear(0, tk.END)

            # Set the selection to the index of the current note title
            self.note_listbox.selection_set(selected_index)

            # Scroll to the selected note in the note list
            self.note_listbox.see(selected_index)

    def create_context_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Delete", command=self.delete_note)

    def show_context_menu(self, event):
        try:
            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def delete_note(self):
        selected_notes = self.note_listbox.curselection()
        for index in reversed(selected_notes):
            note_title = self.note_listbox.get(index)
            if note_title in self.notes:
                del self.notes[note_title]
        self.save_notes()
        self.load_note_list()
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)
        self.current_note_title = ""

    def open_note_file(self, event=None):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle files", "*.pkl")])
        if file_path:
            self.current_pickle_file = file_path  # Update the current pickle file
            self.notes = self.load_notes()
            self.load_note_list()
            self.save_last_database()  # Save the current pickle file to the config file
            self.new_note()

    def create_new_pickle_file(self, event=None):
        new_file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle files", "*.pkl")])
        if new_file_path:
            self.current_pickle_file = new_file_path
            self.save_notes()
            self.save_last_database()

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
