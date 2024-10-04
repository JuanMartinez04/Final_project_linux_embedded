import os
import subprocess
import re
from collections import defaultdict



def start_server():
    subprocess.run(['sudo','systemctl','start','hostapd'])
    subprocess.run(['sudo','systemctl','start','isc-dhcp-sever'])

def restart_server():
    subprocess.run('sudo','systemctl','restart','hostapd')
    subprocess.run('sudo','systemctl','restart','isc-dhcp-sever')

def stop_server():
    subprocess.run('sudo','systemctl','stop','hostapd')
    subprocess.run('sudo','systemctl','stop','isc-dhcp-sever')



#### Wifi-Detected
#### Escanea los canales disponibles y se conecta al canal mas libre.

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

    subprocess.run(
    ['sudo','systemctl','start','hostapd'])

    return best_channels



    







### Detecta os dispositivos conectados a la red y nos entrega su MAC y su direccion ip, adicional a ello 
# def scan_network(interface):
#     """
#     Scans the network using arp-scan and returns the list of IPs and MAC addresses.
#     """
#     print(f"Escaneando la red en la interfaz {interface}...")

#     try:
#         # Running the arp-scan command to discover connected devices
#         result = subprocess.run(['sudo', 'arp-scan', '-l', '-I', interface],capture_output=True, text=True)

#         if result.returncode != 0:
#             print(f"Error al ejecutar arp-scan: {result.stderr}")
#             return []

#         # Process the arp-scan output
#         devices = []
#         for line in result.stdout.splitlines():
#             if "\t" in line:
#                 parts = line.split("\t")
#                 if len(parts) >= 2:
#                     ip = parts[0].strip()
#                     mac = parts[1].strip()
#                     devices.append((ip, mac))

#         return devices

#     except Exception as e:
#         print(f"Hubo un error al escanear la red: {e}")
#         return []
    

# def get_device_info(ip):
#     """
#     Use nmap to get detailed information about a specific device (IP).
#     """
#     print(f"Obteniendo informaci      n detallada del dispositivo en {ip}...")

#     try:
#         # Running the nmap command for detailed information
#         result = subprocess.run(
#             ['sudo', 'nmap', '-sP', ip],  # Scan for ping and services
#             capture_output=True, text=True
#         )

#         if result.returncode == 0:
#             return result.stdout
#         else:
#             return f"Error al escanear {ip}: {result.stderr}"

#     except Exception as e:
#         return f"Error al ejecutar nmap para {ip}: {e}"

# def extract_hostname(nmap_output):
#     """
#     Extract the hostname from the nmap output.
#     """
#     hostnames = {}

#     # Extracting the IP and hostname
#     current_ip = ""
#     for line in nmap_output.splitlines():
#         if "Nmap scan report for" in line:
#             current_ip = line.split(" ")[-1]  # The last part is the IP address
#         elif "MAC Address:" in line:
#             # Attempt to extract the hostname from the MAC address line
#             hostname_match = re.search(r'\((.*?)\)', line)
#             hostname = hostname_match.group(1) if hostname_match else "Unknown"
#             hostnames[current_ip] = hostname

#     return hostnames    

# if __name__ == "__main__":
#     # Replace 'wlan0' with your actual interface name
#     network_interface = "wlan0"

#     # First, scan the network using arp-scan
#     devices = scan_network(network_interface)

#     if not devices:
#         print("No se encontraron dispositivos.")
#     else:
#         print("\nDispositivos conectados encontrados:")
#         for idx, (ip, mac) in enumerate(devices, start=1):
#             print(f"{idx}. IP: {ip}, MAC: {mac}")

#         # For each discovered device, run a detailed scan with nmap
#         for ip, mac in devices:
#             detailed_info = get_device_info(ip)
#             print(f"\nInformaci      n detallada para {ip} ({mac}):\n{detailed_info}")

#             # Extract hostname from nmap output
#             hostnames = extract_hostname(detailed_info)
#             if ip in hostnames:
#                 print(f"Nombre de dispositivo: {hostnames[ip]}")
#             else:
#                 print(f"Nombre de dispositivo: Desconocido")



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

