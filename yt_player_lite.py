import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable

# to run this, you need to install pytube package
# pip install pytube
class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple YouTube Downloader")
        self.root.geometry("600x400")
        self.root.configure(bg='#f0f0f0')
        self.root.minsize(500, 350)
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="YouTube Video Downloader",
                                font=("Arial", 16, "bold"))
        title_label.pack(pady=10)

        url_frame = ttk.LabelFrame(
            main_frame, text="Step 1: Enter YouTube URL", padding="10")
        url_frame.pack(fill=tk.X, pady=10)

        self.url_entry = tk.Text(
            url_frame, height=3, width=60, font=("Arial", 10))
        self.url_entry.pack(fill=tk.X)

        example_label = ttk.Label(url_frame, text="Example: https://www.youtube.com/watch?v=9bZkp7q19f0",
                                  font=("Arial", 8), foreground="gray")
        example_label.pack(pady=5)

        options_frame = ttk.LabelFrame(
            main_frame, text="Step 2: Choose Options", padding="10")
        options_frame.pack(fill=tk.X, pady=10)

        type_frame = ttk.Frame(options_frame)
        type_frame.pack(fill=tk.X, pady=5)

        ttk.Label(type_frame, text="Download as:").pack(side=tk.LEFT)
        self.download_type = tk.StringVar(value="video")
        ttk.Radiobutton(type_frame, text="Video", variable=self.download_type,
                        value="video").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(type_frame, text="Audio (MP3)",
                        variable=self.download_type, value="audio").pack(side=tk.LEFT)

        quality_frame = ttk.Frame(options_frame)
        quality_frame.pack(fill=tk.X, pady=5)

        ttk.Label(quality_frame, text="Quality:").pack(side=tk.LEFT)
        self.quality_var = tk.StringVar(value="720p")
        qualities = ["Highest", "1080p", "720p", "480p", "360p"]
        quality_combo = ttk.Combobox(
            quality_frame, textvariable=self.quality_var, values=qualities, state="readonly")
        quality_combo.pack(side=tk.LEFT, padx=10)

        location_frame = ttk.Frame(options_frame)
        location_frame.pack(fill=tk.X, pady=5)

        ttk.Label(location_frame, text="Save to:").pack(side=tk.LEFT)
        self.location_var = tk.StringVar(
            value=os.path.join(os.path.expanduser("~"), "Downloads"))
        location_entry = ttk.Entry(
            location_frame, textvariable=self.location_var, width=40)
        location_entry.pack(side=tk.LEFT, padx=10)
        ttk.Button(location_frame, text="Browse",
                   command=self.browse_folder).pack(side=tk.LEFT)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20)

        self.download_btn = ttk.Button(
            button_frame, text="Download Now", command=self.start_download)
        self.download_btn.pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame, text="Clear", command=self.clear_all).pack(
            side=tk.LEFT, padx=10)

        progress_frame = ttk.LabelFrame(
            main_frame, text="Progress", padding="10")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=10)
#made by gao le 
        self.progress_label = ttk.Label(
            progress_frame, text="Ready to download...")
        self.progress_label.pack(anchor=tk.W)

        self.progress_bar = ttk.Progressbar(
            progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=5)

        self.info_text = tk.Text(
            progress_frame, height=6, font=("Arial", 9), state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.location_var.set(folder)

    def clear_all(self):
        self.url_entry.delete("1.0", tk.END)
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.config(state=tk.DISABLED)
        self.progress_label.config(text="Ready to download...")
        self.progress_bar.stop()

    def update_progress(self, message):
        self.progress_label.config(text=message)

    def update_info(self, text):
        self.info_text.config(state=tk.NORMAL)
        self.info_text.insert(tk.END, text + "\n")
        self.info_text.see(tk.END)
        self.info_text.config(state=tk.DISABLED)

    def start_download(self):
        url = self.url_entry.get("1.0", tk.END).strip()

        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL")
            return

        if "youtube.com" not in url and "youtu.be" not in url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL")
            return

        self.download_btn.config(state=tk.DISABLED)
        self.progress_bar.start(10)

        thread = threading.Thread(target=self.download_video, args=(url,))
        thread.daemon = True
        thread.start()

    def download_video(self, url):
        try:
            self.update_progress("Connecting to YouTube...")
            self.update_info("=" * 50)
            self.update_info("Starting download...")

            yt = YouTube(url)

            self.update_info(f"🎬 Title: {yt.title}")
            self.update_info(f"👤 Channel: {yt.author}")
            self.update_info(f"⏱️ Duration: {yt.length} seconds")
            self.update_info(f"📊 Views: {yt.views:,}")
            self.update_info("-" * 50)

            download_path = self.location_var.get()
            os.makedirs(download_path, exist_ok=True)

            if self.download_type.get() == "audio":
                self.update_progress("Downloading audio...")
                self.update_info("Downloading audio (MP3)...")

                audio_stream = yt.streams.get_audio_only()
                if audio_stream:
                    file_path = audio_stream.download(
                        output_path=download_path)

                    base, ext = os.path.splitext(file_path)
                    new_file_path = base + ".mp3"
                    os.rename(file_path, new_file_path)

                    self.update_info(
                        f"✅ Audio saved as: {os.path.basename(new_file_path)}")
                    self.update_progress("Download completed successfully!")
                    messagebox.showinfo(
                        "Success", f"Audio downloaded successfully!\nSaved to: {new_file_path}")
                else:
                    self.update_info("❌ No audio stream available")
                    messagebox.showerror(
                        "Error", "No audio stream available for this video")

            else:
                quality = self.quality_var.get()
                self.update_progress(f"Downloading video ({quality})...")
                self.update_info(f"Downloading video ({quality})...")

                if quality == "Highest":
                    video_stream = yt.streams.get_highest_resolution()
                else:
                    video_stream = yt.streams.filter(
                        progressive=True, file_extension='mp4', res=quality).first()
                    if not video_stream:
                        self.update_info(
                            f"Quality {quality} not available, trying highest resolution...")
                        video_stream = yt.streams.get_highest_resolution()

                if video_stream:
                    file_path = video_stream.download(
                        output_path=download_path)
                    self.update_info(
                        f"✅ Video saved as: {os.path.basename(file_path)}")
                    self.update_progress("Download completed successfully!")
                    messagebox.showinfo(
                        "Success", f"Video downloaded successfully!\nSaved to: {file_path}")
                else:
                    self.update_info("❌ No suitable video stream available")
                    messagebox.showerror(
                        "Error", "No suitable video stream available")

        except RegexMatchError:
            self.update_info("❌ Invalid YouTube URL")
            messagebox.showerror(
                "Error", "Invalid YouTube URL. Please check the URL and try again.")
        except VideoUnavailable:
            self.update_info("❌ Video is unavailable")
            messagebox.showerror(
                "Error", "Video is unavailable (private, deleted, or age-restricted)")
        except Exception as e:
            self.update_info(f"❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.root.after(0, self.download_complete)

    def download_complete(self):
        self.download_btn.config(state=tk.NORMAL)
        self.progress_bar.stop()
        self.update_progress("Ready for next download")


def main():
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()


