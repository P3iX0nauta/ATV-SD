import threading
import time
import random

class Bolsa:
    def __init__(self, id_bolsa):
        self.id_bolsa = id_bolsa
        self.saldo = random.randint(100, 1000) 
        self.estado_local = None  
        self.marcador_recebido = False  
        self.lock = threading.Lock()
        self.mensagens_pendentes = []  

    def enviar_mensagem(self, destino, valor):
        with self.lock:
            self.saldo -= valor
            print(f"Bolsa {self.id_bolsa} enviou {valor} ações para Bolsa {destino.id_bolsa}. Saldo atual: {self.saldo}")
            destino.receber_mensagem(self.id_bolsa, valor)

    def receber_mensagem(self, id_remetente, valor):
        with self.lock:
            if self.marcador_recebido:
                self.saldo += valor
                print(f"Bolsa {self.id_bolsa} recebeu {valor} ações de Bolsa {id_remetente}. Saldo atual: {self.saldo}")
            else:
                self.mensagens_pendentes.append((id_remetente, valor))
                print(f"Bolsa {self.id_bolsa} armazenou mensagem pendente de Bolsa {id_remetente}.")

    def iniciar_snapshot(self):
        with self.lock:
            print(f"Bolsa {self.id_bolsa} iniciando snapshot")
            self.estado_local = self.saldo
            self.marcador_recebido = True
            for id_remetente, valor in self.mensagens_pendentes:
                self.saldo += valor
                print(f"Bolsa {self.id_bolsa} processou mensagem pendente de Bolsa {id_remetente}. Saldo atual: {self.saldo}")
            return self.estado_local

    def receber_marcador(self, id_remetente):
        with self.lock:
            if not self.marcador_recebido:
                print(f"Bolsa {self.id_bolsa} recebeu marcador de Bolsa {id_remetente}. Salvando estado local")
                self.estado_local = self.saldo
                self.marcador_recebido = True
                for id_remetente, valor in self.mensagens_pendentes:
                    self.saldo += valor
                    print(f"Bolsa {self.id_bolsa} processou mensagem pendente de Bolsa {id_remetente}. Saldo atual: {self.saldo}")
            else:
                print(f"Bolsa {self.id_bolsa} já recebeu marcador anteriormente")

def simular_bolsa(bolsa, bolsas):
    for _ in range(3):  
        acao = random.choice(["local", "enviar"])
        if acao == "local":
            with bolsa.lock:
                bolsa.saldo += random.randint(1, 100)
                print(f"Bolsa {bolsa.id_bolsa} realizou um evento local. Saldo atual: {bolsa.saldo}")
        else:
            destino = random.choice([b for b in bolsas if b != bolsa])  
            valor = random.randint(10, 100)
            bolsa.enviar_mensagem(destino, valor)
        time.sleep(random.random())  

def coletar_snapshot(bolsas):
    print("\n=== Iniciando Coleta de Snapshot ===")
    estado_global = {1: bolsas[0].iniciar_snapshot()}
    for bolsa in bolsas[1:]:
        bolsa.receber_marcador(1)
        estado_global[bolsa.id_bolsa] = bolsa.estado_local
    print("\n=== Estado Global Coletado ===")
    for id_bolsa, estado in estado_global.items():
        print(f"Bolsa {id_bolsa}: Saldo = {estado}")
    print("==============================\n")

bolsas = [Bolsa(i) for i in range(1, 5)]

threads = [threading.Thread(target=simular_bolsa, args=(bolsa, bolsas)) for bolsa in bolsas]
for thread in threads:
    thread.start()

time.sleep(2)

coletar_snapshot(bolsas)

for thread in threads:
    thread.join()