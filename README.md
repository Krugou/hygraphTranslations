# Hygraph Translation Uploader

A simple PyQt5 GUI tool to upload translations to Hygraph using their GraphQL API.

## Setup

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   - Copy `.env.example` to `.env` and fill in your Hygraph endpoint and auth token.

3. **Run the app:**
   ```sh
   python hygraph_translation_gui.py
   ```

## Features
- Enter translation key and values for Finnish, Swedish, and English.
- Review summary and confirm before upload.
- See upload results in the GUI.

---

**Note:** Requires a valid Hygraph project and permanent auth token.

