from scapy.all import IP, ICMP, send, Raw, rdpcap
from colorama import Fore, Style
import string
from collections import defaultdict

# Frecuencia aproximada de apariciones de letras en español
LETTER_FREQUENCIES = {
    'a': 11.72, 'b': 1.49, 'c': 3.87, 'd': 4.67, 'e': 13.72,
    'f': 0.69, 'g': 1.00, 'h': 0.70, 'i': 5.28, 'j': 0.52,
    'k': 0.11, 'l': 5.24, 'm': 3.08, 'n': 6.83, 'ñ': 0.31,
    'o': 8.44, 'p': 2.89, 'q': 1.11, 'r': 6.41, 's': 7.20,
    't': 4.60, 'u': 4.55, 'v': 1.05, 'w': 0.04, 'x': 0.14,
    'y': 1.09, 'z': 0.47
}
# Frecuencia de aparición de pares de letras en español
LETTER_PAIR_FREQUENCIES = defaultdict(lambda: 0.01, {
    'qu': 1.0, 'el': 0.98, 'la': 0.95, 'de': 0.93, 'en': 0.90,
    'es': 0.85, 'os': 0.83, 'ar': 0.80, 'al': 0.78, 're': 0.75
})

def caesar_decrypt(ciphertext, shift):
    plaintext = ''
    for char in ciphertext:
        if char in string.ascii_lowercase:
            new_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            plaintext += new_char
        elif char in string.ascii_uppercase:
            new_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            plaintext += new_char
        elif char in string.digits:
            new_char = chr((ord(char) - ord('0') - shift) % 10 + ord('0'))
            plaintext += new_char
        else:
            plaintext += char
    return plaintext

def score_message(message):
    letter_score = 0.0
    number_score = 0.0
    message = message.lower()
    
    # Sumar las frecuencias de las letras individuales
    for char in message:
        if char in LETTER_FREQUENCIES:
            letter_score += LETTER_FREQUENCIES[char]
        elif char in string.digits:
            number_score += 2.0  # Puntaje adicional para los números
    
    # Sumar las frecuencias de pares de letras
    for i in range(len(message) - 1):
        pair = message[i:i + 2]
        if pair in LETTER_PAIR_FREQUENCIES:
            letter_score += LETTER_PAIR_FREQUENCIES[pair]

    # Combinar puntajes
    total_score = letter_score + number_score
    return total_score

def find_most_probable_message(ciphertext):
    possible_messages = []
    for shift in range(26):
        decrypted_message = caesar_decrypt(ciphertext, shift)
        score = score_message(decrypted_message)
        possible_messages.append((decrypted_message, score, shift))
    
    # Encontrar el mensaje con la mayor puntuación
    best_message = max(possible_messages, key=lambda x: x[1])
    
    # Ordenar la lista por desplazamiento, no por la puntuación
    possible_messages.sort(key=lambda x: x[2])  # Ordenar por 'shift'
    
    return possible_messages, best_message

def extract_icmp_data(pcap_file):
    packets = rdpcap(pcap_file)
    extracted_data = ''
    
    for packet in packets:
        if ICMP in packet and packet[ICMP].type == 8:  # Solo mensajes ICMP Echo Request
            data = bytes(packet[Raw].load)
            extracted_data += chr(data[8])  # Extraemos el caracter cifrado
    
    return extracted_data

def main(pcap_file):
    encrypted_message = extract_icmp_data(pcap_file)
    possible_messages, best_message = find_most_probable_message(encrypted_message)
    
    print("Combinaciones posibles:")
    for (message, score, shift) in possible_messages:
        if message == best_message[0]:
            print(f"{shift:2d} {Fore.GREEN}{message}{Style.RESET_ALL}")
        else:
            print(f"{shift:2d} {message}")

if __name__ == "__main__":
    pcap_file = './ejemplo2.pcapng'
    main(pcap_file)
