import random
import math
    
'''
Verifica se um numero gerado é primo
'''
def prime(n):
    if (n == 2):
        return True
	
    if (not n & 1):
        return False

    return pow(2, n-1, n) == 1

## Número aleatório para codificar.
'''
Gera um numero aleatório E, sasfazendo as condições
Devemos escolher um número e em que 1 < e < φ(n), de forma que e seja co-primo de φ(n). Em outras palavras, queremos um e onde o MDC(φ(n), e) = 1, sendo e > 1.

REFATORAR.
'''
def calculateE(num): # recives totient of N as a parameter
    
    def mdc(n1, n2): # compute the mdc of the totient of N and E
        rest = 1

        while(n2 != 0):
            rest = n1%n2
            n1   = n2
            n2   = rest
        return n1

    while True:
        # define the range of the E 
        e = random.randrange(2, num) # Inicio no 2 e para no num

        if (mdc(num, e) == 1):
            return e

'''
Gera um numero primo aleatório
'''
def getRandomPrimeNumber():
    while True:
        x = random.randrange(1, 100)

        if(prime(x)==True):
            return x

'''
Função modular entre dois números
'''
def mod(a,b): # mod function
    if(a<b):
        return a
    else:
        c=a%b
        return c
       
'''
Cifra um texto
'''
def encryptMessage(message, e, n): # get the words and compute the encrypt
    messageLenght = len(message)
    i = 0
    lista = []
    
    while(i < messageLenght):
        letter = message[i]

        k = ord(letter)      # integer representing Unicode code
        k = k**e
        d = mod(k, n)

        lista.append(d)
        
        i = i+1
    return lista

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
        texto=mod(result,n)
        letra=chr(texto)
        lista.append(letra)
        i=i+1
    return lista


'''
Calcula a chave privada
'''
def buildPrivateKey(toti,e):
    d=0
    while(mod(d*e,toti)!=1):
        d += 1
    return d


## MAIN
if __name__=='__main__':
    message = input("Informe aqui a sua mensagem: ")

    # Buscando números primos.
    firstPrimeNumber = getRandomPrimeNumber()
    secondaryPrimeNumber = getRandomPrimeNumber()

    # Calculando N.
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