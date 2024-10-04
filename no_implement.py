def block_device(ip):
    """Bloquea un dispositivo usando iptables."""
    try:
        # A      adir regla a la cadena FORWARD
        subprocess.run(['sudo', 'iptables', '-A', 'FORWARD', '-s', ip, '-j', 'DROP'], check=True)
        # Tambi      n mantener la regla en INPUT
        subprocess.run(['sudo', 'iptables', '-A', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)
        blocked_devices = load_blocked_devices()
        blocked_devices.append(ip)
        save_blocked_devices(blocked_devices)
        print(f"Dispositivo {ip} bloqueado.")
    except subprocess.CalledProcessError:
        print(f"Error al bloquear el dispositivo {ip}.")

def unblock_device(ip):
    """Desbloquea un dispositivo usando iptables."""
    try:
        subprocess.run(['sudo', 'iptables', '-D', 'FORWARD', '-s', ip, '-j', 'DROP'], check=True)
        subprocess.run(['sudo', 'iptables', '-D', 'INPUT', '-s', ip, '-j', 'DROP'], check=True)

        # Manejo de la lista de dispositivos bloqueados
        blocked_devices = load_blocked_devices()
        blocked_devices.remove(ip)  # Remueve el IP de la lista de bloqueados
        save_blocked_devices(blocked_devices)
        print(f"Dispositivo {ip} desbloqueado.")
    except subprocess.CalledProcessError:
        print(f"Error al desbloquear el dispositivo {ip}.")
    except ValueError:
        print(f"El dispositivo {ip} no est       en la lista de bloqueados.")
    except Exception as e:
        print(f"Ocurri       un error: {e}")