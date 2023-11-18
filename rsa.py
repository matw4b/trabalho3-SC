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
    while m%2 == 0: #enquanto m mod 2 for 0, ele divide por 2 para descobrir o expoente 's' e o número ímpar 'm'
        m = m/2     #atualiza m
        s += 1

    r = []
    while m > 0:
        r.append(m % 2)
        m = (m - (m % 2))/2

    bases = []
    length = len(bases)
    while length < k:
        randomic_number = random.randrange(2, number-1) #imaginando number primo, pega um dos p-1 numeros coprimos com number, é disso que ocorre o 1/4 de falha (pseudo primo)
        if randomic_number not in bases:
            bases.append(randomic_number)
            length = len(bases)

    for b in bases:
        e = b
        y = b #otimização do daniel, pois m é sempre ímpar e esse primeiro b vai ser sempre elevado a 1
        for expoente in r[1:]: #otimização do cálculo de resto de uma potência muito grande
            e = (e ** 2) % number
            if expoente == 1:
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
    print("retorno true: ", True)
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
        print("odd function: ", number) #print que testa o número sorteado
        print(bin(number))
        number = number | (1 << k_bits - 1) # shifta o 1 e joga zeros atrás, suponha k_bits = 3, entao teremos 100 como resultado (comentário sobre os parênteses).
        and_result = number & 1 #se o bit menos significativo for 1, esse and bitwise vai dar 1, o que significa que o número sorteado é ímpar
        print("after 'or' in odd function: ", number) #testa se o número tem a quantidade de bits desejada
        print(bin(number))
        print("'bitwise and' result: ", and_result) #mostra o resultado do and bitwise
        if (and_result == 1):
            odd = True
    return number

if __name__ == "__main__":
    number = odd_number_generator_with_k_bits(5) #lembrar de chamar na main com 1024 bits. estou usando 5 bits apenas de teste
    print("result: ", number)
    print(bin(number))
    primo = miller_rabin(997, 40)
    print("é primo: ", primo)
    prime = prime_generator(1024)
    print("primo gigante: ", prime)