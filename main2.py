import random
import math
import sys
import time


##
# Retorna uma matriz de zeros com a dimensão especificada nos parâmetros
##
def generate_parity_matrix(num_linhas, num_colunas):
    return [[0 for coluna in range(num_colunas)] for linha in range(num_linhas)]

##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##
def code_packet(originalPacket, num_linhas, num_colunas):
    parity_matrix = generate_parity_matrix(num_linhas, num_colunas)
    codedLen = math.ceil( len(originalPacket) / (num_linhas * num_colunas) ) * (num_linhas * num_colunas + num_linhas + num_colunas)

    if not codedLen:
        raise SystemExit(1)

    codedPacket = [0 for indice in range(codedLen)]

    ##
    # Itera por cada bloco do pacote original. O bloco possui o tamanho
    # da quantidade de bits do pacote que cabem na matriz de paridade.
    ##
    for block in range(len(originalPacket) // (num_linhas * num_colunas)):

        ##
        # Bits do i-esimo bloco sao dispostos na matriz.
        ##
        for lin in range(num_linhas):
            for col in range(num_colunas):
                parity_matrix[lin][col] = originalPacket[block * (num_linhas * num_colunas) + num_colunas * lin + col]

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##
        for mat_index in range(num_linhas * num_colunas):
            codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + mat_index] = originalPacket[block * (num_linhas * num_colunas) + mat_index]

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##
        for col in range(num_colunas):
            sub_total = 0
            for lin in range(num_linhas):
                sub_total += parity_matrix[lin][col]

            if sub_total % 2 == 0:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + num_linhas * num_colunas + col] = 0
            else:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + num_linhas * num_colunas + col] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##
        for lin in range(num_linhas):
            sub_total = 0
            for col in range(num_colunas):
                sub_total += parity_matrix[lin][col]

            if sub_total % 2 == 0:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + (num_linhas * num_colunas + num_colunas) + lin] = 0
            else:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + (num_linhas * num_colunas + num_colunas) + lin] = 1

    return codedPacket

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decode_packet(transmittedPacket, num_linhas, num_colunas):
    parityMatrix = generate_parity_matrix(num_linhas, num_colunas)
    parityColumns = [0 for coluna in range(num_colunas)]
    parityRows = [0 for linha in range(num_linhas)]
    decodedPacket = [0 for i in range(len(transmittedPacket))]

    block_index = 0 # Contador de blocos no pacote decodificado.

    ##
    # Itera por cada sequencia de bits de dados + bits de paridade.
    ##
    for block_offset in range(0, len(transmittedPacket), (num_linhas * num_colunas + num_linhas + num_colunas)):

        ##
        # Bits do i-esimo conjunto sao dispostos na matriz.
        ##
        for lin in range(num_linhas):
            for col in range(num_colunas):
                parityMatrix[lin][col] = transmittedPacket[block_offset + num_colunas * lin + col]

        ##
        # Bits de paridade das colunas.
        ##
        for col in range(num_colunas):
            parityColumns[col] = transmittedPacket[block_offset + (num_linhas * num_colunas) + col]

        ##
        # Bits de paridade das linhas.
        ##
        for lin in range(num_linhas):
            parityRows[lin] = transmittedPacket[block_offset + (num_linhas * num_colunas + num_colunas) + lin]

        ##
        # Verificacao dos bits de paridade: colunas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInColumn = -1
        for col in range(num_colunas):
            sub_total = 0
            for lin in range(num_linhas):
                sub_total += parityMatrix[lin][col]

            if sub_total % 2 != parityColumns[col]:
                errorInColumn = col
                break

        ##
        # Verificacao dos bits de paridade: linhas.
        # Note que paramos no primeiro erro, ja que se houver mais
        # erros, o metodo eh incapaz de corrigi-los de qualquer
        # forma.
        ##
        errorInRow = -1
        for lin in range(num_linhas):
            sub_total = 0
            for col in range(num_colunas):
                sub_total += parityMatrix[lin][col]

            if sub_total % 2 != parityRows[lin]:
                errorInRow = lin
                break

        ##
        # Se algum erro foi encontrado, corrigir.
        ##
        if errorInRow > -1 and errorInColumn > -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        ##
        # Colocar bits (possivelmente corrigidos) na saida.
        ##
        for lin in range(num_linhas):
            for col in range(num_colunas):
                decodedPacket[(num_linhas * num_colunas) * block_index + num_colunas * lin + col] = parityMatrix[lin][col]

        ##
        # Incrementar numero de bytes na saida.
        ##
        block_index = block_index + 1

    return decodedPacket

