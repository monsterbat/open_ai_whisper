import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import whisper
import os

# 定義語言選項，中文、英文、日文放在最上面
languages = ["Chinese", "English", "Japanese"] + sorted([
    "Afrikaans", "Albanian", "Amharic", "Arabic", "Armenian", "Assamese", "Azerbaijani",
    "Bashkir", "Basque", "Belarusian", "Bengali", "Bosnian", "Breton", "Bulgarian",
    "Burmese", "Castilian", "Catalan", "Chinese", "Croatian", "Czech", "Danish", 
    "Dutch", "English", "Estonian", "Faroese", "Finnish", "French", "Galician", 
    "Georgian", "German", "Greek", "Gujarati", "Haitian", "Hausa", "Hawaiian", 
    "Hebrew", "Hindi", "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", 
    "Javanese", "Kannada", "Kazakh", "Khmer", "Korean", "Lao", "Latin", "Latvian", 
    "Letzeburgesch", "Lingala", "Lithuanian", "Luxembourgish", "Macedonian", 
    "Malagasy", "Malay", "Malayalam", "Maltese", "Maori", "Marathi", "Moldavian", 
    "Moldovan", "Mongolian", "Nepali", "Norwegian", "Nynorsk", "Occitan", "Panjabi", 
    "Pashto", "Persian", "Polish", "Portuguese", "Punjabi", "Pushto", "Romanian", 
    "Russian", "Sanskrit", "Serbian", "Shona", "Sindhi", "Sinhala", "Sinhalese", 
    "Slovak", "Slovenian", "Somali", "Spanish", "Sundanese", "Swahili", "Swedish", 
    "Tagalog", "Tajik", "Tamil", "Tatar", "Telugu", "Thai", "Tibetan", "Turkish", 
    "Turkmen", "Ukrainian", "Urdu", "Uzbek", "Valencian", "Vietnamese", "Welsh", 
    "Yiddish", "Yoruba"
])

# 定義模型選項
models = [
    'tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 
    'medium.en', 'medium', 'large-v1', 'large-v2', 'large-v3', 'large'
]

class WhisperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Whisper 轉錄工具 v1.0.0")
        self.root.geometry("500x350")

        # 文件選擇
        self.file_label = tk.Label(root, text="選擇文件:")
        self.file_label.pack(pady=5)
        self.file_button = tk.Button(root, text="瀏覽", command=self.select_file)
        self.file_button.pack(pady=5)
        self.file_path = tk.StringVar()
        self.file_entry = tk.Entry(root, textvariable=self.file_path, width=50)
        self.file_entry.pack(pady=5)

        # 模型選擇
        self.model_label = tk.Label(root, text="選擇Whisper模型:")
        self.model_label.pack(pady=5)
        self.model_var = tk.StringVar(value=models[0])
        self.model_menu = ttk.Combobox(root, textvariable=self.model_var, values=models)
        self.model_menu.pack(pady=5)

        # 語言選擇
        self.language_label = tk.Label(root, text="選擇語言:")
        self.language_label.pack(pady=5)
        self.language_var = tk.StringVar(value=languages[0])
        self.language_menu = ttk.Combobox(root, textvariable=self.language_var, values=languages)
        self.language_menu.pack(pady=5)

        # 執行按鈕
        self.run_button = tk.Button(root, text="執行", command=self.run_whisper)
        self.run_button.pack(pady=20)

    def select_file(self):
        filetypes = (("音頻文件", "*.mp3 *.wav *.m4a *.flac"), ("所有文件", "*.*"))
        filename = filedialog.askopenfilename(title="選擇文件", filetypes=filetypes)
        if filename:
            self.file_path.set(filename)

    def run_whisper(self):
        file_path = self.file_path.get()
        model_name = self.model_var.get()
        language = self.language_var.get()

        if not os.path.isfile(file_path):
            messagebox.showerror("錯誤", "請選擇一個有效的文件")
            return

        try:
            model = whisper.load_model(model_name)
            result = model.transcribe(file_path, language=language)

            # 保存結果為多個文件格式
            base = os.path.splitext(file_path)[0]
            with open(base + ".txt", "w") as f:
                f.write(result["text"])
            with open(base + ".vtt", "w") as f:
                for segment in result["segments"]:
                    f.write(f"{segment['start']:.2f} --> {segment['end']:.2f}\n{segment['text']}\n\n")
            with open(base + ".srt", "w") as f:
                for i, segment in enumerate(result["segments"], start=1):
                    f.write(f"{i}\n{segment['start']:.2f} --> {segment['end']:.2f}\n{segment['text']}\n\n")
            with open(base + ".tsv", "w") as f:
                f.write("start\tend\ttext\n")
                for segment in result["segments"]:
                    f.write(f"{segment['start']:.2f}\t{segment['end']:.2f}\t{segment['text']}\n")
            with open(base + ".json", "w") as f:
                import json
                json.dump(result, f, ensure_ascii=False, indent=4)

            # 在終端機顯示進度
            for segment in result["segments"]:
                print(f"[{segment['start']:.2f} --> {segment['end']:.2f}] {segment['text']}")

            messagebox.showinfo("完成", "轉錄完成，已生成多個文件格式")
        except Exception as e:
            messagebox.showerror("錯誤", f"轉錄失敗: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhisperApp(root)
    root.mainloop()
