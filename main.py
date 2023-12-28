import tkinter as tk
from tkinter import ttk
from pytube import YouTube

class VideoDownloader:
    def __init__(self, master):
        self.website = "YouTube"
        self.website_options = ["YouTube", "TikTok"]
        self.res = "Highest Resolution"
        self.res_options = ["Highest Resolution", "1080p", "720p", "480p", "240p"]
        self.error_label_created = False
        self.downloading_label_created = False
        self.downloaded_label_created = False

        # GUI setup
        self.master = master
        self.master.title("Video Downloader By Gor Mar")

        # Title
        self.downloader_frame = ttk.Frame(master)
        self.downloader_frame.grid(row=0, column=0, padx=10, pady=10)

        self.title_label = ttk.Label(self.downloader_frame, text="Video Downloader", font=("Arial", 15))
        self.title_label.grid(row=0, column=0, pady=10)

        # Settings
        self.settings_frame = tk.LabelFrame(self.downloader_frame, text="Settings", font=("Arial", 13))
        self.settings_frame.grid(row=1, column=0, padx=10, pady=5)

        self.website_var = tk.StringVar(value=self.website)
        self.website_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.website_var, values=self.website_options, state='readonly', width=15)
        self.website_dropdown.grid(row=0, column=0, padx=10, pady=10)

        self.res_var = tk.StringVar(value=self.res)
        self.res_dropdown = ttk.Combobox(self.settings_frame, textvariable=self.res_var, values=self.res_options, state='readonly', width=15)
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
        if url:
            try:
                yt = YouTube(url)
                video_stream = yt.streams.get_highest_resolution()
                print(f"Downloading: {yt.title}")
                video_stream.download('.')
                print("Download complete!")

                self.error_label.grid_forget()
                self.error_label_created = False
            except Exception as e:
                self.create_error_label()
        else:
            self.create_error_label()

    def create_error_label(self):
        if not self.error_label_created:
            self.error_label = ttk.Label(self.downloader_frame, text="The URL is not valid", font=("Arial", 10), foreground="red")
            self.error_label.grid(row=4, column=0, pady=5)
            self.error_label_created = True

def main():
    root = tk.Tk()
    app = VideoDownloader(root)
    root.geometry("400x400")
    root.mainloop()

if __name__ == "__main__":
    main()