###
##
# Outras funcoes.
##
###

##
# Gera conteudo aleatorio no pacote passado como
# parametro. Pacote eh representado por um vetor
# em que cada posicao representa um bit.
# Comprimento do pacote (em bytes) deve ser
# especificado.
##
def generateRandomPacket(length):

    return [random.randint(0,1) for x in range(8 * length)]

##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):

    uRand = 0
    while(uRand == 0):
        uRand = random.uniform(0, 1)

    return int(math.log(uRand) / math.log(1 - p))

##
# Insere erros aleatorios no pacote, gerando uma nova versao.
# Cada bit tem seu erro alterado com probabilidade errorProb,
# e de forma independente dos demais bits.
# Retorna o numero de erros inseridos no pacote e o pacote com erros.
##
def insertErrors(codedPacket, errorProb):
    
    i = -1
    n = 0 # Numero de erros inseridos no pacote.

    ##
    # Copia o conteudo do pacote codificado para o novo pacote.
    ##
    transmittedPacket = list(codedPacket)

    while True:

        ##
        # Sorteia a proxima posicao em que um erro sera inserido.
        ##
        r = geomRand(errorProb)
        i = i + 1 + r

        if i >= len(transmittedPacket):
            break

        ##
        # Altera o valor do bit.
        ##
        if transmittedPacket[i] == 1:
            transmittedPacket[i] = 0
        else:
            transmittedPacket[i] = 1

        n = n + 1

    return n, transmittedPacket

##
# Conta o numero de bits errados no pacote
# decodificado usando como referencia
# o pacote original. O parametro packetLength especifica o
# tamanho dos dois pacotes em bytes.
##
def count_errors(originalPacket, decodedPacket):

    errors = 0

    for i in range(len(originalPacket)):
        if originalPacket[i] != decodedPacket[i]:
            errors = errors + 1

    return errors

##
# Exibe modo de uso e aborta execucao.
##
def help(selfName):
    sys.stderr.write("Simulador de metodos de FEC/codificacao.\n\n")
    sys.stderr.write("Modo de uso:\n\n")
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro> <n. lin> <n. col>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("\tde que um dado bit tenha seu valor alterado pelo canal.)\n")
    sys.stderr.write("\t- <n. lin>: número de linhas da matriz de paridade\n")
    sys.stderr.write("\t- <n. col>: número de colunas da matriz de paridade\n\n")

    sys.exit(1)

##
# Programa principal:
#  - le parametros de entrada;
#  - gera pacote aleatorio;
#  - gera bits de redundancia do pacote
#  - executa o numero pedido de simulacoes:
#      + Introduz erro
#  - imprime estatisticas.
##


##
# Inicializacao de contadores.
##
totalBitErrorCount = 0
totalPacketErrorCount = 0
totalInsertedErrorCount = 0

##
# Leitura dos argumentos de linha de comando.
##
# if len(sys.argv) != 6:
#     help(sys.argv[0])

packet_length = int(sys.argv[1])
reps = int(sys.argv[2])
errorProb = float(sys.argv[3])

if packet_length <= 0 or reps <= 0 or errorProb < 0 or errorProb > 1:
    help(sys.argv[0])

##
# Inicializacao da semente do gerador de numeros
# pseudo-aleatorios.
##
random.seed()

##
# Geracao do pacote original aleatorio.
##

num_linhas = int(sys.argv[4])
num_colunas = int(sys.argv[5])

originalPacket = generateRandomPacket(packet_length)
codedPacket = code_packet(originalPacket, num_linhas, num_colunas)

print(codedPacket)

