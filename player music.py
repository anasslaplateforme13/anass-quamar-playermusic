import tkinter as tk
from tkinter import filedialog
import pygame
import requests
from io import BytesI
import webbrowser

class LecteurAudio:
    def __init__(self, root):
        self.root = root
        self.root.title("Lecteur Audio")
        self.root.geometry("400x300")

        self.current_file = None
        self.paused = False
        self.loop = False

        self.initialize_player()
        self.create_widgets()

    def initialize_player(self):
        pygame.init()
        pygame.mixer.init()

    def create_widgets(self):
        self.btn_select_file = tk.Button(self.root, text="Choisir un fichier", command=self.select_file)
        self.btn_select_file.pack()

        self.btn_select_url = tk.Button(self.root, text="Charger depuis URL", command=self.load_from_url)
        self.btn_select_url.pack()

        self.btn_play = tk.Button(self.root, text="Lecture", command=self.play_audio)
        self.btn_play.pack()

        self.btn_pause = tk.Button(self.root, text="Pause", command=self.pause_audio)
        self.btn_pause.pack()

        self.btn_stop = tk.Button(self.root, text="Arrêter", command=self.stop_audio)
        self.btn_stop.pack()

        self.btn_loop = tk.Button(self.root, text="Boucle", command=self.toggle_loop)
        self.btn_loop.pack()

        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, label="Volume", command=self.set_volume)
        self.volume_slider.pack()

    def select_file(self):
        self.current_file = filedialog.askopenfilename(filetypes=[("Fichiers audio", "*.mp3;*.wav")])

    def load_from_url(self):
        url = tk.simpledialog.askstring("Charger depuis URL", "Entrez l'URL de l'audio:")
        if url:
            try:
                response = requests.get(url)
                audio_data = BytesIO(response.content)
                self.current_file = audio_data
                self.root.title(f"Lecture en cours - URL: {url}")
            except requests.RequestException as e:
                print(f"Erreur lors du chargement depuis l'URL : {e}")

    def play_audio(self):
        if self.current_file:
            if not pygame.mixer.music.get_busy():
                if isinstance(self.current_file, BytesIO):
                    pygame.mixer.music.load(self.current_file)
                else:
                    pygame.mixer.music.load(self.current_file)
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            if isinstance(self.current_file, str):
                self.root.title(f"Lecture en cours - {self.current_file}")
            elif isinstance(self.current_file, BytesIO):
                self.root.title("Lecture en cours - Audio depuis URL")

    def pause_audio(self):
        if pygame.mixer.music.get_busy():
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True
                self.root.title("Lecture en pause")
            else:
                pygame.mixer.music.unpause()
                self.paused = False
                if isinstance(self.current_file, str):
                    self.root.title(f"Lecture en cours - {self.current_file}")
                elif isinstance(self.current_file, BytesIO):
                    self.root.title("Lecture en cours - Audio depuis URL")

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.root.title("Lecteur Audio")
        self.current_file = None

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def toggle_loop(self):
        if not self.loop:
            pygame.mixer.music.play(loops=-1)
            self.loop = True
            if isinstance(self.current_file, str):
                self.root.title(f"Lecture en boucle - {self.current_file}")
            elif isinstance(self.current_file, BytesIO):
                self.root.title("Lecture en boucle - Audio depuis URL")
        else:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.current_file)
            self.loop = False
            if isinstance(self.current_file, str):
                self.root.title(f"Lecteur Audio - {self.current_file}")
            elif isinstance(self.current_file, BytesIO):
                self.root.title("Lecteur Audio - Audio depuis URL")
                def open_music_link(link):
                    

if __name__ == "__main__":
    root = tk.Tk()
    LecteurAudio(root)
    root.mainloop()




