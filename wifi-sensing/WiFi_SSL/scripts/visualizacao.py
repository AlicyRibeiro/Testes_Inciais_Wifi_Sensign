import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import argparse  # Nova importação para permitir argumentos

def parse_csi_string(csi_str):
    """
    Remove colchetes e converte a string de números espaçados em um array numpy.
    """
    # Remove colchetes e limpa espaços extras
    clean_str = re.sub(r'[\[\]]', '', str(csi_str)).strip()
    if not clean_str:
        return np.array([])
    # Converte para float
    return np.fromstring(clean_str, sep=' ')

def process_csi_to_amplitude(csi_array):
    """
    Converte o array 1D intercalado [I, Q, I, Q...] para Amplitude.
    """
    if len(csi_array) % 2 != 0:
        # Se por algum motivo vier um número ímpar de amostras, remove a última
        csi_array = csi_array[:-1]
        
    # Agrupa em pares (Real, Imaginário)
    complex_data = csi_array.reshape(-1, 2)
    
    # Calcula a Amplitude: sqrt(Real^2 + Imag^2)
    amplitude = np.sqrt(complex_data[:, 0]**2 + complex_data[:, 1]**2)
    return amplitude

def plot_csi_spectrogram(csv_file):
    print(f"Lendo o arquivo {csv_file}...")
    
    # Lendo o CSV. 
    # O on_bad_lines='skip' evita que o script quebre se uma linha no CSV for cortada pela metade
    try:
        df = pd.read_csv(csv_file, header=None, on_bad_lines='skip')
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return

    print(f"Total de frames capturados: {len(df)}")
    
    # A coluna final (índice 25 no seu log) é a string com os colchetes
    csi_column = df.iloc[:, -1]
    
    amplitudes = []
    
    for idx, csi_str in enumerate(csi_column):
        raw_array = parse_csi_string(csi_str)
        if len(raw_array) > 0:
            amp = process_csi_to_amplitude(raw_array)
            amplitudes.append(amp)
            
    if not amplitudes:
        print("Nenhum dado válido de CSI encontrado para plotar.")
        return

    # Converte lista de arrays para matriz (Tempo x Subportadoras)
    # Transposta (.T) para que o tempo fique no eixo X
    csi_matrix = np.vstack(amplitudes).T
    
    # --- PROCESSAMENTO BÁSICO DE RADAR (Remoção do fundo estático) ---
    # Subtrai a média de cada subportadora (linha) para remover componentes estáticos
    media_das_subportadoras = np.mean(csi_matrix, axis=1, keepdims=True)
    csi_matrix_dinamica = csi_matrix - media_das_subportadoras
    
    # Plotagem
    plt.figure(figsize=(12, 6))
    
    # Usamos vmin e vmax para dar um limite de contraste nas cores
    plt.imshow(csi_matrix_dinamica, aspect='auto', cmap='jet', origin='lower',
               vmin=-np.std(csi_matrix_dinamica)*2, vmax=np.std(csi_matrix_dinamica)*2)
    
    plt.colorbar(label='Variação de Amplitude')
    plt.xlabel('Tempo (Frames de Pacotes Wi-Fi)')
    plt.ylabel('Índice da Subportadora')
    plt.title('Espectrograma CSI - Detecção de Movimento')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
  # Configura o argumento para receber o caminho do arquivo via terminal
    parser = argparse.ArgumentParser(description="Visualizador de dados CSI")
    parser.add_argument("csv_path", type=str, help="Caminho completo ou relativo para o arquivo CSV")
    
    args = parser.parse_args()
    
    # Chama a função passando o arquivo que você digitou no terminal
    plot_csi_spectrogram(args.csv_path)