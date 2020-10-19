import random
import math
import sys
import os
import time
import pandas as pd

#########
# Implementacao um esquema sem qualquer metodo de codificao.
#
# Cada byte do pacote original eh mapeado para o mesmo byte no pacote
# codificado.
########

###
##
# Funcoes a serem alteradas!
##
###

##
# Codifica o pacote de entrada, gerando um pacote
# de saida com bits redundantes.
##
def codePacket(originalPacket):

    # Sem codificacao, basta copiar conteudo do pacote.
    return list(originalPacket)

##
# Executa decodificacao do pacote transmittedPacket, gerando
# novo pacote decodedPacket.
##
def decodePacket(transmittedPacket):

    # Sem codificacao, basta copiar conteudo do pacote
    return list(transmittedPacket)

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
def generateRandomPacket(l):

    return [random.randint(0,1) for x in range(8 * l)]

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

    while 1:

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
# o pacote original. O parametro packet_l
#ength especifica o
# tamanho dos dois pacotes em bytes.
##
def countErrors(originalPacket, decodedPacket):

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
    sys.stderr.write("\t" + selfName + " <tam_pacote> <reps> <prob. erro>\n\n")
    sys.stderr.write("Onde:\n")
    sys.stderr.write("\t- <tam_pacote>: tamanho do pacote usado nas simulacoes (em bytes).\n")
    sys.stderr.write("\t- <reps>: numero de repeticoes da simulacao.\n")
    sys.stderr.write("\t- <prob. erro>: probabilidade de erro de bits (i.e., probabilidade\n")
    sys.stderr.write("de que um dado bit tenha seu valor alterado pelo canal.)\n\n")

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

def main_program(packet_length, reps, errorProb):
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
    codedPacket = codePacket(originalPacket)

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
        decodedPacket = decodePacket(transmittedPacket)

        ##
        # Contar erros.
        ##
        bitErrorCount = countErrors(originalPacket, decodedPacket)

        if bitErrorCount > 0:

            totalBitErrorCount = totalBitErrorCount + bitErrorCount
            totalPacketErrorCount = totalPacketErrorCount + 1

    taxaErroBitsAposDec = float(totalBitErrorCount) / float(reps * packet_length * 8) * 100.0
    taxaErroPacote = float(totalPacketErrorCount) / float(reps) * 100.0

    print('Numero de transmissoes simuladas: {0:d}\n'.format(reps))
    print('Numero de bits transmitidos: {0:d}'.format(reps * packet_length * 8))
    print('Numero de bits errados inseridos: {0:d}\n'.format(totalInsertedErrorCount))
    print('Taxa de erro de bits (antes da decodificacao): {0:.2f}%'.format(float(totalInsertedErrorCount) / float(reps * len(codedPacket)) * 100.0))
    print('Numero de bits corrompidos apos decodificacao: {0:d}'.format(totalBitErrorCount))
    print('Taxa de erro de bits (apos decodificacao): {0:.2f}%\n'.format(taxaErroBitsAposDec))
    print('Numero de pacotes corrompidos: {0:d}'.format(totalPacketErrorCount))
    print('Taxa de erro de pacotes: {0:.2f}%'.format(taxaErroPacote))
    execTime = str(time.time() - start_time)[:4]
    print(f'\nTempo total de execucao: {execTime}s')

    return totalInsertedErrorCount, totalBitErrorCount, taxaErroBitsAposDec, totalPacketErrorCount, taxaErroPacote, execTime


### GERADOR DE TESTES ###
packet_lengths = [100, 1000, 10000]
error_probs = [0.00005, 0.0005, 0.005]

columns = ['Tamanho_Pacote', 'Probabilidade_Erro', 'Bits_Errados_Inseridos', 'Bits_Corrompidos_Apos_Dec',
           'Taxa_Bits_Corrompidos_Apos_Dec', 'Pacotes_Corrompidos', 'Taxa_Pacotes_Corrompidos', 'Tempo_Exec']

dataTable = pd.DataFrame(columns=columns)

for packet_length in packet_lengths:
    for error_prob in error_probs:
        totalInsertedErrorCount, totalBitErrorCount, taxaErroBitsAposDec, totalPacketErrorCount, taxaErroPacote,\
            execTime = main_program(packet_length, 1000, error_prob)

        new_line = pd.DataFrame(pd.Series([packet_length, error_prob, totalInsertedErrorCount,
                                           totalBitErrorCount, taxaErroBitsAposDec, totalPacketErrorCount,
                                           taxaErroPacote, execTime], index=columns)).T

        dataTable = pd.concat([dataTable, new_line], ignore_index=True)

print("### Tabela Final ###")
print(dataTable)
dataTable.to_csv("{}\\noFEC_dados.csv".format(os.getcwd()))
