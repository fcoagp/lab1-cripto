import string 

def caesar(word, desp):
    caesrMsg=''
    for w in word:
        if w in string.ascii_lowercase or w in string.ascii_uppercase:
            newChar = chr((ord(w) - ord('a') + desp) % 26 + ord('a'))
            caesrMsg += newChar
        elif w == ' ':
            caesrMsg+=w
        else:
            newChar= chr(ord(w) + desp)
            caesrMsg += newChar
    print(caesrMsg)

#newWord = input('Ingrese la palabra a cifrar: ')
#newDesp = int(input('Ingrese el desplazamiento: ')) 
#caesar(newWord,newDesp)

caesar('criptografia y seguridad en redes 1209"!#"!$%#"',9)

