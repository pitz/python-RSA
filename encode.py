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

def multiplicative_inverse(a, b):
    """Returns a tuple (r, i, j) such that r = gcd(a, b) = ia + jb
    """
    # r = gcd(a,b) i = multiplicitive inverse of a mod b
    #      or      j = multiplicitive inverse of b mod a
    # Neg return values for i or j are made positive mod b or a respectively
    # Iterateive Version is faster and uses much less stack space
    x = 0
    y = 1
    lx = 1
    ly = 0
    oa = a  # Remember original a/b to remove
    ob = b  # negative values from return results
    while b != 0:
        q = a // b
        (a, b) = (b, a % b)
        (x, lx) = ((lx - (q * x)), x)
        (y, ly) = ((ly - (q * y)), y)
    if lx < 0:
        lx += ob  # If neg wrap modulo orignal b
    if ly < 0:
        ly += oa  # If neg wrap modulo orignal a
    # return a , lx, ly  # Return only positive values
    return lx

def encrypt(key, n, plaintext):
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    #Return the array of bytes
    return cipher

def decrypt(e, n, ciphertext):
    #Unpack the key into its components

    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char ** e) % n) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)

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

    print('Mensagem Criptografada 1:', encryptedMessage)

    d = multiplicative_inverse(e, nTotient)
    print('Chave Privada (Nova): ', d)
    
    # teste2 = encrypt(d, n, message)
    # print('Mensagem Criptografada 2:', encryptedMessage)
    # print(teste2)

    # teste3 = decrypt(e, n, encryptedMessage)
    # print('Decrypt')
    # print(teste3)
    
    print('---------------------------------------')

    privateKey = buildPrivateKey(nTotient, e)
    print('Chave Privada (Ruim): ', privateKey)
    
    decryptedMessage = decryptMessage(encryptedMessage, n, d)
    print('Mensagem Descriptografada (Com chave nova):',  decryptedMessage)

    # x, y, d = extendMdc(nTotient, e)
    # print('Chave privada com MDC Estendido: ', y)
    
    # x, y, d = extendMdc(nTotient, e)
    # print('Chave privada com MDC Estendido: ', y)

    # print('Chave Privada 2 : ', x)
    # print('Chave Privada 2 : ', y)
    # print('Chave Privada 2 : ', d)

    

    # if (y > 0):
    #     decryptedMessage2 = decryptMessage(encryptedMessage, n, y)
    #     print('Mensagem Descriptografada2:', decryptedMessage2)

    #     if (decryptedMessage != decryptedMessage2):
    #         print('Erro ao descriptografar mensagem.')

