#!/usr/bin/env python3
"""
Script de configuration pour TikTok Downloader
Installe automatiquement les dépendances nécessaires
"""

import subprocess
import sys
import os

def install_package(package):
    """Installe un package Python"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def install_system_packages():
    """Installe les packages système nécessaires"""
    try:
        # Essayer d'installer tkinter via apt (pour Ubuntu/Debian)
        subprocess.check_call(["sudo", "apt", "update"])
        subprocess.check_call(["sudo", "apt", "install", "-y", "python3-tk", "python3-requests"])
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🚀 Configuration de TikTok Downloader...")
    
    # Vérifier Python
    if sys.version_info < (3, 6):
        print("❌ Python 3.6+ requis")
        return False
    
    # Essayer d'importer tkinter
    try:
        import tkinter
        print("✅ tkinter disponible")
    except ImportError:
        print("⚠️  tkinter non disponible, tentative d'installation...")
        if not install_system_packages():
            print("❌ Impossible d'installer tkinter automatiquement")
            print("   Installez manuellement avec: sudo apt install python3-tk")
            return False
    
    # Installer requests
    try:
        import requests
        print("✅ requests disponible")
    except ImportError:
        print("📦 Installation de requests...")
        if install_package("requests"):
            print("✅ requests installé")
        else:
            print("❌ Échec de l'installation de requests")
            return False
    
    print("\n🎉 Configuration terminée!")
    print("Lancez le programme avec: python3 tiktok_downloader_fixed.py")
    return True

if __name__ == "__main__":
    main()