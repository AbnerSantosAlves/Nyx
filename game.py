import random
import time
import os


def titulo():
    print("######## Seja bem-vindo #########")


def gerarNumero():
    numeroaleatorio = random.randrange(101)
    return numeroaleatorio

def runing(numeroGerado, tentativas):
    while True:
        tentativas = tentativas + 1
        chute = int(input("Chute um número: "))
        if chute == numeroGerado:
            print(f"Párabens! Você acertou, o número era {numeroGerado}")
            escolha = input("Você deseja continuar (S/N)?")
            if escolha.upper() in ("N", "NAO", "NÃO"):
                print("Finalizando o programa...")
                time.sleep(3)
                break
            elif escolha.upper() in ("S", "SIM"):
                os.system("cls")
                titulo()
                continue
        elif chute < numeroGerado:
            print(f"O número gerado é maior que {chute}")
            continue
        elif chute > numeroGerado:
            print(f"O número gerado é menor que {chute}")
            continue


            
titulo()
nr = gerarNumero()
tentativas = 0
runing(nr, tentativas)
