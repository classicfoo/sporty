Here's a **README file** written for the end user of your `Sporty Notes` application:

---

# 📘 Sporty Notes – User Guide

**Sporty Notes** is a simple, easy-to-use desktop application for creating and managing notes. It allows you to store notes in a database file (`.pkl`), quickly search, and even auto-link notes when their titles are mentioned in other notes.

---

## 🚀 Getting Started

### 📦 **1. Installation**

1. Ensure you have **Python 3.8 or newer** installed.

2. Install the required libraries:

   ```bash
   pip install tk
   ```

   *(Tkinter comes pre-installed with most Python versions, so you likely don’t need to install it separately.)*

3. Download the `Sporty Notes` script (`note_app.py`) and run it:

   ```bash
   python note_app.py
   ```

---

## 📝 **2. Features Overview**

✅ **Create, Edit, and Delete Notes**
✅ **Auto-Linking Notes** – When a note title is mentioned in another note, it will be clickable (blue + underlined).
✅ **Quick Search** – Filter notes instantly by typing in the search bar.
✅ **Multiple Databases** – Save or switch between different `.pkl` files.
✅ **Right-Click Menu** – Delete notes directly from the list.
✅ **Keyboard Shortcuts** for faster navigation.

---

## 🎯 **3. Using Sporty Notes**

### 🆕 **Creating a New Note**

* Press **`Ctrl + N`** to create a new note.
* You can highlight text in an existing note, press `Ctrl + N`, and it will automatically become the new note’s title.

### 🖊️ **Editing Notes**

* Click on a note title in the list to load it.
* Edit the **title** in the top field or the **content** in the large text box.
* Changes are saved automatically.

### 🗑️ **Deleting Notes**

* **Right-click** on a note title in the list.
* Select **Delete** from the context menu.

### 🔍 **Searching Notes**

* Type in the **search bar** above the note list to filter notes by title.

### 🔗 **Auto-Linking**

* If you mention another note’s **exact title** in the content, it will turn blue and clickable.
* Clicking the linked title will load that note.

---

## 💾 **4. Database Management**

* **Open an Existing Database** → `Ctrl + O`

  * Select a `.pkl` file to load notes.
* **Create a New Database** → `Ctrl + Shift + S` *(or `Ctrl + S` if you mapped it that way)*

  * Save a fresh `.pkl` file for a new set of notes.
* The app remembers the **last opened database** automatically.

---

## ⌨️ **5. Keyboard Shortcuts**

* **Ctrl + N** → New note
* **Ctrl + O** → Open existing note database
* **Ctrl + S** → Save as a new database file
* **Ctrl + Backspace** → Delete the previous word in the note editor

---

## 🗂️ **6. Files Created**

* `notes.pkl` → Default notes database (unless you save a new one)
* `last_database.txt` → Remembers the last database you used

---

## ⚠️ **7. Tips & Notes**

* **Capitalization**: Titles automatically capitalize each word (e.g., “my note” → “My Note”).
* **Auto-Save**: Every change you make is saved instantly — no need to press a save button.
* **Backups**: You can copy `.pkl` files to create backups of your notes.

---

## 🛠️ **8. Troubleshooting**

❓ **The app won’t run?**

* Make sure Python 3 is installed and run it using `python note_app.py`.

❓ **I lost my notes!**

* Check the folder where `Sporty Notes` is saved for `.pkl` files (e.g., `notes.pkl`).

❓ **Text links don’t appear?**

* Ensure the exact note title (capitalization doesn’t matter) is written in the note content.

---

## 📄 License

This program is free for personal use.

---

Would you like me to:

* ✅ **Format this as a `README.md` file** with headings and markdown styling?
* ✅ Or **write a simplified PDF-style user manual** for non-technical users?
