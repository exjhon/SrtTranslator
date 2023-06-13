import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar
import os
import re
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from tqdm import tqdm
import time

# 设置默认的模型文件夹路径
DEFAULT_MODEL_PATH = "./model/"

class SRTTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SRT翻译器")
        self.root.geometry("200x250")

        # 创建选择模型的下拉菜单
        self.model_label = tk.Label(root, text="选择模型：")
        self.model_label.pack()
        self.model_dropdown = tk.StringVar(root)
        self.model_dropdown.set("请选择模型")
        self.model_menu = tk.OptionMenu(root, self.model_dropdown, *self.get_model_folders())
        self.model_menu.pack()

        # 创建选择字幕文件的按钮
        self.select_files_button = tk.Button(root, text="选择字幕文件", command=self.select_files, width=20, height=3)
        self.select_files_button.pack(pady=10)

        # 创建翻译按钮
        self.translate_button = tk.Button(root, text="翻译", command=self.translate, width=20, height=3)
        self.translate_button.pack(pady=10)

        # 创建进度条、百分比和剩余时间标签
        self.progress = Progressbar(root, orient=tk.HORIZONTAL, length=200, mode='determinate')
        self.percentage_label = tk.Label(root, text="")
        self.time_label = tk.Label(root, text="")

    def get_model_folders(self):
        # 获取模型文件夹下的所有子文件夹作为模型选项
        model_folders = []
        for folder_name in os.listdir(DEFAULT_MODEL_PATH):
            folder_path = os.path.join(DEFAULT_MODEL_PATH, folder_name)
            if os.path.isdir(folder_path):
                model_folders.append(folder_name)
        return model_folders

    def select_files(self):
        # 弹出文件选择窗口，选择字幕文件
        files = filedialog.askopenfilenames(filetypes=[("字幕文件", "*.srt")])
        self.files = files if files else []

    def translate(self):
        # 获取选择的模型和字幕文件
        selected_model = self.model_dropdown.get()
        if selected_model == "请选择模型":
            messagebox.showerror("错误", "请选择一个模型")
            return
        if not self.files:
            messagebox.showerror("错误", "请选择一个或多个字幕文件")
            return

        # 加载模型
        model_path = os.path.join(DEFAULT_MODEL_PATH, selected_model)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        model.to(device)

        # 遍历每个字幕文件进行翻译
        for file in self.files:
            output_file = os.path.splitext(file)[0] + "_cn.srt"
            self.progress.pack()
            self.percentage_label.pack()
            self.time_label.pack()
            self.progress['value'] = 0
            self.progress['maximum'] = 100

            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            translated_lines = []
            total_lines = len(lines)
            start_time = time.time()
            for i, line in enumerate(tqdm(lines, desc="翻译进度", unit="行", ncols=80)):
                line = line.strip()

                # 跳过数字序号、时间戳和空行
                if re.match(r"^\d+$", line) or re.match(r"^\d+:\d+:\d+,\d+ --> \d+:\d+:\d+,\d+$", line) or len(line) == 0:
                    translated_lines.append(line)
                    continue

                # 翻译日文文本行
                input_text = tokenizer.encode(line, return_tensors="pt").to(device)
                translated_text = model.generate(input_text)
                translated_text = tokenizer.decode(translated_text[0], skip_special_tokens=True)
                translated_lines.append(translated_text)
                translated_lines.append(line)

                # 更新进度条、百分比和剩余时间
                self.progress['value'] = (i + 1) / total_lines * 100
                self.percentage_label.config(text=f"进度：{self.progress['value']:.2f}%")
                elapsed_time = time.time() - start_time
                remaining_time = elapsed_time / (i + 1) * (total_lines - i - 1)
                self.time_label.config(text=f"剩余时间：{remaining_time:.2f}秒")
                self.root.update()

            # 将翻译结果写入新的字幕文件
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(translated_lines))

            messagebox.showinfo("翻译完成", f"翻译结果已保存到：\n{output_file}")

            self.progress.pack_forget()
            self.percentage_label.pack_forget()
            self.time_label.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = SRTTranslatorApp(root)
    root.mainloop()
