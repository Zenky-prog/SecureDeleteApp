from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from pathlib import Path
import os

CHUNK = 1024 * 1024

class SecureDeleteApp(App):
    def build(self):
        self.title = "Secure Deletion"
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # عنوان التطبيق
        layout.add_widget(Label(text="مسح آمن ونهائي للملفات", font_size=20, size_hint_y=None, height=40))
        
        # حقل إدخال المسار
        self.path_input = TextInput(text='/sdcard/Download/', hint_text='أدخل مسار الملف أو المجلد هنا', size_hint_y=None, height=50)
        layout.add_widget(self.path_input)
        
        # زر البدء
        self.btn = Button(text='بدء المسح الآمن', size_hint_y=None, height=60, background_color=(0.8, 0.1, 0.1, 1))
        self.btn.bind(on_press=self.start_deletion)
        layout.add_widget(self.btn)
        
        # شاشة عرض النتيجة/الحالة
        self.status_label = Label(text='جاهز...', font_size=16)
        layout.add_widget(self.status_label)
        
        return layout

    def start_deletion(self, instance):
        target_path = self.path_input.text.strip()
        if not target_path:
            self.status_label.text = "الرجاء إدخال مسار صحيح!"
            return
            
        target = Path(target_path)
        self.status_label.text = f"جارٍ المعالجة..."
        
        # تنفيذ عملية المسح
        ok, fail = self.wipe_target(target, passes=3, zeros=True)
        self.status_label.text = f"انتهى ✅ - نجح: {ok} | فشل: {fail}"

    def secure_wipe(self, file_path, passes=3, zeros=True):
        try:
            size = file_path.stat().st_size
            with open(file_path, "r+b", buffering=0) as f:
                for p in range(1, passes + 1):
                    f.seek(0)
                    written = 0
                    while written < size:
                        block = os.urandom(min(CHUNK, size - written))
                        f.write(block)
                        written += len(block)
                    f.flush()
                    os.fsync(f.fileno())
                if zeros:
                    f.seek(0)
                    written = 0
                    while written < size:
                        block = b"\x00" * min(CHUNK, size - written)
                        f.write(block)
                        written += len(block)
                    f.flush()
                    os.fsync(f.fileno())
            file_path.unlink()
            return True
        except Exception:
            return False

    def wipe_target(self, target, passes, zeros):
        ok = fail = 0
        if target.is_file():
            if self.secure_wipe(target, passes, zeros): ok += 1
            else: fail += 1
        elif target.is_dir():
            for root, dirs, files in os.walk(target):
                for name in files:
                    fp = Path(root) / name
                    if self.secure_wipe(fp, passes, zeros): ok += 1
                    else: fail += 1
        return ok, fail

if __name__ == '__main__':
    SecureDeleteApp().run()
