import serial
import csv
import time

# Configurações
SERIAL_PORT = '/dev/ttyACM0'  # Ajuste conforme necessário
BAUD_RATE = 115200
OUTPUT_FILE = 'csi_data.csv'

def collect_data():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Conectado a {SERIAL_PORT}. Gravando em {OUTPUT_FILE}...")
        
        with open(OUTPUT_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            
            while True:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                if line.startswith("CSI_DATA"):
                    # O log original tem o formato CSV puro após o prefixo
                    data = line.split(',')
                    writer.writerow(data)
                    print("Dado capturado:", data[0:3]) # Print breve para acompanhar
                    
    except KeyboardInterrupt:
        print("Coleta encerrada.")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    collect_data()