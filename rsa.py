import secrets
import random

"""A função recebe o número a ser testado como primo
e o número de testes a ser feito em cima dele
"""
def miller_rabin(number, k):
    if k > number - 3: #garante que eu nâo vá tentar rodar a função com um k impossível (k tem que ser menor que a função totiente de number, pensando q number é primo)
        k = number - 3

    s = 0
    m = number - 1  #s e m vem da forma de escrever um número par (2^s)*m. para saber mais, veja o tcc do daniel chaves de lima
    tuple = divmod(m, 2) #faz uma dupla, onde o primeiro é o resultado e o segundo é o resto, usamos pq % para mod não dá conta de números grandes.
    while tuple[1] == 0: #enquanto m mod 2 for 0, ele divide por 2 para descobrir o expoente 's' e o número ímpar 'm'
        m = tuple[0] #atualiza m
        tuple = divmod(m, 2) #atualiza a tupla
        s += 1

    # no while anterior descobrimos o m ímpar que queremos, como m vai ser um expoente que faria o cálculo do mod ser enorme
    # convertemos ele para a base binária, portanto r é a lista de restos de m, necessário para fazer essa converssão
    r = []
    while m > 0:
        tuple = divmod(m, 2)
        m = tuple[0]
        r.append(tuple[1])

    coprime_list = []
    length = len(coprime_list)
    while length < k:
        randomic_number = random.randrange(2, number-1) #imaginando number primo, pega um dos p-1 numeros coprimos com number, é disso que ocorre o 1/4 de falha (pseudo primo)
        if randomic_number not in coprime_list:
            coprime_list.append(randomic_number)
            length = len(coprime_list)

    for coprime in coprime_list:
        e = coprime
        y = e #otimização do daniel, pois m é sempre ímpar e esse primeiro coprimo vai ser sempre elevado a 1
        for exponent in r[1:]: #otimização do cálculo de resto de uma potência muito grande
            e = (e ** 2) % number
            if exponent == 1:
                y = (y * e) % number
        if y != 1 and y != number-1:
            i = 1
            while i <= s - 1 and y != number-1:
                y = (y ** 2) % number
                if y == 1:
                    return False
                i += 1
            if y != number - 1:
                return False
    
    return True

def prime_generator(bits):
    is_not_prime = True
    while is_not_prime:
        prime = odd_number_generator_with_k_bits(bits)
        if(miller_rabin(prime, 40)):
            is_not_prime = False
    return prime

"""A função retorna um número k de bits aleatórios.
exemplo: k = 5
00001
mas o python na hora de exibir vai mostrar o seguinte
print(bin(number_generator(6))
output:
0b1
ou seja, o seu número, na prática, tem apenas um bit, ele foi otimizado para ignorar os bits 0 a esquerda
para impedir isso, force o bit mais significativo a ser 1
basta fazer um or com 1-(k_bits de zeros - 1)
assim garantimos que o número terá a quantidade de bits desejada
"""
def odd_number_generator_with_k_bits(k_bits):
    odd = False
    while not odd:
        number = secrets.randbits(k_bits)
        number = number | (1 << k_bits - 1) # shifta o 1 e joga zeros atrás, suponha k_bits = 3, entao teremos 100 como resultado (comentário sobre os parênteses).
        and_result = number & 1 #se o bit menos significativo for 1, esse and bitwise vai dar 1, o que significa que o número sorteado é ímpar
        if (and_result == 1):
            odd = True
    return number

""" retorna o par de chaves pública e privada
"""
def rsa_keys():

    p = prime_generator(1024)
    q = prime_generator(1024)
    n = p*q
    phi_n = (p-1)*(q-1) # função totiente de euler
    e = 65537 # número primo com peso de hamming baixo
    d = pow(e, -1, phi_n) # calcula o inteiro que é o inverso multiplicativo de e, tal que ed mod phi_n = 1

    return (n, e), (n, d)

if __name__ == "__main__":
    number = odd_number_generator_with_k_bits(5) #lembrar de chamar na main com 1024 bits. estou usando 5 bits apenas de teste
    print("result: ", number)
    print(bin(number))
    primo = miller_rabin(997, 40)
    print("é primo: ", primo)
    prime = prime_generator(1024)
    print("primo gigante: ", prime)
    chaves = rsa_keys()
    print("publica: ", chaves[0])
    print("privada: ", chaves[1])
