import threading
import time
import random
from datetime import datetime


class ContaBancaria:
    def __init__(self, saldo_inicial):
        self.saldo = saldo_inicial
        self.lock = threading.Lock()
        self.historico = []

    def registrar_operacao(self, hora, thread, tipo, valor):
        self.historico.append({
            "hora": hora,
            "thread": thread,
            "tipo": tipo,
            "valor": valor,
            "saldo": self.saldo
        })

    def depositar(self, valor):
        with self.lock:
            hora = datetime.now().strftime("%H:%M:%S")
            thread = threading.current_thread().name

            self.saldo += valor

            self.registrar_operacao(
                hora,
                thread,
                "DEPÓSITO",
                valor
            )

            print(
                f"[{hora}] [{thread}] "
                f"[DEPÓSITO] +R${valor:<4} | "
                f"Saldo atual: R${self.saldo}"
            )

    def sacar(self, valor):
        with self.lock:
            hora = datetime.now().strftime("%H:%M:%S")
            thread = threading.current_thread().name

            if self.saldo >= valor:
                self.saldo -= valor

                self.registrar_operacao(
                    hora,
                    thread,
                    "SAQUE",
                    valor
                )

                print(
                    f"[{hora}] [{thread}] "
                    f"[SAQUE]    -R${valor:<4} | "
                    f"Saldo atual: R${self.saldo}"
                )

            else:
                self.registrar_operacao(
                    hora,
                    thread,
                    "SAQUE_NEGADO",
                    valor
                )

                print(
                    f"[{hora}] [{thread}] "
                    f"[SAQUE]    R${valor} não realizado "
                    f"(saldo insuficiente)"
                )

    def mostrar_extrato(self):
        print("\n=== EXTRATO BANCÁRIO ===")

        for operacao in self.historico:
            print(
                f"{operacao['hora']} | "
                f"{operacao['thread']} | "
                f"{operacao['tipo']} | "
                f"R${operacao['valor']:<4} | "
                f"Saldo: R${operacao['saldo']}"
            )


def operacoes_deposito(conta):
    for _ in range(5):
        valor = random.randint(50, 300)

        conta.depositar(valor)

        time.sleep(random.uniform(0.5, 1.5))


def operacoes_saque(conta):
    for _ in range(5):
        valor = random.randint(50, 300)

        conta.sacar(valor)

        time.sleep(random.uniform(0.5, 1.5))


# Conta compartilhada
conta = ContaBancaria(1000)

# Threads
threads = [
    threading.Thread(
        target=operacoes_deposito,
        args=(conta,),
        name="Caixa-Depósito"
    ),

    threading.Thread(
        target=operacoes_saque,
        args=(conta,),
        name="Caixa-Saque-1"
    ),

    threading.Thread(
        target=operacoes_saque,
        args=(conta,),
        name="Caixa-Saque-2"
    )
]

# Início do sistema
print("=== SISTEMA BANCÁRIO CONCORRENTE ===")
print("Simulação de operações bancárias simultâneas.\n")

# Inicializa threads
for t in threads:
    t.start()

# Aguarda finalização
for t in threads:
    t.join()

# Resultado final
print("\n=== ENCERRAMENTO ===")
print(f"Saldo final: R${conta.saldo}")

# Extrato final
conta.mostrar_extrato()