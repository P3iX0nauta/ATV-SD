import threading
import time
import random

class Empresa:
    def __init__(self, id_empresa):
        self.id_empresa = id_empresa
        self.relogio = 0
        self.lock = threading.Lock()

    def incrementar_relogio(self):
        with self.lock:
            self.relogio += 1
            return self.relogio

    def atualizar_relogio(self, relogio_recebido):
        with self.lock:
            self.relogio = max(self.relogio, relogio_recebido) + 1

    def enviar_mensagem(self, destino, mensagem):
        timestamp = self.incrementar_relogio()
        print(f"Empresa {self.id_empresa} enviando mensagem para Empresa {destino.id_empresa} com timestamp {timestamp}")
        destino.receber_mensagem(self.id_empresa, mensagem, timestamp)

    def receber_mensagem(self, id_remetente, mensagem, timestamp):
        self.atualizar_relogio(timestamp)
        print(f"Empresa {self.id_empresa} recebeu mensagem de Empresa {id_remetente}: '{mensagem}' (timestamp: {timestamp}). Relógio atualizado para {self.relogio}")

    def evento_local(self):
        timestamp = self.incrementar_relogio()
        print(f"Empresa {self.id_empresa} realizou um evento local. Relógio atualizado para {self.relogio}")

def simular_empresa(empresa, empresas):
    for _ in range(3): 
        acao = random.choice(["local", "enviar"])
        if acao == "local":
            empresa.evento_local()
        else:
            destino = random.choice(empresas)
            while destino == empresa:  
                destino = random.choice(empresas)
            mensagem = f"Olá da Empresa {empresa.id_empresa}"
            empresa.enviar_mensagem(destino, mensagem)
        time.sleep(random.random())  

def imprimir_estado(empresas):
    print("\n--- Estado Atual das Empresas ---")
    for empresa in empresas:
        print(f"Empresa {empresa.id_empresa}: Relógio = {empresa.relogio}")
    print("--------------------------------\n")

central = Empresa(1)
filial1 = Empresa(2)
filial2 = Empresa(3)
filial3 = Empresa(4)
empresas = [central, filial1, filial2, filial3]

print("=== Estado Inicial das Empresas ===")
imprimir_estado(empresas)

threads = []
for empresa in empresas:
    thread = threading.Thread(target=simular_empresa, args=(empresa, empresas))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\n=== Estado Final das Empresas ===")
imprimir_estado(empresas)