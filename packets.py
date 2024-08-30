from scapy.all import IP, ICMP, send, Raw
import random
import time
import string
import struct

def caesar():
    word = input('Ingrese la palabra a cifrar: ')
    desp = int(input('Ingrese el desplazamiento: ')) 
    caesrMsg = ''
    for w in word:
        if w in string.ascii_lowercase:
            newChar = chr((ord(w) - ord('a') + desp) % 26 + ord('a'))
            caesrMsg += newChar
        elif w in string.ascii_uppercase:
            newChar = chr((ord(w) - ord('A') + desp) % 26 + ord('A'))
            caesrMsg += newChar
        elif w in string.digits:
            newChar = chr((ord(w) - ord('0') + desp) % 10 + ord('0'))
            caesrMsg += newChar
        elif w == ' ':
            caesrMsg += ' '
        else:
            newChar = chr(ord(w) + desp)
            caesrMsg += newChar
    return caesrMsg

def send_icmp_packets(message, target_ip):
    id_base = random.randint(0, 65535)
    seq_base = random.randint(0, 65535)
    
    for i, char in enumerate(message):
        # Construir la carga útil personalizada
        icmp_payload = struct.pack('!d', time.time()) + (b'\x00' * 6) + char.encode() + (b'\x00' * (56 - len(char.encode())))

        # Crear el paquete ICMP
        icmp_packet = IP(dst=target_ip)/ICMP(
            id=id_base,  # ID coherente
            seq=seq_base + i  # Número de secuencia coherente
        )/Raw(load=icmp_payload)
        
        send(icmp_packet)
        print(f"Paquete ICMP enviado con carga útil: {char}, Seq: {seq_base + i}, ID: {id_base}")

if __name__ == "__main__":
    # Cifrar el mensaje
    encrypted_message = caesar()
    
    # Dirección IP del servidor DNS al que quieres enviar los paquetes (Google DNS)
    target_ip = "8.8.8.8"
    
    # Enviar los paquetes ICMP
    send_icmp_packets(encrypted_message, target_ip)
