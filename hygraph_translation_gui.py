import os
from dotenv import load_dotenv
from PyQt5 import QtWidgets, QtCore
import requests
import json

# === CONFIGURATION ===
load_dotenv()
HYGRAPH_ENDPOINT = os.getenv("HYGRAPH_ENDPOINT")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

def create_translation(key, value, locale):
    mutation = '''
    mutation CreateTranslation($key: String!, $value: String!, $locale: Locale!) {
      createTranslation(data: { key: $key, value: $value }, locale: $locale) {
        id
      }
    }
    '''
    variables = {
        "key": key,
        "value": value,
        "locale": locale
    }

    response = requests.post(HYGRAPH_ENDPOINT, json={
        "query": mutation,
        "variables": variables
    }, headers=HEADERS)

    if response.status_code == 200:
        return True, f"✅ Translation for '{locale}' uploaded."
    else:
        return False, f"❌ Error uploading translation for '{locale}': {response.text}"

def list_translations():
    # Query all translations (limit 50 for demo)
    query = '''
    query {
      translations(first: 50) {
        id
        key
        value
        locale
      }
    }
    '''
    response = requests.post(HYGRAPH_ENDPOINT, json={"query": query}, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        return data.get("data", {}).get("translations", [])
    else:
        return []

class TranslationUploader(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Hygraph Translation Uploader")
        layout = QtWidgets.QVBoxLayout()

        form_layout = QtWidgets.QFormLayout()
        self.key_input = QtWidgets.QLineEdit()
        self.fi_input = QtWidgets.QLineEdit()
        self.se_input = QtWidgets.QLineEdit()
        self.en_input = QtWidgets.QLineEdit()
        form_layout.addRow("Translation Key:", self.key_input)
        form_layout.addRow("Finnish (fi):", self.fi_input)
        form_layout.addRow("Swedish (se):", self.se_input)
        form_layout.addRow("English (en):", self.en_input)

        layout.addLayout(form_layout)

        btn_layout = QtWidgets.QHBoxLayout()
        self.submit_btn = QtWidgets.QPushButton("Upload Translations")
        self.submit_btn.clicked.connect(self.upload_translations)
        btn_layout.addWidget(self.submit_btn)

        self.list_btn = QtWidgets.QPushButton("List All Translations")
        self.list_btn.clicked.connect(self.show_translations)
        btn_layout.addWidget(self.list_btn)

        layout.addLayout(btn_layout)

        self.result_box = QtWidgets.QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        self.setLayout(layout)

        # Show all translations at startup
        self.show_translations(initial=True)

    def upload_translations(self):
        key = self.key_input.text().strip()
        fi = self.fi_input.text().strip()
        se = self.se_input.text().strip()
        en = self.en_input.text().strip()

        summary = f"\n📋 Summary:\n  Key: {key}\n  FI : {fi}\n  SE : {se}\n  EN : {en}\n"
        self.result_box.append(summary)

        confirm = QtWidgets.QMessageBox.question(self, "Confirm", "Is this correct?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if confirm != QtWidgets.QMessageBox.Yes:
            self.result_box.append("Aborted.")
            return

        for locale, value in [("fi", fi), ("se", se), ("en", en)]:
            success, msg = create_translation(key, value, locale)
            self.result_box.append(msg)

    def show_translations(self, initial=False):
        translations = list_translations()
        if not translations:
            self.result_box.append("No translations found.")
            return
        self.result_box.append("\n--- All Translations (first 50) ---")
        # Show as: key (locale): value
        for t in translations:
            self.result_box.append(f"{t['key']} ({t['locale']}): {t['value']}")
        if initial:
            # Show the first translation as requested
            first = translations[0]
            self.result_box.append(f"\nFirst translation: {first['key']} ({first['locale']}): {first['value']}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = TranslationUploader()
    window.show()
    sys.exit(app.exec_())
