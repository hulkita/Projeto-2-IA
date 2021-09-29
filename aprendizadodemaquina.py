import pandas as pd
import numpy as np
import math

df = pd.read_csv("accident_data.csv")
# a = df.loc[0:, ['Genre']].to_numpy()

matriz = df.values
# AlGUMAS CONSTANTES UTEIS
# somente será utilizado como dados 80% das linhas que significa linha do 0 ao 350.
limite = 350

# Data,Countries,Local,Industry Sector,Accident Level,Potential Accident Level,Genre,Employee ou Terceiro,Risco Critico
# Exemplo de entrada
Data = "2016-02-21 00:00:00"
country = "Country_01"

Industry_Sector = "Mining"
Accident_Level = "III"
Potential_Accident_Level = "IV"
Genre = "Male"
Employee_ou_Terceiro = "Third Party"
Risco_Critico = "Others"
teste1 = "Accident Level"
#teste = df.query('Genre == "Male" & `format(teste1)` == "I"').head().to_numpy()
#print(teste.shape[0])

tipos_level = ["I", "II", "III", "IV"]
local = ["Local_01", "Local_02", "Local_03", "Local_04", "Local_05", "Local_06", "Local_07", "Local_08", "Local_09",
         "Local_10", "Local_11", "Local_12"]


# def calcular_entropia_item(palavra, coluna):
# for i in range(0, 350):
# return

def descobrir_nodo():
    return


def find_entropia_palavra(coluna_palavra, palavra):
    quant = [0, 0, 0, 0]
    entropia_palavra = 0
    aux = 0
    for tipo in tipos_level:
        n_ocorrencias = 0
        for i in range(0, 350):
            if matriz[i][coluna_palavra] == palavra and matriz[i][4] == tipo:
                n_ocorrencias = n_ocorrencias + 1

        quant[aux] = n_ocorrencias
        aux = aux + 1

    quant_total = quant[0] + quant[1] + quant[2] + quant[3]

    for i in range(0, 4):
        if quant[i] != 0:
            entropia_palavra = entropia_palavra - ((quant[i] / quant_total) * (math.log2(quant[i] / quant_total)))

    return entropia_palavra


def calcular_ganho(palavra, coluna_palavra, coluna):
    ganho = 0
    lista_aux = []
    for i in range(0, limite):
        ja_contado = 0
        for elemento in lista_aux:
            if matriz[i][coluna] == elemento:
                ja_contado = 1
        if ja_contado == 0:
            lista_aux.append(matriz[i][coluna])
    quant = []
    for i in lista_aux:
        n_ocorrencias = 0
        for linha in range(0, limite):
            if matriz[linha][coluna_palavra] == palavra and matriz[linha][coluna] == i:
                n_ocorrencias = n_ocorrencias + 1

        quant.append(n_ocorrencias)
    quant_total = 0
    for i in quant:
        quant_total = quant_total + i
    for i in range(0, len(quant)):
        if quant[i] != 0:
            ganho = ganho - (quant[i] / quant_total) * (find_entropia_palavra(coluna, lista_aux[i]))

    return ganho


def find_entropia_inicial():
    tipos_de_acidente = ["I", "II", "III", "IV"]
    entropia_total = 0

    for i in tipos_de_acidente:
        n_de_ocorrencia = 0
        for j in range(0, limite):
            if matriz[j][4] == i:
                n_de_ocorrencia = n_de_ocorrencia + 1

        if n_de_ocorrencia != 0:
            n_de_ocorrencia = n_de_ocorrencia / 350
            entropia_total = entropia_total - (n_de_ocorrencia * math.log2(n_de_ocorrencia))

    return entropia_total


def calcular_ganho_coluna_inicial(coluna):
    ganho = 0
    lista_aux = []
    for i in range(0, limite):
        ja_contado = 0
        for elemento in lista_aux:
            if matriz[i][coluna] == elemento:
                ja_contado = 1
        if ja_contado == 0:
            lista_aux.append(matriz[i][coluna])
    quant = []
    for i in lista_aux:
        n_ocorrencias = 0
        for linha in range(0, limite):
            if matriz[linha][coluna] == i:
                n_ocorrencias = n_ocorrencias + 1

        quant.append(n_ocorrencias)

    quant_total = 0
    for i in quant:
        quant_total = quant_total + i
    for i in range(0, len(quant)):
        if quant[i] != 0:
            ganho = ganho - (quant[i] / quant_total) * (find_entropia_palavra(coluna, lista_aux[i]))
    #print(ganho)
    return ganho

def procurar_a_maior_ocorrencia(palavra, coluna, info_entrada, entrada_palavras):
    quant = [0, 0, 0, 0]
    aux = 0
    for tipo in tipos_level:
        n_ocorrencias = 0
        for i in range(0, 350):
            if matriz[i][coluna] == palavra and matriz[i][4] == tipo:
                falhou = 0
                for aux2 in range(0, 9):
                    if info_entrada[aux2] == 2:
                        if matriz[i][aux2] != entrada_palavras[aux2]:
                            falhou = 1

                if falhou == 0:
                    n_ocorrencias = n_ocorrencias + 1



        quant[aux] = n_ocorrencias
        aux = aux + 1
    print(quant)
    for i in range(0, 4):
        if quant[i] == max(quant):
            return tipos_level[i]


def receber_entrada():
    entrada_palavras = ["2016-07-27 00:00:00", "Country_01", "Local_03", "Mining", "II", "IV", "Male", "Employee", "Others"]
    info_entrada = [0, 1, 1, 1, 0, 1, 1, 1, 1]
    entropia_total = find_entropia_inicial()
    # calculando primeiro elemento da arvore
    entropia_max = 0

    id_palavra_ligacao = 3
    for i in range(0, 9):
        if info_entrada[i] == 1:
            entropia_da_coluna = entropia_total + calcular_ganho_coluna_inicial(i)
            if entropia_da_coluna >= entropia_max:
                entropia_max = entropia_da_coluna
                id_palavra_ligacao = i

    info_entrada[id_palavra_ligacao] = 2

    entropia_da_palavra_ligacao = find_entropia_palavra(id_palavra_ligacao, entrada_palavras[id_palavra_ligacao])

    palavra_de_ligacao = entrada_palavras[id_palavra_ligacao]

    while entropia_da_palavra_ligacao != 0 and (info_entrada[3] == 1 or info_entrada[5] == 1 or info_entrada[6] == 1 or info_entrada[7] == 1 or info_entrada[8] == 1):
        ganho_max = 0
        for i in range(0, 9):
            if info_entrada[i] == 1:
                ganho_coluna = entropia_da_palavra_ligacao + calcular_ganho(palavra_de_ligacao, id_palavra_ligacao, i)
                #print(ganho_coluna, info_entrada)
                if ganho_coluna == 0:
                    info_entrada[i] = 2
                if ganho_coluna >= ganho_max and ganho_coluna != 0:
                    ganho_max = ganho_coluna
                    id_palavra_ligacao = i
        if ganho_max > 0:
            info_entrada[id_palavra_ligacao] = 2
            palavra_de_ligacao = entrada_palavras[id_palavra_ligacao]
            entropia_da_palavra_ligacao = find_entropia_palavra(id_palavra_ligacao, entrada_palavras[id_palavra_ligacao])
        if ganho_max == 0:
            break
    print(entropia_da_palavra_ligacao)
    print(info_entrada)
    decisao_final = procurar_a_maior_ocorrencia(palavra_de_ligacao, id_palavra_ligacao, info_entrada, entrada_palavras)
    print(decisao_final)

receber_entrada()

