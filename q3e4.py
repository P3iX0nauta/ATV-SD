import time
import threading
import random

class No:
    def __init__(self, id):
        self.id = id
        self.ativo = True

    def __repr__(self):
        return f'No({self.id}, ativo={self.ativo})'

class SistemaDistribuido:
    def __init__(self, nos):
        self.nos = sorted(nos, key=lambda no: no.id, reverse=True)
        self.coordenador = self.nos[0]
        self.executar()

    def eleicao_bully(self):
        ativos = [no for no in self.nos if no.ativo]
        self.coordenador = max(ativos, key=lambda no: no.id)
        print(f'Novo coordenador: No {self.coordenador.id}')

    def monitorar_heartbeat(self):
        while True:
            print(f'Heartbeat do coordenador {self.coordenador.id}')
            if not self.coordenador.ativo:
                print(f'Coordenador {self.coordenador.id} falhou! Iniciando eleição...')
                self.eleicao_bully()
            time.sleep(2)

    def simular_falha(self, id_no):
        for no in self.nos:
            if no.id == id_no:
                no.ativo = False
                print(f'No {id_no} falhou!')
                break

    def simular_recuperacao(self, id_no):
        for no in self.nos:
            if no.id == id_no:
                no.ativo = True
                print(f'No {id_no} recuperado!')
                self.eleicao_bully()
                break

    def executar(self):
        threading.Thread(target=self.monitorar_heartbeat, daemon=True).start()

nos = [No(i) for i in range(1, 6)]
sistema = SistemaDistribuido(nos)

time.sleep(5)
sistema.simular_falha(sistema.coordenador.id)

time.sleep(5)
sistema.simular_recuperacao(5)

time.sleep(5)
sistema.simular_falha(5)

time.sleep(5)
sistema.simular_falha(4)

time.sleep(5)
sistema.simular_falha(sistema.coordenador.id)

time.sleep(5)
sistema.simular_recuperacao(sistema.coordenador.id)


