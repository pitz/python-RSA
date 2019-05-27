import random


def getRandomPrimeNumber():
    randomicNumber = random.randrange(10, 10000)

    if (isPrime(randomicNumber)):
        return randomicNumber
    
    while True:
        randomicNumber = randomicNumber + 1
        
        if (isPrime(randomicNumber)):
            return randomicNumber

def isPrime(n):
    if (n == 2):
        return True
	
    if (not n & 1):
        return False

    return pow(2, n-1, n) == 1


# Devemos escolher um número e em que 1 < e < φ(n), de forma que e seja co-primo de φ(n)
def calculateE(nTotient):
    while True:
        e = random.randrange(2, (nTotient - 1))
        if (mdc(nTotient, e) == 1):
            return e


def mdc(n1, n2):
    if (n2 <= 1):
        return -1

    while (n2 != 0):
        rest = n1 % n2
        n1   = n2
        n2   = rest

    return n1


def encryptMessage(message, publicKey):
    n, e = publicKey

    messageLenght = len(message)
    
    count = 0
    encryptedMessage = []
    
    while(count < messageLenght):
        letter = message[count]
        numericLetter = ord(letter)

        encryptedLetter = pow(numericLetter, e, n)
        encryptedMessage.append(encryptedLetter)

        count += 1

    return encryptedMessage


def decryptMessage(message, n, privateKey):
    messageLenght = len(message)

    count = 0
    decryptedMessage = ''

    while(count < messageLenght):
        decryptedNumber = pow(message[count], privateKey, n)
        decryptedChar   = (chr(decryptedNumber))
        decryptedMessage += decryptedChar

        count += 1

    return decryptedMessage

# A multiplicação de um número pelo seu inverso multiplicativo tem como resultado a identidade multiplicativa do conjunto. Nos conjuntos que estamos estudando esta identidade é sempre 1.
# https://www.lambda3.com.br/2013/01/entendendo-de-verdade-a-criptografia-rsa-parte-iii/

def multiplicativeInverse(e, nTotient):
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a

    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x  = 0
    y  = 1
    previusX = 1
    previusY = 0
    
    previusE = e
    previusNTotient = nTotient  
    
    while (nTotient != 0):
        intDivision = (e // nTotient)

        eAux = e
        e = nTotient
        nTotient = eAux % nTotient

        auxX = x
        x = (previusX - (intDivision * x))
        previusX = auxX

        auxY = y
        y = (previusY - (intDivision * y))
        previusY = auxY

    if (previusX < 0):
        previusX += previusNTotient

    if (previusY < 0):
        previusY += previusE

    return previusX

def factor(n):
    factors = []

    if (n == 1):
        return 1
    else:    
        for factor in range(2, n + 1):          
            while n % factor == 0:
                n = n / factor
                factors.append(factor)
        return factors

    print("Não encontrado.")
    return -1

def breakRSA(publicKey, encryptedMessage):
    print("Quebrando a chave privada.")

    n, e    = publicKey
    nFactor = factor(n)

    print('nFactor', nFactor)
    
    nTotient   = (nFactor[0] - 1) * (nFactor[1] - 1) 
    privateKey = multiplicativeInverse(e, nTotient)
    
    print("Descriptografando mensagem com Força Bruta:")
    print(decryptMessage(encryptedMessage, n, privateKey))

def rsaTest(message):
    firstPrimeNumber     = getRandomPrimeNumber()
    secondaryPrimeNumber = getRandomPrimeNumber()

    print('firstPrimeNumber: ',     firstPrimeNumber) 
    print('secondaryPrimeNumber: ', secondaryPrimeNumber) 

    n        = (firstPrimeNumber * secondaryPrimeNumber)
    nTotient = (firstPrimeNumber - 1) * (secondaryPrimeNumber - 1) 
    e        = calculateE(nTotient)
    publicKey = (n, e)
    d = multiplicativeInverse(e, nTotient)

    encryptedMessage = encryptMessage(message, publicKey)
    decryptedMessage = decryptMessage(encryptedMessage, n, d)

    if (message != decryptedMessage):
        print('Erro ao descriptografar a mensagem.')
    
    breakRSA(publicKey, encryptedMessage)
    


if __name__=='__main__':
    print('Iniciando testes...')
    
    rsaTest("Eduardo Pitz")

    # print('2')
    # rsaTest("Eduardo Pitz")

    # print('3')
    # rsaTest("Eduardo Alberto")

    # print('4')
    # rsaTest("Raquel")

    # print('5')
    # rsaTest("Raquel Agostini")    

    print('Final dos testes.')