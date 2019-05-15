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


def xmdc(a, b):
    if b == 0:
        return [1,0,a]
    else:
        x, y, d = xmdc(b, a%b)
        return [y, x - (a//b) * y, d]

def findPrivateKey(a, b):
    r  = a
    r1 = b
    u  = 1
    v  = 0
    u1 = 0
    v1 = 1

    # rs = 0
    # us = 0
    # vs = 0
    # q  = 0

    while (r1 != 0):
        q = r // r1
        rs = r
        us = u
        vs = v
        r = r1
        u = u1
        v = v1
        r1 = rs - q * r1
        u1 = us - q * u 
        v1 = vs - q * v1

    print('>>>>') # a = n

    print(r)
    print(v)
    print(u)

    return r


# def mdcExtended(n1, n2, n3):

#     13 : 640 = 0 com resto 13
#     n1 : n2 = int resultado resto 13

    
#     resto = (1 * n1) - (dividendo * n2)

#     3 = (1 * 640) - (49 * 13)
#     resto = (1 * n1) - (dividendo * n2)


#     n2 = (1 * n1) - (dividendo * n2)



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

    n        = (firstPrimeNumber * secondaryPrimeNumber)
    nTotient = (firstPrimeNumber - 1) * (secondaryPrimeNumber - 1) 

    e = calculateE(nTotient)

    publicKey = (n, e) 

    print('Chave Pública:', publicKey)
    encryptedMessage = encryptMessage(message, e, n)

    

    print('Mensagem Criptografada:', encryptedMessage)
    
    # privateKey
    privateKey = buildPrivateKey(nTotient, e)
    privateKey2 = findPrivateKey(n, e)

    x, y, d = xmdc(n, e)

    print('Chave Privada 1   : ', privateKey)
    print('Chave Privada 2 x : ', x)
    print('Chave Privada 2 y : ', y)
    print('Chave Privada 2 d : ', d)

    # print('Chave Privada 2 : ', privateKey2)

    decryptedMessage = decryptMessage(encryptedMessage, n, privateKey)
    print('Mensagem Descriptografada:', decryptedMessage)

    decryptedMessage = decryptMessage(encryptedMessage, n, x)
    print('Mensagem Descriptografada:', decryptedMessage)