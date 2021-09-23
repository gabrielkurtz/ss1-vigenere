import os
import collections

# Variaveis Globais Configuraveis
# Path do arquivo de texto
FILE_PATH = os.getcwd() + '/enunciado/Cifrados/cipher1.txt'

# Lingua - "EN"/"PT". Default: "EN"
LANGUAGE = "EN"

# Tamanho maximo de chave para procurar antes de utilizar o valor mais proximo
MAX_KEY_SIZE = 30

# Diferenca entre IC do texto e média da lingua
# ACCEPTABLE_DIFFERENCE = 0.015
ACCEPTABLE_DIFFERENCE = 0.000


# Variaveis Globais Fixas
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
        print("{} - {}".format(i, "%.3f" % ic[i]))

    averageIc = sum(ic) / len(ic)
    return averageIc

def findKeySize(text, averageIc):
    icDifferences = [None] * (MAX_KEY_SIZE - 1)
    i = 1
    while(i < MAX_KEY_SIZE):
        ic = calculateIcWithJump(text, i)
        
        print("{} - {}".format(i, "%.3f" % ic))
        
        icDifference = abs(ic - averageIc)
        if(icDifference < ACCEPTABLE_DIFFERENCE):
             return i

        icDifferences[i-1] = icDifference

        i += 1

    # Retorna índice do menor valor (acrescido de 1 para compensar que nao há item 0)
    return icDifferences.index(min(icDifferences)) + 1


if __name__ == "__main__":
    text = readAndFormatText()
    ic = calculateIc(text)
    printFormattedIc(ic)
    print(findKeySize(text, AVERAGE_IC_EN))
