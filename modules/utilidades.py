# utilidades.py
import os, time

def Limpiar_consola():
    """Limpia la pantalla según el sistema operativo."""
    limpia = os.system("cls" if os.name == "nt" else "clear")
    return limpia

def Stop():
    time.sleep(1)