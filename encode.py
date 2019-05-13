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

    while True:
        # Essa lógica precisa melhorar. (todo)
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


def encryptMessage(message, e, n):
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


# def mdcExtended(n1, n2, n3):
#     rest = 1

#     while (n2 != 0):
#         rest = n1 % n2
#         n1   = n2
#         n2   = rest
#     return n1

    
#     #   n1 divide por n2
#     #   c = um número que corresponde a função
#     #
#     #   r = (1 * x) - (c * y)


#     int c = n1 / n2
#     resto = (1 * n1) - (c * n2)

#     r = b % a

#     if (r == 0):
#         return (c / a) % (b / a)

#     return ((mdcExtended(r, a, -c) * b + c) / (a % b))



# def buildPrivateKeyL3(nTotient, e):
#     d = 0

#     divisor = nTotient
    
#     resto = mdc(e, nTotient)

#     while(((d * e) % nTotient) != 1):
#         d += 1

#     return d


if __name__=='__main__':
    message = input("Informe aqui a sua mensagem: ")

    firstPrimeNumber = getRandomPrimeNumber()
    secondaryPrimeNumber = getRandomPrimeNumber()

    n = firstPrimeNumber*secondaryPrimeNumber
    nTotient = (firstPrimeNumber - 1) * (secondaryPrimeNumber - 1) 

    e = calculateE(nTotient)

    publicKey = (n, e) 

    print('Chave Pública:', publicKey)
    encryptedMessage = encryptMessage(message, e, n)

    print('Mensagem Criptografada:', encryptedMessage)
    privateKey = buildPrivateKey(nTotient, e)

    decryptedMessage = decryptMessage(encryptedMessage, n, privateKey)
    print('Mensagem Descriptografada:', decryptedMessage)