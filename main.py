import tkinter as tk
from tkinter import ttk
from pytube import YouTube
import threading

class VideoDownloader:
    def __init__(self, master):
        self.format = "MP4"
        self.format_options = ["MP4", "MP3"]
        self.res = "Highest Resolution"
        self.res_options = ["Highest Resolution", "720p", "480p", "240p"]
        self.error_label_created = False
        self.downloading_label_created = False
        self.downloaded_label_created = False

        # GUI setup
        self.master = master
        self.master.title("YouTube Video Downloader By Gor Mar")

        # Title
        self.downloader_frame = ttk.Frame(master)
        self.downloader_frame.grid(row=0, column=0, padx=10, pady=10)

        self.title_label = ttk.Label(self.downloader_frame, text="YouTube Video Downloader", font=("Arial", 15))
        self.title_label.grid(row=0, column=0, pady=10)

        # Settings
        self.settings_frame = tk.LabelFrame(self.downloader_frame, text="Settings", font=("Arial", 13))
        self.settings_frame.grid(row=1, column=0, padx=10, pady=5)

        self.format_var = tk.StringVar(value=self.format)
        self.format_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.format_var, values=self.format_options, state='readonly', width=12)
        self.format_dropdown.grid(row=0, column=0, padx=10, pady=10)

        self.res_var = tk.StringVar(value=self.res)
        self.res_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.res_var, values=self.res_options, state='readonly', width=18)
        self.res_dropdown.grid(row=0, column=1, padx=10, pady=10)

        # URL
        self.url_frame = tk.LabelFrame(self.downloader_frame, text="URL", font=("Arial", 13))
        self.url_frame.grid(row=2, column=0, padx=10, pady=10)

        self.url_entry = ttk.Entry(self.url_frame, width=40)
        self.url_entry.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Download Button
        download_style = ttk.Style()
        download_style.configure("Download.TButton", font=("Arial", 15), width=20)

        self.download_button = ttk.Button(self.downloader_frame, style="Download.TButton", text="Download", command=self.download_video)
        self.download_button.grid(row=3, column=0, pady=10)

    def download_video(self):
        url = self.url_entry.get()
        self.res = self.res_var.get()
        self.format = self.format_var.get()

        if url:
            try:
                yt = YouTube(url)
                download_thread = threading.Thread(target=self.download_in_thread, args=(yt, self.res, self.format))
                download_thread.start()
            except Exception as e:
                self.show_error_label()
        else:
            self.show_error_label()

    def download_in_thread(self, yt, resolution, video_format):
        try:
            if resolution == "Highest Resolution":
                video_stream = yt.streams.get_highest_resolution()
            else:
                video_stream = yt.streams.filter(res=resolution).first()
            self.hide_error_label()
            
            if video_format == "MP3":
                audio_stream = yt.streams.filter(only_audio=True).first()
                self.show_downloading_label()
                filename = f"{yt.title}.mp3"
                audio_stream.download('.', filename=filename)
            elif video_format == "MP4":
                self.show_downloading_label()
                video_stream.download('.')


            print(f"Download completed")
            self.hide_downloading_label()
            self.show_downloaded_label()
            self.master.after(2500, self.hide_downloaded_label)

        except Exception as e:
            self.show_error_label()

    def show_downloading_label(self):
        if not self.downloading_label_created:
            self.downloading_label = ttk.Label(self.downloader_frame, text="Downloading...", font=("Arial", 10), foreground="blue")
            self.downloading_label.grid(row=4, column=0, pady=5)
            self.downloading_label_created = True

    def hide_downloading_label(self):
        if self.downloading_label_created:
            self.downloading_label.grid_forget()
            self.downloading_label_created = False
            
    def show_downloaded_label(self):
        if not self.downloaded_label_created:
            self.downloaded_label = ttk.Label(self.downloader_frame, text="Downloaded", font=("Arial", 10), foreground="green")
            self.downloaded_label.grid(row=4, column=0, pady=5)
            self.downloaded_label_created = True
        else:
            self.downloaded_label.grid(row=4, column=0, pady=5)

    def hide_downloaded_label(self):
        if self.downloaded_label_created:
            self.downloaded_label.grid_forget()
            self.downloaded_label_created = False

    def show_error_label(self):
        if not self.error_label_created:
            if self.downloading_label_created:
                self.hide_downloading_label()
            if self.downloaded_label_created:
                self.hide_downloaded_label()
            
            self.error_label = ttk.Label(self.downloader_frame, text="The URL is not valid", font=("Arial", 10), foreground="red")
            self.error_label.grid(row=4, column=0, pady=5)
            self.error_label_created = True

    def hide_error_label(self):
        if self.error_label_created:
            self.error_label.grid_forget()
            self.error_label_created = False

def main():
    root = tk.Tk()
    app = VideoDownloader(root)
    root.geometry("315x300")
    root.mainloop()

if __name__ == "__main__":
    main()