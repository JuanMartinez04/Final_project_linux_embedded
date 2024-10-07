import os
import subprocess
import re
from collections import defaultdict

# Host control: Funcionalidades para iniciar, reiniciar y detener el servidor hostapd.

def start_server():
    """
    Inicia el servicio 'hostapd'.
    """
    subprocess.run(['sudo','systemctl','start','hostapd']) 

def restart_server():
    """
    Reinicia el servicio 'hostapd'.
    """
    subprocess.run(['sudo','systemctl','restart','hostapd'])

def stop_server():
    """
    Detiene el servicio 'hostapd'.
    """
    subprocess.run(['sudo','systemctl','stop','hostapd'])


#### Escaneo de canales Wi-Fi disponibles y selección de los menos ocupados.

def scan_channels(interface):
    """
    Escanea los canales Wi-Fi en busca de redes activas y retorna la cantidad de redes por canal.
    
    Parámetros:
    - interface: la interfaz de red que se va a usar para el escaneo, en este caso "wlan0"

    Retorna:
    - Un diccionario con el número de redes por cada canal detectado.
    """
    # Detiene el servicio hostapd antes de escanear.
    subprocess.run(['sudo','systemctl','stop','hostapd'])

    print(f"Escaneando canales Wi-Fi en la interfaz {interface}...")

    try:
        # Ejecutar el comando 'iwlist' para escanear canales.
        result = subprocess.run(
            ['sudo', 'iwlist', interface, 'scan'],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"Error al escanear canales: {result.stderr}")
            return {}

        # Procesar la salida para contar redes por canal.
        channels_usage = defaultdict(int)
        cells = result.stdout.split("Cell ")

        for cell in cells[1:]:
            # Extraer el canal de cada red detectada.
            channel = re.search(r"Channel:(\d+)", cell)
            if channel:
                channel = int(channel.group(1))
                channels_usage[channel] += 1

        return channels_usage

    except Exception as e:
        print(f"Error al escanear canales: {e}")
        return {}

def select_best_channels(channels_usage, n=3):
    """
    Selecciona los 'n' mejores canales (menos congestionados) con menos uso.

    Parámetros:
    - channels_usage: diccionario con el número de redes por canal.
    - n: cantidad de canales a seleccionar (por defecto 3).

    Retorna:
    - Lista con los 3 mejores canales.
    """
    if not channels_usage:
        print("No se encontraron canales disponibles.")
        return None

    # Ordenar los canales por el número de redes en cada uno (de menor a mayor).
    sorted_channels = sorted(channels_usage.items(), key=lambda x: x[1])

    # Obtener los 'n' mejores canales.
    best_channels = sorted_channels[:n]

    print(f"Mejores {n} canales encontrados:")
    for channel, usage in best_channels:
        print(f"Canal {channel}: {usage} redes.")

    return [channel for channel, usage in best_channels]


# Modifica el archivo de configuración del hostapd para seleccionar el canal óptimo.

def configure_hostapd(channel, hostapd_conf_path='/etc/hostapd/hostapd.conf'):
    """
    Configura el archivo hostapd.conf para cambiar el canal utilizado por el punto de acceso.

    Parámetros:
    - channel: el canal a configurar en hostapd.
    - hostapd_conf_path: ruta del archivo de configuración de hostapd (por defecto '/etc/hostapd/hostapd.conf').
    """
    try:
        # Leer el archivo hostapd.conf.
        with open(hostapd_conf_path, 'r') as file:
            config = file.readlines()

        # Actualizar el canal en el archivo de configuración.
        with open(hostapd_conf_path, 'w') as file:
            for line in config:
                if line.startswith('channel='):
                    file.write(f'channel={channel}\n')  # Utiliza el primer canal de la lista.
                else:
                    file.write(line)

        print(f"Archivo {hostapd_conf_path} actualizado con el canal {channel}.")

    except Exception as e:
        print(f"Error al configurar hostapd: {e}")


def Channels():
    """
    Realiza un escaneo de canales Wi-Fi y selecciona los 3 mejores canales disponibles.
    
    Retorna:
    - Lista con los mejores canales.
    """
    network_interface = "wlan0"

    # Escanear los canales disponibles.
    channels_usage = scan_channels(network_interface)

    # Seleccionar los 3 mejores canales.
    best_channels = select_best_channels(channels_usage, n=3)

    # Reinicia el servicio hostapd.
    subprocess.run(['sudo','systemctl','start','hostapd'])

    return best_channels


#### Escaneo de dispositivos conectados en la red mediante ARP-scan.

def scan_network(interface):
    """
    Escanea la red utilizando arp-scan y retorna las listas de IPs y direcciones MAC de los dispositivos conectados.

    Parámetros:
    - interface: la interfaz de red utilizada para el escaneo (p. ej., 'wlan0').

    Retorna:
    - Una lista de IPs, una lista de direcciones MAC y una lista de nombres asignados.
    """
    print(f"Escaneando la red en la interfaz {interface}...")

    try:
        # Ejecutar el comando arp-scan.
        result = subprocess.run(['sudo', 'arp-scan', '-l', '-I', interface], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error al ejecutar arp-scan: {result.stderr}")
            return [], [], []

        # Procesar la salida de arp-scan.
        ips = []
        macs = []
        names = []
        for line in result.stdout.splitlines():
            if "\t" in line:
                parts = line.split("\t")
                if len(parts) >= 2:
                    ip = parts[0].strip()
                    mac = parts[1].strip()
                    ips.append(ip)
                    macs.append(mac)
                    names.append(f"User {len(names) + 1}")  # Asignar nombres genéricos.

        return ips, macs, names

    except Exception as e:
        print(f"Hubo un error al escanear la red: {e}")
        return [], [], []

def devices():
    """
    Función que retorna la cantidad de dispositivos conectados, junto con sus nombres, IPs y MACs.

    Retorna:
    - Número de dispositivos conectados.
    - Lista de nombres asignados a los dispositivos.
    - Lista de direcciones IP de los dispositivos.
    - Lista de direcciones MAC de los dispositivos.
    """
    network_interface = "wlan0"
    
    # Escanea la red para obtener dispositivos conectados.
    ips, macs, names = scan_network(network_interface)
    number = len(ips)

    return number, names, ips, macs
