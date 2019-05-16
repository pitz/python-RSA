import random


def getRandomPrimeNumber():
    randomicNumber = random.randrange(100, 1000)

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
    while True:
        e = random.randrange(2, nTotient)

        if (mdc(nTotient, e) == 1):
            return e


def mdc(n1, n2):
    rest = 1

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


def buildPrivateKey(nTotient, e):
    d = 0

    while(((d * e) % nTotient) != 1):
        d += 1

    return d


def extendMdc(a, b):
    if (b <= 0):
        return [1, 0, a]
    else:
        x, y, d = extendMdc(b, a % b)
        return [y, x - (a // b) * y, d]


if __name__=='__main__':
    firstPrimeNumber     = getRandomPrimeNumber()
    secondaryPrimeNumber = getRandomPrimeNumber()

    n        = (firstPrimeNumber * secondaryPrimeNumber)
    nTotient = (firstPrimeNumber - 1) * (secondaryPrimeNumber - 1) 
    e        = calculateE(nTotient)
    publicKey = (n, e)

    print('A sua chave pública é:', publicKey)

    message = input("Informe aqui a sua mensagem: ")
    encryptedMessage = encryptMessage(message, publicKey)

    print('Mensagem Criptografada:', encryptedMessage)
    
    privateKey = buildPrivateKey(nTotient, e)
    print('Chave Privada: ', privateKey)

    # x, y, d = extendMdc(nTotient, e)
    # print('Chave privada com MDC Estendido: ', y)
    
    x, y, d = extendMdc(nTotient, e)
    print('Chave privada com MDC Estendido: ', y)

    print('Chave Privada 2 : ', x)
    print('Chave Privada 2 : ', y)
    print('Chave Privada 2 : ', d)

    decryptedMessage = decryptMessage(encryptedMessage, n, privateKey)
    print('Mensagem Descriptografada:',  decryptedMessage)

    if (y > 0):
        decryptedMessage2 = decryptMessage(encryptedMessage, n, y)
        print('Mensagem Descriptografada2:', decryptedMessage2)