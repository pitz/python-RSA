import random

def getRandomPrimeNumber():
    randomicNumber = random.randrange(1, 100)

    if (isPrime(randomicNumber)):
        return randomicNumber

    return getRandomPrimeNumber()

def isPrime(n):
    if (n == 2):
        return True
	
    if (not n & 1):
        return False

    return pow(2, n-1, n) == 1

# Devemos escolher um número e em que 1 < e < φ(n), de forma que e seja co-primo de φ(n)
def calculateE(nTotient):

    def mdc(n1, n2):
        rest = 1

        while (n2 != 0):
            rest = n1%n2
            n1   = n2
            n2   = rest
        return n1

    while True:
        # Essa lógica precisa melhorar. (todo)
        e = random.randrange(2, nTotient)

        if (mdc(nTotient, e) == 1):
            return e

       
'''
Cifra um texto
'''
def encryptMessage(message, e, n): # get the words and compute the encrypt
    messageLenght = len(message)
    
    count = 0
    encryptList = []
    
    while(count < messageLenght):
        letter = message[count]
        numericLetter = ord(letter)              # integer representing Unicode code

        encryptedLetter = (numericLetter ** e % n)
        encryptList.append(encryptedLetter)

        count += 1

    return encryptList

'''
Descriptografa um texto criptografado
'''
def decryptMessage(cifra,n,d):
    lista=[]
    i=0
    tamanho=len(cifra)
    # texto=cifra ^ d mod n
    while i<tamanho:
        result=cifra[i]**d
        texto= result % n
        letra=chr(texto)
        lista.append(letra)
        i=i+1
    return lista


'''
Calcula a chave privada
'''
def buildPrivateKey(toti,e):
    d = 0

    while(((d*e) % toti) != 1):
        d += 1

    return d

## MAIN
if __name__=='__main__':
    message = input("Informe aqui a sua mensagem: ")

    # Buscando números primos.
    firstPrimeNumber = getRandomPrimeNumber()
    secondaryPrimeNumber = getRandomPrimeNumber()

    # Calculando N. // Chave para codificar.
    n = firstPrimeNumber*secondaryPrimeNumber
    
    # compute the totient of N # totient = primo - 1
    nTotient = (firstPrimeNumber - 1) * (secondaryPrimeNumber - 1) 

    # e para Chave
    e = calculateE(nTotient)

    # Chave de codificação
    publicKey = (n, e) 

    # Calcular Chave Pública
    print('Chave Pública:', publicKey)
    encryptedMessage = encryptMessage(message, e, n)

    # Criptografa
    print('Mensagem Criptografada:', encryptedMessage)
    privateKey = buildPrivateKey(nTotient, e)

    # Descriptografa
    decryptedMessage = decryptMessage(encryptedMessage, n, privateKey)
    print('Mensagem Descriptografada:', decryptedMessage)