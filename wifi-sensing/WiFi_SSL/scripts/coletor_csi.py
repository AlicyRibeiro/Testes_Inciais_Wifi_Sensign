import serial
import csv
import time
import os

# Configurações do Hardware
SERIAL_PORT = '/dev/ttyACM0'  # Ajuste se a porta mudar
BAUD_RATE = 115200

def get_save_path():
    """
    Pergunta ao usuário os dados da coleta e monta o caminho do arquivo.
    """
    print("\n--- CONFIGURAÇÃO DA COLETA ---")
    dominio = input("Digite o ambiente (ex: lab, corredor, biblioteca): ").strip().lower()
    atividade = input("Digite a atividade (ex: vazio, andar, sentar): ").strip().lower()
    amostra_num = input("Digite o número da amostra (ex: 01, 02, 03): ").strip()
    
    # Sobe um nível da pasta 'scripts' e entra em 'dataset'
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dataset'))
    dominio_dir = os.path.join(base_dir, f'ufc_{dominio}')
    
    # Cria a pasta do domínio se ela não existir
    os.makedirs(dominio_dir, exist_ok=True)
    
    # Monta o nome final do arquivo
    file_name = f"{atividade}_{amostra_num}.csv"
    full_path = os.path.join(dominio_dir, file_name)
    
    return full_path

def collect_data():
    output_file = get_save_path()
    
    # Pergunta o tempo de gravação
    try:
        duracao_segundos = int(input("Tempo de gravação (em segundos, ex: 15): "))
    except ValueError:
        duracao_segundos = 15
        print("Valor inválido. Usando 15 segundos por padrão.")
    
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"\nConectado a {SERIAL_PORT}.")
        print(f"GRAVANDO OS DADOS EM: {output_file}")
        
        # O Timer para você sair da sala
        print("\nPREPARANDO PARA GRAVAR. VOCÊ TEM 10 SEGUNDOS PARA SAIR DO AMBIENTE...")
        for i in range(10, 0, -1):
            print(f"Iniciando em {i}...", end='\r')
            time.sleep(1)
            
        print("\n\n[ GRAVANDO... ]")
        
        with open(output_file, 'a', newline='') as f:
            writer = csv.writer(f)
            
            tempo_inicio = time.time()
            
            # O loop agora para sozinho quando o tempo acabar
            while (time.time() - tempo_inicio) < duracao_segundos:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("CSI_DATA"):
                    data = line.split(',')
                    writer.writerow(data)
                    print(f"Gravando... Tempo restante: {int(duracao_segundos - (time.time() - tempo_inicio))}s", end='\r')
                    
        print(f"\n\nColeta encerrada com sucesso! Arquivo salvo em: {output_file}")
        
    except KeyboardInterrupt:
        print(f"\n\nColeta abortada pelo usuário.")
    except Exception as e:
        print(f"\nErro na porta serial: {e}")

if __name__ == "__main__":
    # Garante que estamos rodando no diretório do script
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    collect_data()