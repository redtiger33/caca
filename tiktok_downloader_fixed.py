import requests
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import os
import re
import json
from urllib.parse import urlparse, parse_qs
import time

class TikTokDownloader:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        
    def setup_ui(self):
        """Configuration de l'interface utilisateur"""
        self.root.title("TikTok Downloader - Version Améliorée")
        self.root.geometry("650x350")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#1e1e1e")
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Titre
        title_label = tk.Label(
            main_frame, 
            text="TikTok Video Downloader", 
            font=("Arial", 18, "bold"), 
            bg="#1e1e1e", 
            fg="#00b894"
        )
        title_label.pack(pady=(0, 20))
        
        # Label pour l'URL
        url_label = tk.Label(
            main_frame, 
            text="Collez le lien TikTok ici :", 
            font=("Arial", 12), 
            bg="#1e1e1e", 
            fg="white"
        )
        url_label.pack(anchor="w", pady=(0, 5))
        
        # Entry pour l'URL
        self.url_entry = tk.Entry(
            main_frame, 
            width=70, 
            font=("Arial", 11), 
            bg="#2d3436", 
            fg="white", 
            insertbackground="white",
            relief="flat",
            bd=5
        )
        self.url_entry.pack(pady=(0, 20), ipady=10)
        self.url_entry.bind('<Return>', lambda e: self.download_tiktok())
        
        # Frame pour les boutons
        button_frame = tk.Frame(main_frame, bg="#1e1e1e")
        button_frame.pack(pady=15)
        
        # Bouton de téléchargement
        self.download_btn = tk.Button(
            button_frame,
            text="📥 Télécharger",
            command=self.download_tiktok,
            font=("Arial", 12, "bold"),
            bg="#00b894",
            fg="white",
            activebackground="#00cec9",
            relief="flat",
            padx=25,
            pady=12,
            cursor="hand2"
        )
        self.download_btn.pack(side="left", padx=(0, 15))
        
        # Bouton pour effacer
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ Effacer",
            command=self.clear_url,
            font=("Arial", 12),
            bg="#74b9ff",
            fg="white",
            activebackground="#0984e3",
            relief="flat",
            padx=20,
            pady=12,
            cursor="hand2"
        )
        clear_btn.pack(side="left")
        
        # Barre de progression
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate', 
            length=450,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress.pack(pady=20)
        
        # Label de statut
        self.status_label = tk.Label(
            main_frame,
            text="Prêt à télécharger une vidéo TikTok",
            font=("Arial", 10),
            bg="#1e1e1e",
            fg="#a8a8a8"
        )
        self.status_label.pack(pady=(0, 10))
        
        # Frame d'information
        info_frame = tk.Frame(main_frame, bg="#2d3436", relief="flat", bd=1)
        info_frame.pack(fill="x", pady=(10, 0))
        
        info_text = """💡 Formats d'URL supportés:
• https://www.tiktok.com/@username/video/123456789
• https://vm.tiktok.com/ZM123abc/
• https://vt.tiktok.com/ZS123abc/
• https://www.tiktok.com/t/ZT123abc/"""
        
        info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg="#2d3436",
            fg="#b2bec3",
            justify="left"
        )
        info_label.pack(padx=15, pady=10)

    def extract_video_id(self, url):
        """Extrait l'ID de la vidéo depuis différents formats d'URL TikTok"""
        # Pattern pour les URLs standard
        patterns = [
            r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/(\d+)',
            r'https?://(?:vm|vt)\.tiktok\.com/([\w-]+)',
            r'https?://(?:www\.)?tiktok\.com/t/([\w-]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def resolve_short_url(self, url):
        """Résout les URLs courtes TikTok vers l'URL complète"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.head(url, headers=headers, allow_redirects=True, timeout=10)
            return response.url
        except:
            return url

    def clean_tiktok_url(self, url):
        """Nettoie et valide l'URL TikTok"""
        if not url:
            return None
            
        url = url.strip()
        
        # Supprimer les paramètres inutiles
        if "?q=" in url:
            url = url.split("?")[0]
        if "&" in url and "?" not in url:
            url = url.split("&")[0]
            
        # Résoudre les URLs courtes
        if any(domain in url for domain in ['vm.tiktok.com', 'vt.tiktok.com', 'tiktok.com/t/']):
            url = self.resolve_short_url(url)
        
        # Vérifier si c'est une URL TikTok valide
        if "tiktok.com" not in url or not url.startswith(("http://", "https://")):
            return None
            
        return url

    def update_status(self, message, color="#a8a8a8"):
        """Met à jour le message de statut"""
        self.status_label.config(text=message, fg=color)
        self.root.update()

    def clear_url(self):
        """Efface le champ URL"""
        self.url_entry.delete(0, tk.END)
        self.update_status("Prêt à télécharger une vidéo TikTok")

    def try_multiple_apis(self, tiktok_url):
        """Essaie plusieurs APIs/méthodes pour télécharger la vidéo"""
        
        # API 1: TikMate (version mise à jour)
        try:
            self.update_status("Tentative avec l'API TikMate...", "#74b9ff")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Referer': 'https://tikmate.app/',
                'Origin': 'https://tikmate.app'
            }
            
            # Nouvelle API endpoint
            api_url = "https://api.tikmate.app/api/lookup"
            data = {
                'url': tiktok_url
            }
            
            response = requests.post(api_url, json=data, headers=headers, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('token') and result.get('id'):
                    download_url = f"https://tikmate.app/download/{result['token']}/{result['id']}.mp4"
                    return download_url, "TikMate"
                    
        except Exception as e:
            print(f"TikMate API error: {e}")
        
        # API 2: Alternative TikTok downloader
        try:
            self.update_status("Tentative avec une API alternative...", "#74b9ff")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            api_url = "https://www.tikwm.com/api/"
            params = {
                'url': tiktok_url,
                'hd': '1'
            }
            
            response = requests.get(api_url, params=params, headers=headers, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 0 and result.get('data', {}).get('play'):
                    return result['data']['play'], "TikWM"
                    
        except Exception as e:
            print(f"TikWM API error: {e}")
        
        # API 3: Backup downloader
        try:
            self.update_status("Tentative avec l'API de secours...", "#74b9ff")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            api_url = "https://tikdown.org/api/ajaxSearch"
            data = {
                'q': tiktok_url,
                'lang': 'en'
            }
            
            response = requests.post(api_url, data=data, headers=headers, timeout=20)
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'ok':
                    # Parse HTML response to extract download link
                    import re
                    html = result.get('data', '')
                    video_match = re.search(r'href="([^"]+)"[^>]*>Download MP4', html)
                    if video_match:
                        return video_match.group(1), "TikDown"
                        
        except Exception as e:
            print(f"TikDown API error: {e}")
            
        return None, None

    def download_tiktok(self):
        """Télécharge la vidéo TikTok"""
        user_url = self.url_entry.get().strip()
        
        if not user_url:
            messagebox.showwarning("Attention", "Veuillez coller un lien TikTok")
            return
        
        # Validation et nettoyage de l'URL
        cleaned_url = self.clean_tiktok_url(user_url)
        if not cleaned_url:
            messagebox.showerror("Erreur", "Lien TikTok invalide.\n\nAssurez-vous que le lien commence par https:// et contient tiktok.com")
            return

        # Désactiver le bouton et démarrer la progression
        self.download_btn.config(state="disabled")
        self.progress.start(10)
        self.update_status("Préparation du téléchargement...", "#74b9ff")

        try:
            # Essayer plusieurs APIs
            download_url, api_used = self.try_multiple_apis(cleaned_url)
            
            if not download_url:
                raise Exception("Aucune API n'a pu traiter cette vidéo.\nLa vidéo pourrait être privée ou le lien invalide.")
            
            self.update_status(f"Vidéo trouvée via {api_used}! Sélection du dossier...", "#74b9ff")
            
            # Générer un nom de fichier par défaut
            video_id = self.extract_video_id(cleaned_url) or str(int(time.time()))
            default_filename = f"tiktok_{video_id}.mp4"
            
            # Choisir où sauvegarder
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4",
                filetypes=[("Fichiers MP4", "*.mp4"), ("Tous les fichiers", "*.*")],
                initialvalue=default_filename,
                title="Enregistrer la vidéo TikTok"
            )
            
            if not file_path:
                self.update_status("Téléchargement annulé", "#e17055")
                return
            
            self.update_status("Téléchargement en cours...", "#00b894")
            
            # Télécharger la vidéo
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://www.tiktok.com/'
            }
            
            video_response = requests.get(download_url, headers=headers, timeout=60, stream=True)
            
            if video_response.status_code != 200:
                raise Exception(f"Échec du téléchargement (Code HTTP: {video_response.status_code})")
            
            # Sauvegarder avec barre de progression
            total_size = int(video_response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(file_path, "wb") as f:
                for chunk in video_response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            self.update_status(f"Téléchargement... {progress:.1f}%", "#00b894")
            
            # Vérifier le fichier téléchargé
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
                self.update_status(f"✅ Téléchargement terminé ({file_size:.1f} MB)", "#00b894")
                
                messagebox.showinfo(
                    "Succès! 🎉", 
                    f"Vidéo téléchargée avec succès!\n\n"
                    f"📁 Fichier: {os.path.basename(file_path)}\n"
                    f"📊 Taille: {file_size:.1f} MB\n"
                    f"🔧 API utilisée: {api_used}\n"
                    f"📍 Emplacement: {file_path}"
                )
            else:
                raise Exception("Le fichier téléchargé est vide ou corrompu")

        except requests.exceptions.Timeout:
            messagebox.showerror("Erreur", "⏰ Délai d'attente dépassé.\nVérifiez votre connexion internet.")
            self.update_status("Erreur: Délai d'attente dépassé", "#e17055")
            
        except requests.exceptions.ConnectionError:
            messagebox.showerror("Erreur", "🌐 Erreur de connexion.\nVérifiez votre connexion internet.")
            self.update_status("Erreur: Pas de connexion internet", "#e17055")
            
        except Exception as e:
            error_msg = str(e)
            messagebox.showerror("Erreur", f"❌ Erreur lors du téléchargement:\n\n{error_msg}")
            self.update_status(f"Erreur: {error_msg[:50]}...", "#e17055")
            
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
        
        # Message de bienvenue
        self.update_status("Prêt à télécharger! Collez un lien TikTok et appuyez sur Entrée", "#00b894")
        
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = TikTokDownloader()
        app.run()
    except ImportError as e:
        print(f"Erreur d'importation: {e}")
        print("Installez les dépendances avec: pip install requests")
    except Exception as e:
        print(f"Erreur: {e}")