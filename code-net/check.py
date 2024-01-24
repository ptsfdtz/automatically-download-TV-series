import speedtest
import tkinter as tk
from tkinter import Label, Button, ttk

class SpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("网速检测工具")

        # 调整窗口大小
        self.root.geometry("400x200")

        self.speed_label = Label(root, text="点击按钮检测网速")
        self.speed_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(root, length=300, mode="indeterminate")
        self.progress_bar.pack(pady=10)

        self.test_button = Button(root, text="检测网速", command=self.run_speed_test)
        self.test_button.pack()

    def run_speed_test(self):
        # 重置进度条
        self.progress_bar.stop()
        self.progress_bar.start(10)  # 启动进度条动画

        # 在后台线程中执行速度测试
        self.root.after(100, self.execute_speed_test)

    def execute_speed_test(self):
        st = speedtest.Speedtest()
        download_speed = st.download() / 1_000_000  # 转换为兆比特每秒
        upload_speed = st.upload() / 1_000_000  # 转换为兆比特每秒

        result_text = f"下载速度: {download_speed:.2f} Mbps\n上传速度: {upload_speed:.2f} Mbps"
        self.speed_label.config(text=result_text)

        # 停止进度条动画
        self.progress_bar.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedTestApp(root)
    root.mainloop()
