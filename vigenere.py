import os
import collections

# Variaveis Globais Configuraveis
# Path do arquivo de texto
FILE_NAME = 'cipher1.txt'

# Lingua - "EN"/"PT". Default: "EN"
LANGUAGE = "EN"

# Tamanho maximo de chave para procurar antes de utilizar o valor mais proximo
MAX_KEY_SIZE = 12

# Variaveis Globais Fixas
FILE_PATH = os.getcwd() + '/enunciado/Cifrados/' + FILE_NAME

# Indice de coincidencia medio - Fonte: https://en.wikipedia.org/wiki/Index_of_coincidence
AVERAGE_IC_EN = 1.76/26 # 0.0677
AVERAGE_IC_PT = 1.93/26 # 0.0742

# Letras mais frequentes por lingua - Fonte: https://en.wikipedia.org/wiki/Letter_frequency
MOST_FREQUENT_EN = 'ETAOINSHRDLCUMWFGYPBVKJXQZ'
MOST_FREQUENT_PT = 'AEOSRIDMNTCULPVGQBFHZJXWKY'

def readAndFormatText():
    text = ''  
    with open(FILE_PATH, 'r') as file:
        text = file.read().replace('\n', '')
    return text.upper()

def printFormattedIc(ic):
    print("%.3f" % ic)

# Calculando IC
def calculateIc(text):
    # 26 Letras do alfabeto ingles
    LETTERS = map(chr, range(ord('A'), ord('Z')+1))
    n = len(text)
    occurences = collections.Counter(text)
    
    sum = 0.0
    for l in LETTERS:
        sum += occurences[l] * (occurences[l] - 1)

    return sum/(n*(n-1))

# Calculando IC com "saltos" entre caracteres(incrementos), retorna a média para aquele tamanho de incremento
def calculateIcWithJump(text, jumpSize):
    ic = [None] * jumpSize

    for i in range(0, jumpSize):
        newText = ""
        for j in range(i, len(text), jumpSize):
            newText += text[j]
        ic[i] = calculateIc(newText);
        # print("{} - {}".format(i, "%.3f" % ic[i]))

    averageIc = sum(ic) / len(ic)
    return averageIc

def findKeySize(text, averageIc):
    icDifferences = [None] * (MAX_KEY_SIZE - 1)
    i = 1
    while(i < MAX_KEY_SIZE):
        ic = calculateIcWithJump(text, i)
        
        print("{} - {}".format(i, "%.3f" % ic))
        
        icDifference = ic - averageIc
        if(icDifference > 0):
            # Fiz uma pequena adaptacao para corrigir alguns casos que estava dando errado
            icDifference = icDifference * 0.7
        else:
            icDifference = abs(icDifference)

        icDifferences[i-1] = icDifference

        i += 1

    # Retorna índice do menor valor (acrescido de 1 para compensar que nao há item 0)
    return icDifferences.index(min(icDifferences)) + 1

def splitTextByKeySize(text, keySize):
    separatedTexts = [None] * keySize
    for i in range(0, keySize):
        newText = ""
        for j in range(i, len(text), keySize):
            newText += text[j]
        separatedTexts[i] = newText
    return separatedTexts

def dislocateCharacter(character, jumpSize):
    newLetter=chr(ord(character)+jumpSize)
    if(newLetter > chr(ord('Z'))):
        newLetter = chr(ord(newLetter)-26)
    return newLetter

def dislocateCharacters(text, jumpSize):
    newText = ""
    for l in text:
        newText += dislocateCharacter(l, jumpSize)
    return newText

def findKey(text, keySize, mostCommon):
    key = [None] * keySize
    splitTexts = splitTextByKeySize(text, keySize)
    mostCommonCharLang = mostCommon[0]
    
    for i in range(0, keySize):
        print("--- Finding Key at position: " + str(i))
        for j in range (0, 26):
            mostCommonCharText = collections.Counter(dislocateCharacters(splitTexts[i], j)).most_common(1)[0][0]
            if(mostCommonCharText == mostCommonCharLang):
                key[i] = j
                print(key)
                break

    return key

def decipherText(text, key):
    keySize = len(key)
    textSize = len(text)
    decipheredText = ""

    i = 0
    for l in text:
        decipheredText += dislocateCharacter(l, key[i])
        
        if(i>=keySize-1):
            i = 0
        else:
            i += 1
    
    return decipheredText



    

if __name__ == "__main__":
    text = readAndFormatText()
    print("--- Calculating Key Size (IC for each increment size) ---")

    keySize = findKeySize(text, AVERAGE_IC_EN)
    print("--- Probable Key Size: {}".format(keySize))

    key = findKey(text, keySize, MOST_FREQUENT_EN)
    # key = findKey(text, 8, MOST_FREQUENT_EN)

    decipheredText = decipherText(text, key)
    print(decipheredText)

# 11, 22, 4, 24