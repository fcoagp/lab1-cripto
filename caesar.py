import string

def caesar(word, desp):
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
    print(caesrMsg)

newWord = input('Ingrese la palabra a cifrar: ')
newDesp = int(input('Ingrese el desplazamiento: ')) 
caesar(newWord,newDesp)



