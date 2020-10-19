import random
import math
import sys
import time
import os
import pandas as pd


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
    codedLen = math.ceil(len(originalPacket) / (num_linhas * num_colunas)) * (
                num_linhas * num_colunas + num_linhas + num_colunas)

    if not codedLen:
        raise SystemExit(1)

    codedPacket = [0 for indice in range(codedLen)]

    ##
    # Itera por cada bloco do pacote original. O bloco possui o tamanho
    # da quantidade de bits do pacote que cabem na matriz de paridade.
    ##
    for block in range(math.ceil(len(originalPacket) / (num_linhas * num_colunas))):

        ##
        # Bits do i-esimo bloco sao dispostos na matriz.
        ##
        for lin in range(num_linhas):
            for col in range(num_colunas):
                try:
                    parity_matrix[lin][col] = originalPacket[
                        block * (num_linhas * num_colunas) + num_colunas * lin + col]
                except:
                    parity_matrix[lin][col] = 0

        ##
        # Replicacao dos bits de dados no pacote codificado.
        ##
        for mat_index in range(num_linhas * num_colunas):
            try:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + mat_index] = originalPacket[
                    block * (num_linhas * num_colunas) + mat_index]
            except:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + mat_index] = 0

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das colunas.
        ##
        for col in range(num_colunas):
            sub_total = 0
            for lin in range(num_linhas):
                sub_total += parity_matrix[lin][col]

            if sub_total % 2 == 0:
                codedPacket[
                    block * (num_linhas * num_colunas + num_linhas + num_colunas) + num_linhas * num_colunas + col] = 0
            else:
                codedPacket[
                    block * (num_linhas * num_colunas + num_linhas + num_colunas) + num_linhas * num_colunas + col] = 1

        ##
        # Calculo dos bits de paridade, que sao colocados
        # no pacote codificado: paridade das linhas.
        ##
        for lin in range(num_linhas):
            sub_total = 0
            for col in range(num_colunas):
                sub_total += parity_matrix[lin][col]

            if sub_total % 2 == 0:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + (
                            num_linhas * num_colunas + num_colunas) + lin] = 0
            else:
                codedPacket[block * (num_linhas * num_colunas + num_linhas + num_colunas) + (
                            num_linhas * num_colunas + num_colunas) + lin] = 1

    return codedPacket


##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decode_packet(transmittedPacket, num_linhas, num_colunas):
    parityMatrix = generate_parity_matrix(num_linhas, num_colunas)
    parityColumns = [0] * num_colunas
    parityRows = [0] * num_linhas
    decodedPacket = [0] * int(
        len(transmittedPacket) / (num_linhas * num_colunas + num_linhas + num_colunas) * (num_linhas * num_colunas))

    block_index = 0  # Contador de blocos no pacote decodificado.

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
        if errorInRow != -1 and errorInColumn != -1:

            if parityMatrix[errorInRow][errorInColumn] == 1:
                parityMatrix[errorInRow][errorInColumn] = 0
            else:
                parityMatrix[errorInRow][errorInColumn] = 1

        ##
        # Colocar bits (possivelmente corrigidos) na saida.
        ##
        for lin in range(num_linhas):
            for col in range(num_colunas):
                decodedPacket[(num_linhas * num_colunas) * block_index + num_colunas * lin + col] = parityMatrix[lin][
                    col]

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
    return [random.randint(0, 1) for x in range(8 * length)]


##
# Gera um numero pseudo-aleatorio com distribuicao geometrica.
##
def geomRand(p):
    uRand = 0
    while (uRand == 0):
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
    n = 0  # Numero de erros inseridos no pacote.

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

def main_program(packet_length, reps, errorProb, num_linhas, num_colunas):
    ##
    # Inicializacao de contadores.
    ##
    totalBitErrorCount = 0
    totalPacketErrorCount = 0
    totalInsertedErrorCount = 0

    ##
    # Inicializacao da semente do gerador de numeros
    # pseudo-aleatorios.
    ##
    random.seed()

    ##
    # Geracao do pacote original aleatorio.
    ##

    originalPacket = generateRandomPacket(packet_length)
    codedPacket = code_packet(originalPacket, num_linhas, num_colunas)

    start_time = time.time()

    ##
    # Loop de repeticoes da simulacao.
    ##
    for i in range(reps):

        ##
        # Gerar nova versao do pacote com erros aleatorios.
        ##
        insertedErrorCount, transmittedPacket = insertErrors(codedPacket, errorProb)
        totalInsertedErrorCount = totalInsertedErrorCount + insertedErrorCount

        ##
        # Gerar versao decodificada do pacote.
        ##
        decodedPacket = decode_packet(transmittedPacket, num_linhas, num_colunas)

        ##
        # Contar erros.
        ##
        bitErrorCount = count_errors(originalPacket, decodedPacket)

        if bitErrorCount > 0:
            totalBitErrorCount = totalBitErrorCount + bitErrorCount
            totalPacketErrorCount = totalPacketErrorCount + 1

    taxaErroBitsAposDec = float(totalBitErrorCount) / float(reps * packet_length * 8) * 100.0
    taxaErroPacote = float(totalPacketErrorCount) / float(reps) * 100.0

    print("####################################################################\n")
    print("\n\n### {}x{} - {} - {} ###\n".format(num_linhas, num_colunas, packet_length, errorProb))

    print('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
    print('Numero de bits transmitidos: {0:d}'.format(reps * packet_length * 8))
    print('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
    print('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(
        (float(totalInsertedErrorCount) / float(reps * len(codedPacket))) * 100.0))
    print('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
    print('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(
        float(totalBitErrorCount) / float(reps * packet_length * 8) * 100.0))
    print('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
    print('Taxa de erro de pacotes: {0:.2f}%'.format(float(totalPacketErrorCount) / float(reps) * 100.0))
    execTime = str(time.time() - start_time)[:4]
    print(f'\nTempo total de execucao: {execTime}s')

    print("\n####################################################################\n")

    return totalInsertedErrorCount, totalBitErrorCount, taxaErroBitsAposDec, totalPacketErrorCount, taxaErroPacote, execTime


### GERADOR DE TESTES ###
matrix_lengths = [(4, 4), (6, 6), (8, 8)]
packet_lengths = [100, 1000, 10000]
error_probs = [0.00005, 0.0005, 0.005]

columns = ['Tamanho_Matriz', 'Tamanho_Pacote', 'Probabilidade_Erro', 'Bits_Errados_Inseridos',
                                  'Bits_Corrompidos_Apos_Dec', 'Taxa_Bits_Corrompidos_Apos_Dec', 'Pacotes_Corrompidos',
                                  'Taxa_Pacotes_Corrompidos', 'Tempo_Exec']

dataTable = pd.DataFrame(columns=columns)

for matrix_length in matrix_lengths:
    for packet_length in packet_lengths:
        for error_prob in error_probs:
            totalInsertedErrorCount, totalBitErrorCount, taxaErroBitsAposDec, totalPacketErrorCount, taxaErroPacote,\
                execTime = main_program(packet_length, 1000, error_prob, matrix_length[0], matrix_length[1])

            new_line = pd.DataFrame(pd.Series(['{}x{}'.format(matrix_length[0], matrix_length[1]), packet_length,
                                               error_prob, totalInsertedErrorCount,
                                               totalBitErrorCount, taxaErroBitsAposDec, totalPacketErrorCount,
                                               taxaErroPacote, execTime], index=columns)).T

            dataTable = pd.concat([dataTable, new_line], ignore_index=True)

print("### Tabela Final ###")
print(dataTable)
dataTable.to_csv("{}\\dados.csv".format(os.getcwd()))
