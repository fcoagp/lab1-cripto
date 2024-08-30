from scapy.all import IP, ICMP, send, Raw
import random
import time
import struct
import string
from caesar import caesar

def send_icmp_packets(message, target_ip):
    id_base = random.randint(0, 65535)
    seq_base = random.randint(0, 65535)
    
    for i, char in enumerate(message):
        # Timestamp en segundos (32 bits)
        timestamp_sec = int(time.time()) & 0xFFFFFFFF
        # Timestamp en microsegundos (32 bits)
        timestamp_usec = int((time.time() * 1000000) % 1000000) & 0xFFFFFFFF
        
        # Crear la carga útil del ICMP, con el timestamp y padding
        icmp_payload = struct.pack('!II', timestamp_sec, timestamp_usec)  # 8 bytes para el timestamp
        icmp_payload += char.encode()  # Añadir el carácter cifrado

        icmp_payload += b'\x00' * 7   # Añadir padding hasta completar 64 bytes
        
        chain = b''

        for i in range(0x10, 0x38): # Payload ICMP
            chain += bytes([i])

        icmp_payload += chain
        # Crear el paquete ICMP
        icmp_packet = IP(dst=target_ip)/ICMP(
            id=id_base,  # ID coherente
            seq=seq_base + i  # Número de secuencia coherente
        )/Raw(load=icmp_payload)
        
        # Enviar el paquete ICMP
        send(icmp_packet)
        print(f"Paquete ICMP enviado con carga útil: {char}, Seq: {seq_base + i}, ID: {id_base}, Timestamp: {timestamp_sec}, {timestamp_usec}")
        
        # Esperar un segundo antes de enviar el siguiente paquete
        time.sleep(1)

if __name__ == "__main__":
    # Cifrar el mensaje
    encrypted_message = caesar()
    
    # Dirección IP del servidor DNS al que quieres enviar los paquetes (Google DNS)
    target_ip = "8.8.8.8"
    
    # Enviar los paquetes ICMP
    send_icmp_packets(encrypted_message, target_ip)
