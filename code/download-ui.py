import os
import requests
import threading
from tkinter import Tk, Button, ttk, IntVar
from PIL import Image, ImageTk, ImageEnhance
from tqdm import tqdm

class TransparentButton(Button):
    def __init__(self, master=None, **kwargs):
        Button.__init__(self, master, **kwargs)
        self['bg'] = self.master['bg']

class VideoDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("关注披头散发的秃子喵")
        root.geometry("560x320")

        self.background_images = [
            "image\\background_image1.jpg",
            "image\\background_image2.jpg",
            "image\\background_image3.jpg",
            "image\\background_image4.jpg",
            "image\\background_image5.jpg",
            "image\\background_image6.jpg",
            "image\\background_image7.jpg",
            "image\\background_image8.jpg",
            "image\\background_image9.jpg",
            "image\\background_image10.jpg",
            "image\\background_image11.jpg",
            "image\\background_image12.jpg",
            "image\\background_image13.jpg",
            "image\\background_image14.jpg",
            "image\\background_image15.jpg",
        ]
        self.current_background_index = 0
        self.load_background_image()

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

        self.button = TransparentButton(root, text="下载", command=self.start_download, font=('Helvetica', 14), width=5, height=2)
        self.button.grid(row=3, column=0, padx=20, pady=10, sticky='w')

        self.stop_button = TransparentButton(root, text="停止", command=self.stop_download, font=('Helvetica', 14), width=5, height=2)
        self.stop_button.grid(row=3, column=1, padx=20, pady=10, sticky='w')

        root.grid_rowconfigure(3, weight=1)
        root.grid_columnconfigure(0, weight=0)

        self.thread = None
        self.stop_event = threading.Event()

    def load_background_image(self):
        background_path = self.background_images[self.current_background_index]
        self.background_image = Image.open(background_path)

        enhancer = ImageEnhance.Brightness(self.background_image)
        self.background_image = enhancer.enhance(1.0) 

        self.background_photo = ImageTk.PhotoImage(self.background_image)

        if hasattr(self, 'background_label'):
            self.background_label.configure(image=self.background_photo)
            self.background_label.image = self.background_photo
        else:
            self.background_label = ttk.Label(self.root, image=self.background_photo)
            self.background_label.place(relwidth=1, relheight=1)

    def update_background(self):
        self.current_background_index = (self.current_background_index + 1) % len(self.background_images)
        self.load_background_image()

    def start_download(self):
        self.progress_var.set(0)

        total = int(self.entry_total.get()) + 1
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

            if replacement_digit % 1 == 0:
                self.update_background()

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
