import os
import subprocess
import re
from collections import defaultdict

#Host control, start, restart y stop functionalities

def start_server():
    subprocess.run( ['sudo','systemctl','start','hostapd']) 

def restart_server():
    subprocess.run('sudo','systemctl','restart','hostapd')

def stop_server():
    subprocess.run('sudo','systemctl','stop','hostapd')



#### Wifi-Detected
#### Escanea los canales disponibles y se retorna los canales más libre.

def scan_channels(interface):
    subprocess.run(
    ['sudo','systemctl','stop','hostapd'])
    """
    Escanea los canales Wi-Fi en busca de redes activas y retorna la cantidad de redes por canal.
    """
    print(f"Escaneando canales Wi-Fi en la interfaz {interface}...")

    try:
        # Ejecutar el comando iwlist para escanear canales
        result = subprocess.run(
            ['sudo', 'iwlist', interface, 'scan'],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            print(f"Error al escanear canales: {result.stderr}")
            return {}

        # Procesar la salida para contar redes por canal
        channels_usage = defaultdict(int)
        cells = result.stdout.split("Cell ")

        for cell in cells[1:]:
            # Extraer el canal
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
    Selecciona los 'n' mejores canales con menos uso.
    """
    if not channels_usage:
        print("No se encontraron canales disponibles.")
        return None

    # Ordenar los canales por el n      mero de redes en cada uno (de menor a mayor)
    sorted_channels = sorted(channels_usage.items(), key=lambda x: x[1])

    # Obtener los 'n' mejores canales
    best_channels = sorted_channels[:n]

    print(f"Mejores {n} canales encontrados:")
    for channel, usage in best_channels:
        print(f"Canal {channel}: {usage} redes.")

    return [channel for channel, usage in best_channels]

#Modifica las lines del archivo de configuración del hostapd
def configure_hostapd(channel, hostapd_conf_path='/etc/hostapd/hostapd.conf'):


    try:
        # Leer el archivo hostapd.conf
        with open(hostapd_conf_path, 'r') as file:
            config = file.readlines()

        # Actualizar el canal en el archivo de configuracion
        with open(hostapd_conf_path, 'w') as file:
            for line in config:
                if line.startswith('channel='):
                    file.write(f'channel={channel}\n')  # Utiliza el primer canal de la lista
                else:
                    file.write(line)

        print(f"Archivo {hostapd_conf_path} actualizado con el canal {channel}.")

    except Exception as e:
        print(f"Error al configurar hostapd: {e}")

        

def Channels():

    network_interface = "wlan0"

    # Escanear los canales disponibles
    channels_usage = scan_channels(network_interface)

    # Seleccionar los 3 mejores canales
    best_channels = select_best_channels(channels_usage, n=3)

    subprocess.run(['sudo','systemctl','start','hostapd'])

    return best_channels




def scan_network(interface):
    """
    Scans the network using arp-scan and returns the list of IPs and MAC addresses.
    """
    print(f"Escaneando la red en la interfaz {interface}...")

    try:
        result = subprocess.run(['sudo', 'arp-scan', '-l', '-I', interface], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"Error al ejecutar arp-scan: {result.stderr}")
            return [], [], []

        # Process the arp-scan output
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
                    names.append(f"Dispositivo {len(names) + 1}")  # Asignar nombres genéricos

        return ips, macs, names

    except Exception as e:
        print(f"Hubo un error al escanear la red: {e}")
        return [], [], []

def devices():
    """
    Función que retorna la cantidad de dispositivos, sus nombres, IPs y MACs.
    """
    network_interface = "wlan0"
    
    ips, macs, names = scan_network(network_interface)
    number = len(ips)

    return number, names, ips, macs

