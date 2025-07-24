import requests
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import re
from urllib.parse import urlparse

class TikTokDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.root.title("TikTok Downloader - API Tikmate")
        self.root.geometry("600x300")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(
            main_frame, 
            text="TikTok Video Downloader", 
            font=("Segoe UI", 16, "bold"), 
            bg="#1e1e1e", 
            fg="#00b894"
        )
        title_label.pack(pady=(0, 20))
        
        # Label pour l'URL
        url_label = tk.Label(
            main_frame, 
            text="Lien TikTok :", 
            font=("Segoe UI", 11), 
            bg="#1e1e1e", 
            fg="white"
        )
        url_label.pack(anchor="w", pady=(0, 5))
        
        # Entry pour l'URL
        self.url_entry = tk.Entry(
            main_frame, 
            width=70, 
            font=("Segoe UI", 10), 
            bg="#2d3436", 
            fg="white", 
            insertbackground="white",
            relief="flat",
            bd=5
        )
        self.url_entry.pack(pady=(0, 20), ipady=8)
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame, bg="#1e1e1e")
        button_frame.pack(pady=10)
        
        # Bouton de téléchargement
        self.download_btn = tk.Button(
            button_frame,
            text="Télécharger la vidéo",
            command=self.download_tiktok,
            font=("Segoe UI", 11, "bold"),
            bg="#00b894",
            fg="white",
            activebackground="#00cec9",
            relief="flat",
            padx=30,
            pady=10,
            cursor="hand2"
        )
        self.download_btn.pack(side="left", padx=(0, 10))
        
        # Bouton pour effacer
        clear_btn = tk.Button(
            button_frame,
            text="Effacer",
            command=self.clear_url,
            font=("Segoe UI", 11),
            bg="#74b9ff",
            fg="white",
            activebackground="#0984e3",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        clear_btn.pack(side="left")
        
        # Barre de progression
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=400
        )
        self.progress.pack(pady=20)
        
        # Label de statut
        self.status_label = tk.Label(
            main_frame,
            text="Prêt à télécharger",
            font=("Segoe UI", 9),
            bg="#1e1e1e",
            fg="#636e72"
        )
        self.status_label.pack()
        
        # Label d'information
        info_label = tk.Label(
            main_frame,
            text="Utilise l'API tikmate.app pour télécharger sans watermark",
            font=("Segoe UI", 8),
            bg="#1e1e1e",
            fg="#636e72"
        )
        info_label.pack(side="bottom", pady=(20, 0))

    def validate_tiktok_url(self, url):
        """Valide et nettoie l'URL TikTok"""
        if not url:
            return None
            
        # Nettoyage de l'URL
        url = url.strip()
        
        # Supprimer les paramètres de requête inutiles
        if "?q=" in url:
            url = url.split("?")[0]
        
        # Vérifier si c'est une URL TikTok valide
        tiktok_patterns = [
            r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
            r'https?://(?:vm|vt)\.tiktok\.com/[\w-]+',
            r'https?://(?:www\.)?tiktok\.com/t/[\w-]+',
        ]
        
        for pattern in tiktok_patterns:
            if re.match(pattern, url):
                return url
                
        # Vérifier si c'est au moins un domaine TikTok
        if "tiktok.com" in url and url.startswith(("http://", "https://")):
            return url
            
        return None

    def update_status(self, message, color="#636e72"):
        """Met à jour le message de statut"""
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def clear_url(self):
        """Efface le champ URL"""
        self.url_entry.delete(0, tk.END)
        self.update_status("Prêt à télécharger")

    def download_tiktok(self):
        """Télécharge la vidéo TikTok"""
        user_url = self.url_entry.get().strip()
        
        # Validation de l'URL
        cleaned_url = self.validate_tiktok_url(user_url)
        if not cleaned_url:
            messagebox.showerror("Erreur", "Lien TikTok invalide.\n\nFormats acceptés:\n- https://www.tiktok.com/@user/video/123\n- https://vm.tiktok.com/abc123\n- https://vt.tiktok.com/abc123")
            return

        # Désactiver le bouton et démarrer la progression
        self.download_btn.config(state="disabled")
        self.progress.start(10)
        self.update_status("Récupération des informations de la vidéo...", "#74b9ff")

        try:
            # Configuration des headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "cross-site"
            }
            
            # Appel à l'API
            api_url = "https://api.tikmate.app/api/lookup"
            
            self.update_status("Connexion à l'API tikmate.app...", "#74b9ff")
            
            resp = requests.get(
                api_url, 
                params={"url": cleaned_url}, 
                headers=headers,
                timeout=30
            )
            
            if resp.status_code != 200:
                raise Exception(f"Erreur API: Code {resp.status_code}")
            
            try:
                data = resp.json()
            except ValueError:
                raise Exception("Réponse API invalide")
            
            if not data.get("token") or not data.get("id"):
                raise Exception("Token ou ID manquant dans la réponse API")

            video_id = data["id"]
            token = data["token"]
            
            # Construction du lien de téléchargement
            download_url = f"https://tikmate.app/download/{token}/{video_id}.mp4"
            
            self.update_status("Sélection du dossier de destination...", "#74b9ff")
            
            # Choisir où sauvegarder avec un nom par défaut
            default_filename = f"tiktok_video_{video_id}.mp4"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("Fichiers MP4", "*.mp4"), ("Tous les fichiers", "*.*")],
                initialvalue=default_filename,
                title="Enregistrer la vidéo TikTok"
            )
            
            if not file_path:
                self.update_status("Téléchargement annulé", "#e17055")
                return
            
            self.update_status("Téléchargement de la vidéo...", "#00b894")
            
            # Téléchargement de la vidéo
            video_response = requests.get(download_url, headers=headers, timeout=60)
            
            if video_response.status_code != 200:
                raise Exception(f"Impossible de télécharger la vidéo (Code: {video_response.status_code})")
            
            # Sauvegarde du fichier
            with open(file_path, "wb") as f:
                f.write(video_response.content)
            
            # Vérifier que le fichier a été créé et n'est pas vide
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # Taille en MB
                self.update_status(f"Téléchargement terminé ({file_size:.1f} MB)", "#00b894")
                messagebox.showinfo(
                    "Succès", 
                    f"Vidéo TikTok téléchargée avec succès ✅\n\nFichier: {os.path.basename(file_path)}\nTaille: {file_size:.1f} MB\nEmplacement: {file_path}"
                )
            else:
                raise Exception("Le fichier téléchargé est vide ou n'a pas pu être créé")

        except requests.exceptions.Timeout:
            messagebox.showerror("Erreur", "Délai d'attente dépassé. Vérifiez votre connexion internet.")
            self.update_status("Erreur: Délai d'attente dépassé", "#e17055")
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erreur", "Erreur de connexion. Vérifiez votre connexion internet.")
            self.update_status("Erreur: Pas de connexion internet", "#e17055")
            
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror("Erreur", f"Erreur lors du téléchargement:\n{error_msg}")
            self.update_status(f"Erreur: {error_msg}", "#e17055")
            
        finally:
            # Réactiver le bouton et arrêter la progression
            self.download_btn.config(state="normal")
            self.progress.stop()

    def run(self):
        """Lance l'application"""
        # Centrer la fenêtre
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()

if __name__ == "__main__":
    app = TikTokDownloader()
    app.run()