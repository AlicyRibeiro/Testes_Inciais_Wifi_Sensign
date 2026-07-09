# ESP32 Wi-Fi Sensing & CSI Analysis

Pesquisa aplicada sobre Wi-Fi Sensing utilizando sinais CSI (Channel State Information) coletados por ESP32 para detecção de presença e movimento humano, desenvolvida no âmbito do curso de Engenharia de Computação da UFC Quixadá.



##  Resultados Preliminares
O projeto já conta com um pipeline funcional:
* **Firmware:** Firmware customizado no ESP32 capaz de transmitir e capturar pacotes com injeção de dados CSI.
* **Coleta:** Scripts Python robustos para aquisição e armazenamento de dados em formato estruturado (`.csv`).
* **Processamento:** Algoritmos de tratamento de sinal para extração de amplitude e remoção de ruído estático, permitindo a visualização de espectrogramas de movimento.

*Consulte a pasta `ufc_salaca` para visualizar os espectrogramas gerados (ex: `sala_CA.png`).*

##  Stack Tecnológica
* **Hardware:** 2x ESP32 (AP e Station).
* **Firmware:** ESP-IDF v6.0.2.
* **Processamento de Dados:** Python 3.12 (NumPy, Pandas, Matplotlib).
* **Ambiente:** Ubuntu 24.04+ com VS Code.

##  Estrutura do Repositório

```text
pesquisa_wifi-sensing/
├── archive/                  # Pasta para guardar tudo que é "legado" (Blink, Hello_World, Testes_Iniciais)
├── firmware/                 # Todo o código C++ que vai para os ESP32
│   ├── active_ap/            # (Movido do ESP32-CSI-Tool)
│   ├── active_sta/           # (Movido do ESP32-CSI-Tool)
│   └── passive/              # (Movido do ESP32-CSI-Tool)
├── research_workspace/       # O seu trabalho principal (Antigo WiFi_SSL)
│   ├── dataset/              # Todos os seus .csv organizados aqui
│   └── scripts/              # Seus scripts Python (coletor e visualizacao)
├── docs/                     # Relatórios, LOG_DE_ERROS.md e README.md
└── .venv/                    # Seu ambiente virtual (deixe aqui na raiz)
```


## Como Executar

1. Ambiente de Firmware

Para compilar e gravar o código no ESP32:

1. Navegue até o firmware: 

   ``` cd firmware/active_sta/ ```

2. Carregue o ambiente do ESP-IDF: 

    ``` source /home/ana-ribeiro/.espressif/v6.0.2/esp-idf/export.sh ```

3. Compile e grave: 

    ``` idf.py build flash -p /dev/ttyACM0 ```

2. Ambiente de Processamento (Python)

    ``` Para analisar os dados coletados: ```

1. Ative o ambiente virtual: 


    ``` source .venv/bin/activate ```

2. Execute a visualização:
    
    ``` python3 research_workspace/scripts/visualizacao.py research_workspace/dataset/nome_do_arquivo.csv ```



## Documentação de Apoio

Encontrou problemas? Consulte nosso LOG_DE_ERROS.md para soluções sobre conflitos de CMake, erros de Python (PEP 668) e falhas na toolchain.

✅ Etapas da Pesquisa

[x] Configuração do ambiente e Toolchain (ESP-IDF)

[x] Implementação do firmware de coleta (CSI)

[x] Desenvolvimento de scripts Python para processamento

[x] Validação experimental (Coleta em ambiente real)

[ ] Implementação de filtros digitais (Butterworth)

[ ] Treinamento de modelos de ML para classificação

[ ] Escrita do artigo final


## Autora

Ana Alicy Ribeiro
Universidade Federal do Ceará (UFC) – Campus Quixadá