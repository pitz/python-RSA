import random
import math 
import time
from datetime import datetime

def getRandomPrimeNumber():
    randomicNumber = random.randrange(10, 1000)

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

    for factor in range(2, n + 1):          
        while n % factor == 0:
            n = n / factor
            factors.append(factor)
    return factors


def factorByPollardsRho(n):
    x = 2
    y = 2
    d = 1
    f = lambda x: (x**2 + 1) % n

    while d == 1:
        x = f(x)
        y = f(f(y))
        d = math.gcd(abs(x-y), n)

    if d != n: 
        return [d, n // d]


def factorBreakingRSA(publicKey, encryptedMessage):
    initialTime = datetime.now()

    n, e     = publicKey
    nFactor  = factor(n)
    nTotient = (nFactor[0] - 1) * (nFactor[1] - 1) 
    dBroken  = multiplicativeInverse(e, nTotient)

    decryptedMessage = decryptMessage(encryptedMessage, n, dBroken)
    finalTime = datetime.now()

    print("[..] Tempo para fatoração utilizando factorBreakingRSA(): ", finalTime-initialTime)

    return decryptedMessage
    

def factorByPollardsRhoBreakingRSA(publicKey, encryptedMessage):
    initialTime = datetime.now()

    n, e     = publicKey
    nFactor  = factorByPollardsRho(n)
    nTotient = (nFactor[0] - 1) * (nFactor[1] - 1) 
    dBroken  = multiplicativeInverse(e, nTotient)

    decryptedMessage = decryptMessage(encryptedMessage, n, dBroken)
    finalTime = datetime.now()
    
    print("[..] Tempo para fatoração utilizando factorByPollardsRhoBreakingRSA(): ", finalTime-initialTime)
    
    return decryptedMessage


def rsaBrokenTest(publicKey, encryptedMessage, decryptedMessage):
    brokenRsaDecryptedMessageA = factorBreakingRSA(publicKey, encryptedMessage)
    brokenRsaDecryptedMessageB = factorByPollardsRhoBreakingRSA(publicKey, encryptedMessage)

    if (brokenRsaDecryptedMessageA == decryptedMessage):
        print('[..] O método factorBreakingRSA() se mostrou eficaz como algoritmo de força bruta para descriptografar a mensagem.')

    if (brokenRsaDecryptedMessageB == decryptedMessage):
        print('[..] O método factorByPollardsRhoBreakingRSA() se mostrou eficaz como algoritmo de força bruta para descriptografar a mensagem.')


def rsaTest(message):
    firstPrimeNumber     = getRandomPrimeNumber()
    secondaryPrimeNumber = getRandomPrimeNumber()

    n         = (firstPrimeNumber * secondaryPrimeNumber)
    nTotient  = (firstPrimeNumber - 1) * (secondaryPrimeNumber - 1) 
    e         = calculateE(nTotient)
    publicKey = (n, e)
    d         = multiplicativeInverse(e, nTotient)

    encryptedMessage = encryptMessage(message, publicKey)
    decryptedMessage = decryptMessage(encryptedMessage, n, d)

    rsaBrokenTest(publicKey, encryptedMessage, decryptedMessage)


if __name__=='__main__':
    print('.')
    print('.')
    print('.')

    message = input("Informe aqui a sua mensagem: ")
    rsaTest(message)