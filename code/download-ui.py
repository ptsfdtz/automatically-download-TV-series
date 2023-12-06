import os
import requests
import threading
from tkinter import Tk, Label, Entry, Button, StringVar, IntVar, ttk
from PIL import Image, ImageTk
from tqdm import tqdm


class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Downloader")

        root.geometry("1080x640")

        self.background_image = Image.open("image\\background_image.jpg")
        self.background_photo = ImageTk.PhotoImage(self.background_image)

        self.background_label = ttk.Label(root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.label_total = ttk.Label(root, text="视频集数:")
        self.label_total.grid(row=0, column=0, padx=20, pady=10, sticky='w')
        self.entry_total = ttk.Entry(root)
        self.entry_total.grid(row=0, column=1, padx=20, pady=10, sticky='w')

        self.label_url = ttk.Label(root, text="链接:")
        self.label_url.grid(row=1, column=0, padx=20, pady=10, sticky='w')
        self.entry_url = ttk.Entry(root, width=50)
        self.entry_url.grid(row=1, column=1, padx=20, pady=10, sticky='w')

        self.label_path = ttk.Label(root, text="存储路径:")
        self.label_path.grid(row=2, column=0, padx=20, pady=10, sticky='w')
        self.entry_path = ttk.Entry(root, width=50)
        self.entry_path.grid(row=2, column=1, padx=20, pady=10, sticky='w')

        self.progress_label = ttk.Label(root, text="")
        self.progress_label.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky='w')

        self.progress_var = IntVar()
        self.progressbar = ttk.Progressbar(root, mode='determinate', length=400, variable=self.progress_var)
        self.progressbar.grid(row=4, column=1, padx=20, pady=10, sticky='w')

        self.button_style = ttk.Style()
        self.button_style.configure("TButton", font=('Helvetica', 14), width=5, height=2) 
        self.button = ttk.Button(root, text="下载", command=self.start_download, style="TButton")
        self.button.grid(row=3, column=0, padx=20, pady=10, sticky='w')

        self.stop_button = ttk.Button(root, text="停止", command=self.stop_download, style="TButton")
        self.stop_button.grid(row=3, column=1, padx=20, pady=10, sticky='w')

        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=0)

        self.thread = None
        self.stop_event = threading.Event()

    def start_download(self):
        self.progress_var.set(0)

        total = int(self.entry_total.get())
        original_url = self.entry_url.get()
        path = self.entry_path.get()

        self.button.configure(state='disabled')

        self.thread = threading.Thread(target=self.download_videos, args=(total, original_url, path))
        self.thread.start()

    def download_videos(self, total, original_url, path):
        for replacement_digit in range(1, total):
            if self.stop_event.is_set():
                break

            modified_url = self.replace_last_digit(original_url, replacement_digit)
            destination_file = f"downloaded_file_{replacement_digit}.mp4"
            self.download_file(modified_url, path, destination_file)
            self.progress_label.config(text=f"File downloaded: {destination_file}")

            progress_value = (replacement_digit / total) * 100
            self.progress_var.set(progress_value)

        self.button.configure(state='normal')

    def download_file(self, url, path, filename):
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            full_path = os.path.join(path, filename)
            if not os.path.exists(path):
                os.makedirs(path)

            print(f"Downloading {full_path}")

            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024
            with open(full_path, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for data in response.iter_content(block_size):
                    if self.stop_event.is_set():
                        break

                    bar.update(len(data))
                    file.write(data)

        else:
            print(f"Failed to download file. Status code: {response.status_code}")

    def replace_last_digit(self, url, replacement):
        last_digit_index = url.rfind('1')
        if last_digit_index != -1:
            modified_url = url[:last_digit_index] + str(replacement) + url[last_digit_index + 1:]
            return modified_url
        else:
            return url

    def stop_download(self):
        self.stop_event.set()
        if self.thread is not None:
            self.thread.join()
        self.stop_event.clear()


if __name__ == "__main__":
    root = Tk()
    app = VideoDownloaderApp(root)
    root.mainloop()
