
import os
import time
import pytesseract
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from PIL import Image
import pyperclip

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
screenshot_folder = os.path.expanduser(r"C:\Users\imama\OneDrive\Pictures\Screenshots")
output_folder = r"C:\KyojinStudios\SSReader\Screenshot transcribed"

class ScreenshotHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory or not event.src_path.lower().endswith(".png"):
            return
        time.sleep(1)  
        try:
            img = Image.open(event.src_path)
            text = pytesseract.image_to_string(img)
            base_name = os.path.splitext(os.path.basename(event.src_path))[0]
            txt_path = os.path.join(output_folder, f"{base_name}.txt")
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            pyperclip.copy(text)
            print(f"[✅] OCR complete. Saved and copied text from: {base_name}")
        except Exception as e:
            print(f"[❌] Failed to process {event.src_path}: {e}")

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

observer = Observer()
event_handler = ScreenshotHandler()
observer.schedule(event_handler, screenshot_folder, recursive=False)
observer.start()
print("[🔍] Watching for new screenshots... Press Ctrl+C to stop.")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
