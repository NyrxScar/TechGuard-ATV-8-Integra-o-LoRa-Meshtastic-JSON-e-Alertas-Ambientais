# Americas TechGuard | ATIVIDADE PROPOSTA 8 - Integração LoRa-Meshtastic, JSON e Alertas Ambientais

**Estudante:** Nyrx Oliveira de Aquino Farias  
**Eixo:** Sistemas Embarcados | LoRa, Meshtastic, LoRaWAN, JSON, IoT, Integração de Dados e Alertas Ambientais  
**Período:** ATIVIDADE 8 | 08/07/2026 até 18/07/2026  
**Docentes:** Valério Piana, Lucas Lacerda e Alex Salazar  
**Entrega:** Trilha B - Software-only / Simulação

---
## Sobre o Projeto

Este repositório apresenta uma simulação em software de uma arquitetura IoT resiliente para monitoramento ambiental e emissão de alertas móveis, desenvolvida como parte da Atividade 8 do projeto Americas TechGuard.

A solução implementa uma cadeia completa de processamento de dados, desde a simulação de sensores ambientais até a geração de payloads JSON, classificação de risco, seleção da arquitetura de comunicação (LoRaWAN ou Meshtastic), publicação via MQTT e visualização de dados espaciais em mapa interativo.

O projeto foi desenvolvido na modalidade Software-only, conforme a escolha da trilha,permitindo a reprodução da solução sem a necessidade de hardware físico, focando em Blumenau-SC como exemplo.

---

## Objetivos

- Simular sensores ambientais em cenários determinísticos de enchente.
- Construir payloads JSON padronizados e enriquecidos com metadados.
- Validar mensagens.
- Classificar automaticamente o risco.
- Simular comunicação LoRa/Meshtastic.
- Utilizar tópicos estruturados MQTT para integração de rede.
- Demonstrar uma arquitetura híbrida.
- Otimizar o consumo de banda de rádio aplicando compressão extrema de payloads.
- Registrar dados simulados em múltiplos formatos de saída(como Jsone e csv) e gerar mapas interativos geoespaciais.
## 1. Estudo Técnico dos Artigos e Arquitetura

Este projeto fundamenta-se nos seguintes materiais técnicos obrigatórios:

1. **Artigo Principal:** *Development of a smart sensing unit for LoRaWAN-based IoT flood monitoring and warning system in catchment areas* . Internet of Things and Cyber-Physical
Systems, 2023. DOI: 10.1016/j.iotcps.2023.04.005.  Link:
(https://www.sciencedirect.com/science/article/pii/S26673452230002'63)
2. **Artigo Complementar:** *A Meshtastic-based LoRa Mesh System for Smart Campus Applications: From Solar-Powered Sensing to Containerized Data Management* (arXiv, 2026). Link:
https://arxiv.org/abs/2605.20379
3. **Documentação de Referência:** [Meshtastic MQTT/JSON Configuration](https://meshtastic.org/docs/configuration/module/mqtt/) e [Telemetry Module](https://meshtastic.org/docs/configuration/module/telemetry/).

### 🔍 Síntese dos Artigos e Solução Proposta:
* **Problema Resolvido pelo Artigo Principal:** Desenvolver um sistema de monitoramento de inundações em tempo real robusto, solar e acessível. O artigo propõe uma unidade de sensoriamento inteligente (baseada em um microcontrolador Arduino e no sensor ultrassônico HC-SR04) que mede o nível d'água em rios e transmite as leituras para plataformas como The Things Network (TTN), TagoIO e ThingSpeak via conexões de rádio LoRaWAN de baixo consumo.
* **Contributos do Artigo Complementar:** O estudo aborda a implementação prática de uma rede mesh descentralizada utilizando o protocolo de código aberto *Meshtastic* para aplicações de Smart Campus. Destaca-se o uso de hardware de baixo consumo (Raspberry Pi Pico + transceptor SX1262) alimentado por energia solar, integrado a uma arquitetura de gerenciamento de dados conteinerizada no Edge Gateway (Raspberry Pi 4 rodando Docker Compose com Mosquitto MQTT, Node-RED para fluxo, InfluxDB para séries temporais e Grafana para painéis de visualização).

---

## 2. 📡 Entendimento de Conceitos

| Termo                                 | O que é                                                                           | Para que serve                                                                                         | Exemplo no Americas TechGuard                                                                    |
| ------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
| **LoRa**                              | Tecnologia de comunicação por rádio.                                              | Enviar pequenas quantidades de dados por longas distâncias gastando pouca bateria.                     | Um sensor envia temperatura, nível do rio ou um alerta usando ondas de rádio LoRa.               |
| **Meshtastic**                        | Aplicativo e protocolo que utiliza LoRa para criar uma rede mesh (malha).         | Permite que dispositivos conversem diretamente entre si, sem depender de internet ou torre de celular. | Equipes de campo trocam mensagens e localização mesmo durante uma enchente sem sinal de celular. |
| **Rede Mesh**                         | Forma de organização da rede.                                                     | Cada dispositivo pode retransmitir mensagens para outros, aumentando o alcance.                        | Um alerta passa de nó em nó até chegar ao destino.                                               |
| **LoRaWAN**                           | Arquitetura de rede baseada em LoRa.                                              | Conectar sensores IoT a gateways e servidores para monitoramento remoto.                               | Sensores espalhados pela cidade enviam dados para um gateway conectado à internet.               |
| **Gateway LoRaWAN**                   | Equipamento que recebe sinais LoRa e envia para a internet.                       | Faz a ponte entre dispositivos LoRa e servidores.                                                      | Um gateway instalado na Defesa Civil recebe dados dos sensores e envia para o sistema central.   |
| **Servidor de Rede (Network Server)** | Software que gerencia uma rede LoRaWAN.                                           | Controla autenticação, segurança e encaminhamento dos dados.                                           | Recebe os dados dos sensores antes de enviá-los ao banco de dados.                               |
| **IoT (Internet das Coisas)**         | Conceito de dispositivos conectados coletando dados automaticamente.              | Automatizar monitoramento e controle.                                                                  | Sensores de chuva, umidade e nível do rio enviando dados continuamente.                          |
| **Off-grid**                          | Funcionamento sem depender da infraestrutura tradicional (internet ou telefonia). | Manter comunicação mesmo quando tudo falha.                                                            | Durante um desastre, celulares com Meshtastic continuam trocando mensagens.                      |
| **JSON**                              | Formato de organização dos dados.                                                 | Facilitar a troca de informações entre sistemas.                                                       | O sensor envia um pacote contendo device_id, timestamp, latitude, longitude etc.                 |
| **MQTT**                              | Protocolo leve de comunicação para IoT.                                           | Transportar os dados dos sensores para servidores.                                                     | O gateway publica os dados em um broker MQTT, que envia ao dashboard.                            |

---
## 3. 📝 Justificativa da Proposta de Confecção da Atividade 

Após estudar os conceitos de LoRa, Meshtastic e LoRaWAN, bem como analisar os materiais de apoio e a documentação indicados na atividade, surgiu a proposta de desenvolver uma arquitetura híbrida de comunicação para o Americas TechGuard. O objetivo dessa abordagem é aumentar a resiliência do sistema de monitoramento ambiental, permitindo sua operação tanto em cenários com infraestrutura de comunicação disponível quanto em situações de desastre, nas quais essa infraestrutura esteja indisponível ou degradada.

É importante destacar que esta implementação não considera Meshtastic e LoRaWAN como tecnologias equivalentes. O Meshtastic é utilizado como uma solução de comunicação em rede mesh descentralizada baseada em LoRa, adequada para cenários off-grid e de comunicação direta entre dispositivos. Já o LoRaWAN é adotado apenas como referência arquitetural para representar ambientes que dispõem de gateways, servidores de rede e conectividade com a infraestrutura convencional.

Dessa forma, a arquitetura híbrida proposta neste projeto representa uma solução acadêmica desenvolvida para o contexto do Americas TechGuard. Em condições normais de operação, quando há disponibilidade de gateway e infraestrutura de rede, a comunicação segue uma arquitetura inspirada no LoRaWAN, permitindo a transmissão dos dados para serviços de monitoramento e processamento. Caso essa infraestrutura se torne indisponível, como em eventos de enchentes, deslizamentos, apagões ou falhas de comunicação, o sistema passa a utilizar uma rede mesh baseada em Meshtastic para manter a disseminação dos alertas entre os dispositivos e garantir a continuidade da comunicação.

Essa abordagem busca demonstrar, por meio de uma simulação em software, como diferentes arquiteturas de comunicação podem ser empregadas de forma complementar para aumentar a disponibilidade, a robustez e a confiabilidade de sistemas de monitoramento e alerta ambiental, respeitando as diferenças conceituais entre Meshtastic e LoRaWAN apresentadas na atividade.

ps: Trata-se de uma proposta arquitetural para fins acadêmicos, em que um Communication Manager decide qual tecnologia utilizar conforme a disponibilidade da infraestrutura.

---
## 4. 📝 Fluxo do Sistema Inicial

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Sensores Ambientais (Simulados ou Hardware)              │
│    • Nível da água • Chuva • Temperatura • Umidade          │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Processamento Local (Edge Computing)                     │
│    • Leitura dos sensores                                   │
│    • Cálculo do nível de risco                              │
│    • Geração da mensagem de alerta                          │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. Construção e Validação do Payload JSON                   │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
               Gateway / Infraestrutura disponível?
                             │
          ┌──────────────────┴──────────────────┐
          │                                     │
        SIM                                    NÃO
          │                                     │
          ▼                                     ▼
┌──────────────────────┐             ┌────────────────────────┐
│ Arquitetura          │             │ Rede Mesh              │
│ inspirada em LoRaWAN │             │ Meshtastic             │
└───────────┬──────────┘             └───────────┬────────────┘
            │                                   │
            └──────────────┬────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ MQTT (Publicação de Eventos e Alertas)                      │
└────────────────────────────┬────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────┐
│ Dashboard • Banco de Dados • Aplicativo • Logs              │
└─────────────────────────────────────────────────────────────┘

```

---

# 5. 📝 Arquitetura do Diretório

```text
TechGuard-ATV-8-Integracao-LoRa-Meshtastic-JSON-e-Alertas-Ambientais/
│
├── MVPS/                                         # Histórico de desenvolvimento e evolução do projeto
│   ├── assets/                                   # Evidências visuais e capturas de tela dos MVPs
│   │   ├── Saída do MVP2.png
│   │   └── Saída do MVP2.6.png
│   │
│   ├── mvp_main.ipynb                            # Notebook utilizado para prototipação e validação incremental
│   ├── mvp2.py                                   # Implementação consolidada do MVP de segunda geração
│   └── README_MVPS.md                            # Documentação técnica da evolução dos MVPs
│
├── outputs/                                      # Artefatos gerados automaticamente pela simulação
│   │
│   ├── csv/                                      # Exportação tabular da telemetria
│   │   └── simulation_*.csv
│   │
│   ├── json/                                     # Payloads produzidos pelo Edge Node
│   │   ├── simulation_*.json                     # Payload completo
│   │   └── simulation_compact_*.json             # Payload otimizado para transmissão LPWAN
│   │
│   ├── maps/                                     # Mapas interativos gerados com Folium
│   │   └── map_*.html
│   │
│   └── reports/                                  # Relatórios estatísticos da execução
│       └── statistics_*.txt
│
├── main.py                                       # Simulador principal da arquitetura híbrida LoRaWAN + Meshtastic
│
└── README.md                                     # Documentação do projeto
```

## Descrição dos Diretórios

| Diretório | Descrição |
|-----------|-----------|
| **MVPS/** | Contém o histórico de desenvolvimento do projeto, incluindo versões intermediárias, experimentos, notebook de prototipação e documentação da evolução dos MVPs. |
| **outputs/csv/** | Armazena os dados consolidados da simulação em formato CSV, permitindo análises estatísticas e importação em ferramentas como Excel, LibreOffice ou Power BI. |
| **outputs/json/** | Contém os payloads produzidos durante a simulação. São exportadas duas versões: uma completa, utilizada para armazenamento e análise, e outra compactada, otimizada para transmissão em redes LPWAN. |
| **outputs/maps/** | Armazena mapas interativos em HTML gerados com Folium, apresentando a distribuição geográfica dos nós simulados, bem como seus respectivos estados e níveis de risco. |
| **outputs/reports/** | Contém relatórios estatísticos gerados automaticamente ao término da simulação, incluindo métricas de processamento, utilização das redes, níveis monitorados e taxa de compressão dos payloads. |
| **main.py** | Script principal responsável por executar toda a simulação, incluindo leitura dos sensores, processamento em Edge Computing, seleção automática da rede de comunicação, compactação da telemetria, publicação MQTT simulada e geração dos artefatos de saída. |

---

## 6. 📝 Modelagem de Dados: Exemplo de Estrutura do Payload JSON com os Rquisitos Mínimos Exigidos pelos Orientadores

O payload utilizado pelo simulador foi modelado para representar a leitura de dados ambientais, estado de risco e avisos na região metropolitana de Blumenau - SC com simulação de múltiplos nós (NODE_BLUMENAU_001 a NODE_BLUMENAU_006):

### Exemplo de Entrada do Cenário A: Condição Segura (Safe) e Gateway Disponível (LoRaWAN):
```json
{
    "schema_version": "1.0.0",
    "firmware_version": "1.2.4",
    "simulation": true,
    "message_id": "9b1deb4d-3b7d-4bad-9bdd-2b0d7b3dcb6d",
    "device_id": "NODE_BLUMENAU_001",
    "timestamp": "2026-07-16T18:00:00Z",
    "latitude": -26.9194,
    "longitude": -49.0661,
    "sensor_type": "ultrasonic_level",
    "sensor_value": 0.6,
    "unit": "m",
    "rain_mm": 0.0,
    "temperature_c": 24.5,
    "humidity_pct": 65,
    "risk_level": "Seguro",
    "alert_message": "Nível da água dentro da normalidade.",
    "source": "LoRaWAN",
    "network_mode": "LoRaWAN",
    "gateway_available": true,
    "mesh_hops": 0,
    "battery_percent": 100,
    "signal_rssi": -75,
    "signal_snr": 7.0,
    "processing_time_ms": 0.124
}

```
### Exemplo de Entrada do Cenário B:Alerta Crítico Off-Grid via Meshtastic (Compactado para Rádio):

Para otimização em redes de rádio de baixa taxa de dados, a classe TelemetryMinimizer reduz o JSON original em aproximadamente 80%, convertendo strings e timestamps ISO em inteiros, códigos curtos e Unix Epoch:
```json

{
    "id": "NODE_BLUMENAU_006",
    "ts": 1784221512,
    "wl": 3.6,
    "rn": 55.0,
    "tp": 18.2,
    "hm": 98,
    "bt": 92,
    "rk": "CR",
    "nt": "MT"
}

```
---

# 7. 📝 Tecnologias Utilizadas

O simulador foi desenvolvido integralmente em **Python**, utilizando bibliotecas da linguagem para processamento de dados, manipulação de arquivos e geração de artefatos da simulação. A Tabela 1 apresenta as principais tecnologias empregadas.

| Tecnologia | Finalidade |
|------------|------------|
| **Python 3** | Linguagem principal utilizada no desenvolvimento do simulador. |
| **Folium** | Geração de mapas interativos em HTML para visualização geográfica dos nós simulados. |
| **JSON** | Estruturação e exportação dos payloads completos e compactados. |
| **CSV** | Exportação tabular dos resultados para análise em planilhas e ferramentas de BI. |
| **Datetime** | Geração de timestamps e medição temporal dos eventos da simulação. |
| **UUID** | Criação de identificadores únicos para cada mensagem transmitida. |
| **Time** | Controle da execução dos ciclos e medição do tempo de processamento do Edge Node. |
| **OS** | Gerenciamento automático de diretórios e arquivos produzidos durante a execução. |

---

# 8. 📝 Fluxo da Simulação

O simulador representa a evolução de um evento hidrológico extremo por meio de **seis ciclos consecutivos**, simulando desde condições ambientais normais até um cenário de falha da infraestrutura de comunicação.

Durante cada ciclo são atualizados diversos parâmetros ambientais e operacionais do dispositivo, permitindo avaliar o comportamento do sistema diante da progressão do desastre.

As variáveis simuladas incluem:

- Nível da água;
- Volume de precipitação;
- Temperatura ambiente;
- Umidade relativa do ar;
- Nível da bateria do dispositivo;
- Intensidade do sinal de rádio (RSSI e SNR);
- Disponibilidade do gateway LoRaWAN;
- Rede de comunicação utilizada.

## Evolução dos Cenários

| Ciclo | Situação Simulada | Rede Utilizada |
|:-----:|-------------------|----------------|
| **1** | Condições ambientais normais | LoRaWAN |
| **2** | Início da precipitação | LoRaWAN |
| **3** | Elevação significativa do nível da água | LoRaWAN |
| **4** | Situação de alerta para inundação | LoRaWAN |
| **5** | Indisponibilidade do Gateway | LoRaWAN (debounce) |
| **6** | Persistência da falha de comunicação | Meshtastic |

Durante a simulação, o algoritmo implementa um mecanismo de **failover com debounce**, realizando a migração para a rede **Meshtastic** apenas após 2 falhas consecutivas na comunicação com o gateway LoRaWAN.

---

# 9. 📝 Componentes da Arquitetura

O sistema foi desenvolvido seguindo uma arquitetura modular, onde cada componente possui responsabilidades bem definidas dentro do fluxo de processamento da informação.

## 9.1 Camada de Simulação dos Sensores

A função

```python
read_simulated_sensors()
```

é responsável por simular o comportamento dos sensores instalados em campo.

Cada ciclo gera leituras determinísticas para:

- nível da água;
- precipitação acumulada;
- temperatura ambiente;
- umidade relativa;
- nível de bateria.

Essa abordagem permite reproduzir exatamente o mesmo cenário em diferentes execuções, facilitando testes e validações.

---

## 9.2 Motor de Classificação de Risco (Edge Computing)

A classe

```python
RiskEngine
```

implementa a lógica de processamento local do dispositivo (*Edge Computing*), realizando a classificação do risco antes do envio das informações para a rede.

A classificação é baseada no nível da água medido pelo sensor.

| Nível da Água | Classificação |
|---------------|---------------|
| **< 1,0 m** | Seguro |
| **1,0 – 1,9 m** | Atenção |
| **2,0 – 2,9 m** | Alerta |
| **≥ 3,0 m** | Crítico |

Essa abordagem reduz a dependência da infraestrutura remota, permitindo que decisões críticas sejam tomadas diretamente no dispositivo.

---

## 9.3 Gerenciador de Comunicação

A classe

```python
CommunicationManager
```

é responsável por selecionar automaticamente a rede de comunicação utilizada pelo dispositivo.

O algoritmo implementa uma estratégia de **failover ativo**, priorizando inicialmente a comunicação via **LoRaWAN**.

Caso o gateway permaneça indisponível por ciclos consecutivos, ocorre a migração automática para a rede **Meshtastic**, garantindo maior resiliência durante eventos extremos.

```text
                Gateway Operacional
                        │
                        ▼
                    LoRaWAN
                        │
          Falhas consecutivas detectadas
                        │
                        ▼
                  Meshtastic Mesh
```

Além disso, é empregado um mecanismo de **debounce**, evitando trocas de rede provocadas por falhas momentâneas na comunicação.

---

## 9.4 Otimização da Telemetria

A classe

```python
TelemetryMinimizer
```

realiza a compactação do payload antes da transmissão, reduzindo significativamente o consumo de banda em redes LPWAN.

Enquanto o payload completo é utilizado para armazenamento e análise, uma versão reduzida é preparada especificamente para transmissão via rádio.

### Payload original

```json
{
    "device_id": "NODE_BLUMENAU_001",
    "risk_level": "Crítico",
    "network_mode": "Meshtastic"
}
```

### Payload compactado

```json
{
    "id": "NODE_BLUMENAU_001",
    "rk": "CR",
    "nt": "MT"
}
```

A compactação reduz a quantidade de bytes transmitidos sem comprometer as informações essenciais necessárias para o monitoramento remoto.

---


# 10. 📝 Artefatos Gerados

Ao término da simulação, o sistema realiza automaticamente a exportação dos dados produzidos durante a execução. Esses artefatos permitem a análise dos resultados, a validação da arquitetura proposta e a integração com ferramentas externas.

| Artefato | Localização | Descrição |
|-----------|-------------|-----------|
| **JSON Completo** | `outputs/json/simulation_*.json` | Contém todos os payloads produzidos pelo Edge Node, incluindo informações ambientais, estado da rede, métricas de comunicação e metadados da simulação. |
| **JSON Compactado** | `outputs/json/simulation_compact_*.json` | Versão otimizada dos payloads para transmissão em redes LPWAN, reduzindo significativamente o consumo de banda. |
| **CSV** | `outputs/csv/simulation_*.csv` | Exportação tabular dos dados, adequada para análises estatísticas, planilhas eletrônicas e ferramentas de Business Intelligence. |
| **Mapa Interativo** | `outputs/maps/map_*.html` | Visualização georreferenciada dos dispositivos simulados em Blumenau (SC), gerada com Folium. |
| **Relatório Estatístico** | `outputs/reports/statistics_*.txt` | Resumo estatístico da execução contendo indicadores de desempenho e métricas da simulação. |

---

## 10.1 Conteúdo do Mapa Interativo

O mapa gerado em HTML apresenta uma representação espacial dos dispositivos simulados, contendo informações detalhadas sobre cada nó da rede.

Cada marcador exibe:

- Identificação do dispositivo;
- Localização geográfica;
- Nível da água;
- Volume de precipitação;
- Temperatura ambiente;
- Umidade relativa;
- Nível da bateria;
- Rede de comunicação utilizada;
- Classificação do risco;
- Intensidade do sinal de rádio (RSSI).

As cores dos marcadores variam de acordo com o nível de risco calculado pelo **Edge Node**, facilitando a identificação visual das regiões críticas.

<p align="center">
  <img src="/MVPS/assets/Mapa interativo blumenau.png" alt="Mapa interativo blumenau" height="400">
  &nbsp;&nbsp;&nbsp;
  <img src="/MVPS/assets/Kpis Mapa Interativo.png" alt="Kpis Mapa Interativo" height="400">
</p>

---
# 11. 📝 Tabelas Comparativas do MVP1 x MVP2 e MVP2 x Main


## Tabela Comparativa da Evolução da Arquitetura: MVP 1 × MVP 2

| Aspecto                         | MVP 1                                                          | MVP 2                                                                                     | Alterações                                                                                       |
| ------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **Objetivo**                    | Simular monitoramento ambiental e comunicação LoRa/Meshtastic. | Validar uma arquitetura híbrida com processamento em borda (*Edge Computing*). | Ampliação do escopo para validação da arquitetura de comunicação híbrida.                        |
| **Estrutura do Código**         | Predominantemente funcional.                                   | Organização orientada a objetos, com classes e responsabilidades definidas.               | Separação da lógica em componentes especializados, favorecendo modularidade e manutenção.        |
| **Simulação dos Sensores**      | Leituras aleatórias (*random*).                                | Cenários determinísticos que representam a evolução de uma enchente.                      | Simulação reproduzível para facilitar testes, validações e demonstrações.                        |
| **Processamento em Borda**      | Lógica concentrada na função `calcular_risco()`.               | Classe `RiskEngine` dedicada ao processamento de borda.                                   | Centralização da lógica de classificação em um componente específico.                            |
| **Classificação de Risco**      | Estados: `SAFE`, `ATTENTION`, `ALERT` e `CRITICAL`.            | Estados: Seguro, Atenção, Alerta e Crítico.                                               | Adequação da nomenclatura ao contexto da aplicação e integração com o restante da arquitetura.   |
| **Comunicação**                 | Seleção direta da rede de transmissão.                         | Classe `CommunicationManager`.                                                            | Centralização da lógica de seleção e gerenciamento da comunicação.                               |
| **Failover (Redundância)**      | Mudança imediata para a rede secundária.                       | Failover com *debounce* após duas falhas consecutivas.                                    | Inclusão de mecanismo para reduzir alternâncias indevidas entre as arquiteturas de comunicação.  |
| **LoRaWAN**                     | Comunicação simulada.                                          | Comunicação simulada com gerenciamento de estado da rede.                                 | Aprimoramento da representação da arquitetura LoRaWAN durante a simulação.                       |
| **Meshtastic**                  | Comunicação simulada.                                          | Comunicação simulada com controle de *mesh hops* e failover.                              | Inclusão de elementos representativos do funcionamento de uma rede Mesh.                         |
| **Gateway**                     | Estado definido diretamente na simulação.                      | Estado gerenciado dinamicamente pelo `CommunicationManager`.                              | Separação da lógica de gerenciamento da infraestrutura de comunicação.                           |
| **Construção do Payload**       | Payload JSON básico.                                           | Payload estruturado e enriquecido com metadados.                                          | Inclusão de informações adicionais para rastreabilidade e integração entre sistemas.             |
| **Identificação das Mensagens** | Não possui identificador único.                                | UUID (`message_id`) para cada payload.                                                    | Inclusão de identificador único para rastreamento das mensagens.                                 |
| **Versionamento**               | Não possui.                                                    | `schema_version` e `firmware_version`.                                                    | Inclusão de informações de versionamento para compatibilidade da solução.                        |
| **Validação do Payload**        | Não possui validação.                                          | Verificação automática dos campos obrigatórios.                                           | Implementação de validação antes da transmissão dos dados.                                       |
| **Compressão LPWAN**            | Não implementada.                                              | Classe `TelemetryMinimizer` responsável pela compactação.                                 | Inclusão de mecanismo para redução do tamanho do payload transmitido.                            |
| **Timestamp**                   | ISO 8601.                                                      | ISO 8601 com conversão para Unix Epoch durante a compactação.                             | Otimização da representação temporal para simulação de transmissão LPWAN.                        |
| **MQTT**                        | Publicação simulada genérica.                                  | Publicação simulada utilizando tópicos específicos para LoRaWAN e Meshtastic.             | Organização da estrutura de tópicos conforme a arquitetura utilizada.                            |
| **Métricas de Comunicação**     | RSSI, SNR e bateria.                                           | RSSI, SNR, bateria, *Mesh Hops* e tempo de processamento.                                 | Ampliação das métricas coletadas durante a execução da simulação.                                |
| **Tempo de Processamento**      | Não disponível.                                                | Medição através de `processing_time_ms`.                                                  | Inclusão de indicador de desempenho do processamento local.                                      |
| **Diagnóstico da Compressão**   | Não disponível.                                                | Exibição do tamanho original, compactado e percentual de redução.                         | Inclusão de métricas para avaliação da eficiência da compactação.                                |
| **Saída da Simulação**          | Exibe apenas o payload JSON no terminal.                       | Exibe resumo operacional, métricas e payload compactado.                                  | Organização das informações apresentadas durante a execução da simulação.                        |
| **Escalabilidade**              | Estrutura limitada ao escopo inicial.                          | Arquitetura modular preparada para futuras integrações.                                   | Estrutura organizada para facilitar evolução com hardware, brokers MQTT e persistência de dados. |

## MVP2 x Main

| Aspecto | `mvp2.py` | `main.py`  |
| :--- | :--- | :--- |
| **Foco Geográfico** | Florianópolis (coordenadas e IDs de Floripa). | **Blumenau** (coordenadas reais do centro de Blumenau e IDs `NODE_BLUMENAU`). |
| **Persistência de Dados** | Apenas printa no terminal. Não salva os arquivos JSON, CSV ou mapas. | **Salva automaticamente** em pastas estruturadas (`outputs/json/`, `outputs/csv/`, etc.). |
| **Nomenclatura de Arquivos** | Não aplicável. | Nomeia os arquivos usando **timestamp** da execução para que um teste não apague o anterior. |
| **Representação dos Sensores** | Simula apenas 1 único sensor estático. | Simula **múltiplos sensores** com pequenos desvios de localização geográfica. |
| **LPWAN (Redes de Rádio)** | Compacta na memória mas não exporta o arquivo. | Exporta a simulação normal e a **versão compactada para rádio** (`simulation_compact.json`) separadamente. |
| **Mapa Dinâmico** | Não possui mapa. | Gera um **mapa interativo HTML (Folium)** contendo marcadores coloridos com popups ricos de telemetria. |
| **Estatísticas** | Não calcula indicadores agregados. | Gera e exibe no terminal um **painel estatístico** (médias, maior chuva, redução de rádio) e o salva como relatório (`reports/statistics.txt`). |
| **Organização do Código** | Procedural simples no main. | **Modularizado em funções**, separando a lógica da simulação das funções de exportação. |

---

# 12. 📝 Guia de Execução do Sistema

Esta seção apresenta o passo a passo para configurar o ambiente, executar o simulador e acessar os artefatos gerados automaticamente pelo **Americas TechGuard**.

---

## 12.1 Pré-requisitos

Antes de executar o projeto, certifique-se de possuir os seguintes requisitos instalados em sua máquina:

- **Python 3.10** ou superior;
- **pip** (gerenciador de pacotes do Python).

O projeto utiliza principalmente bibliotecas nativas do Python (`os`, `csv`, `json`, `time`, `uuid` e `datetime`), sendo necessária apenas uma dependência externa:

| Biblioteca | Finalidade |
|------------|------------|
| **Folium** | Geração do mapa interativo em HTML contendo a localização dos dispositivos simulados. |

---

## 12.2 Configuração do Ambiente

Embora não seja obrigatório, recomenda-se utilizar um ambiente virtual (*Virtual Environment*) para manter as dependências do projeto isoladas.

### Passo 1 — Acessar o diretório do projeto

Abra um terminal na pasta raiz do projeto:

```bash
cd TechGuard-ATV-8-Integracao-LoRa-Meshtastic-JSON-e-Alertas-Ambientais
```

### Passo 2 — Criar um ambiente virtual (Opcional)

#### Windows (Prompt de Comando ou PowerShell)

```bash
python -m venv venv

venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv

source venv/bin/activate
```

### Passo 3 — Instalar as dependências

Instale a biblioteca utilizada pelo projeto:

```bash
pip install folium
```

Caso exista um arquivo `requirements.txt`, basta executar:

```bash
pip install -r requirements.txt
```

---

## 12.3 Executando o Simulador

Com o ambiente configurado, execute o script principal:

```bash
python main.py
```

O simulador iniciará automaticamente a execução da arquitetura híbrida proposta, realizando todas as etapas de processamento e exportação dos resultados.

---

## 12.4 Fluxo de Execução

Durante a execução, o sistema realiza automaticamente **seis ciclos determinísticos**, simulando a evolução de um evento hidrológico em Blumenau (SC).

Em cada ciclo são executadas as seguintes etapas:

1. Simulação das leituras dos sensores ambientais;
2. Processamento local das informações pelo **Risk Engine** (*Edge Computing*);
3. Classificação automática do nível de risco;
4. Verificação da disponibilidade do Gateway LoRaWAN;
5. Seleção automática da rede de comunicação (LoRaWAN ou Meshtastic);
6. Compactação do payload para transmissão em redes LPWAN;
7. Simulação da publicação via MQTT;
8. Exibição das métricas de processamento e comunicação no terminal.

Durante os primeiros ciclos, o dispositivo transmite utilizando **LoRaWAN**. Após falhas consecutivas do gateway, o mecanismo de *failover* realiza automaticamente a migração para a rede **Meshtastic**, garantindo a continuidade da comunicação.

Ao final do sexto ciclo, o sistema exporta automaticamente todos os artefatos produzidos durante a simulação.

---

## 12.5 Arquivos Gerados

Após a conclusão da simulação, o programa cria automaticamente a estrutura abaixo (caso ainda não exista) e salva todos os resultados obtidos durante a execução.

```text
outputs/
│
├── csv/
├── json/
├── maps/
└── reports/
```

Os arquivos recebem automaticamente um **timestamp** em seus nomes para evitar sobrescritas.

Exemplo:

```text
outputs/
│
├── csv/
│   └── simulation_20260716_180736.csv
│
├── json/
│   ├── simulation_20260716_180736.json
│   └── simulation_compact_20260716_180736.json
│
├── maps/
│   └── map_20260716_180736.html
│
└── reports/
    └── statistics_20260716_180736.txt
```

---

## 12.6 Visualizando os Resultados

Após a execução do simulador, os resultados podem ser analisados conforme descrito a seguir.

### Mapa Interativo

1. Acesse a pasta:

```text
outputs/maps/

PS: pode baixar a extenção 'live server' no vscode para facilitar a visualização dos mapas interativos também

```

2. Abra o arquivo `map_*.html` utilizando qualquer navegador de internet (Google Chrome, Microsoft Edge, Mozilla Firefox ou similar).

O mapa apresenta os dispositivos simulados distribuídos geograficamente em Blumenau (SC). Cada marcador é colorido de acordo com o nível de risco calculado pelo sistema. Ao selecionar um marcador, são exibidas informações detalhadas da telemetria correspondente.

---

### Relatório Estatístico

Acesse a pasta:

```text
outputs/reports/
```

Em seguida, abra o arquivo `statistics_*.txt`.

O relatório apresenta um resumo da execução da simulação, incluindo métricas como:

- quantidade de ciclos executados;
- níveis máximo, mínimo e médio da água;
- maior índice pluviométrico registrado;
- quantidade de transmissões realizadas via LoRaWAN e Meshtastic;
- tempo médio de processamento do Edge Node;
- tamanho médio dos payloads;
- percentual médio de redução obtido pela compactação da telemetria.

---

### Arquivos JSON

Os arquivos localizados em

```text
outputs/json/
```

podem ser utilizados para auditoria dos dados produzidos durante a simulação.

São exportadas duas versões:

- **JSON completo**, contendo todas as informações produzidas pelo simulador;
- **JSON compactado**, otimizado para transmissão em redes LPWAN.

---

### Arquivo CSV

O arquivo localizado em

```text
outputs/csv/
```

contém todos os registros da simulação em formato tabular.

Esse arquivo pode ser aberto em ferramentas como:

- Microsoft Excel;
- LibreOffice Calc;
- Google Sheets;
- Power BI;

ou importado diretamente por aplicações desenvolvidas em Python utilizando bibliotecas como **Pandas** para análises adicionais.


# 13. ⚠️ Limitações do MVP e Trabalhos Futuros

O **Americas TechGuard** foi desenvolvido como uma prova de conceito (*Proof of Concept – PoC*) em ambiente **software-only**, permitindo validar a arquitetura híbrida proposta sem a necessidade de hardware físico. Dessa forma, algumas limitações inerentes ao escopo atual devem ser consideradas.

As leituras dos sensores são geradas por cenários determinísticos previamente definidos, não contemplando variações provenientes de dispositivos reais, como ruídos de medição, falhas de sensores, perda de pacotes, interferências eletromagnéticas (RF), atenuação do sinal LoRa ou mudanças ocasionadas pelas condições ambientais.

Além disso, a simulação representa um conjunto reduzido de nós distribuídos geograficamente, não reproduzindo o comportamento de uma rede **Mesh** em larga escala, incluindo aspectos como roteamento *multi-hop* complexo, congestionamento da rede, latência entre múltiplos saltos e diferentes densidades de dispositivos.

Como continuidade do projeto, pretende-se migrar a lógica atualmente implementada em Python para plataformas embarcadas utilizando **ESP32**, **ESP-IDF**, **MicroPython** ou desenvolvimento em **C/C++**, permitindo a execução da aplicação em dispositivos físicos equipados com módulos **LoRa**, como o **Heltec WiFi LoRa 32 V3**.

Entre as principais evoluções previstas destacam-se:

- integração com sensores ultrassônicos reais para monitoramento do nível da água;
- integração com sensores pluviométricos, temperatura e umidade;
- comunicação utilizando rádios LoRa físicos;
- integração com uma rede Meshtastic real;
- conexão com brokers MQTT, como **Mosquitto** ou **EMQX**;
- armazenamento persistente dos dados em banco de dados;
- desenvolvimento de dashboards para monitoramento em tempo real;
- utilização de modelos de aprendizado de máquina para apoio à previsão de enchentes e eventos hidrológicos.

Essas melhorias permitirão aproximar o simulador de um ambiente operacional, ampliando sua aplicabilidade em sistemas reais de monitoramento ambiental e apoio à tomada de decisão.

---

# 14. 🌎 Aplicação Prática no Contexto do Americas TechGuard

Como estudo de caso, adotou-se o município de **Blumenau (SC)**, reconhecido pelo histórico recorrente de enchentes associadas ao Rio Itajaí-Açu. Durante eventos climáticos severos, interrupções no fornecimento de energia elétrica e falhas na infraestrutura de telecomunicações podem comprometer significativamente os sistemas convencionais de monitoramento e emissão de alertas. Nessas situações, a disponibilidade de uma infraestrutura de comunicação resiliente torna-se essencial para garantir a continuidade da transmissão das informações.

A arquitetura híbrida proposta combina a cobertura do **LoRaWAN** em condições normais de operação com a capacidade de auto-organização proporcionada pelo **Meshtastic** quando ocorre indisponibilidade da infraestrutura principal. Dessa forma, mesmo na ausência dos gateways LoRaWAN, os dispositivos continuam compartilhando informações críticas por meio da rede Mesh.

Essa abordagem possibilita a criação de uma infraestrutura descentralizada de comunicação capaz de auxiliar órgãos de monitoramento, equipes da Defesa Civil e comunidades locais, contribuindo para a disseminação contínua de alertas e dados sobre o nível dos rios durante situações de emergência.Embora o presente trabalho tenha caráter acadêmico e demonstrativo, a arquitetura desenvolvida estabelece uma base para futuras implementações em sistemas reais de monitoramento ambiental distribuído e redes resilientes para resposta a desastres naturais.

---

# 15. 🌟 Diferenciais do Projeto

Além dos requisitos previstos para a Atividade 8, o projeto incorpora funcionalidades adicionais voltadas à engenharia de software, arquitetura de sistemas distribuídos e boas práticas de desenvolvimento.

## 15.1 Gerenciamento Inteligente de Comunicação

Foi implementado um mecanismo de **failover** com **debounce**, responsável por monitorar continuamente a disponibilidade do gateway LoRaWAN.

A migração para a rede Meshtastic ocorre apenas após falhas consecutivas, reduzindo trocas desnecessárias de rede e simulando um comportamento mais próximo de ambientes reais.


## 15.2 Otimização de Payload para Redes LPWAN

O componente **TelemetryMinimizer** realiza a compactação automática dos payloads antes da transmissão.

Entre as estratégias empregadas destacam-se:

- conversão de timestamps ISO para Unix Epoch;
- utilização de identificadores abreviados;
- codificação compacta dos níveis de risco;
- redução do tamanho das chaves JSON.

Essa abordagem reduz significativamente o volume de dados transmitidos, tornando a comunicação mais adequada às restrições de largura de banda das redes LPWAN.

## 15.3 Exportação Multiformato e Visualização Geográfica

Ao término da simulação, o sistema exporta automaticamente os resultados em diferentes formatos, facilitando análises posteriores e integração com outras ferramentas.

São gerados automaticamente:

- arquivos **CSV** para análise tabular;
- payloads completos e compactados em **JSON**;
- relatório estatístico em formato texto;
- mapa interativo em **HTML**, desenvolvido com **Folium**, apresentando a distribuição geográfica dos nós simulados e seus respectivos níveis de risco.


## 15.4 Estruturação Profissional do Projeto

O repositório foi organizado seguindo boas práticas de desenvolvimento de software, incluindo:

- arquitetura modular e organizada;
- documentação técnica em Markdown;
- estrutura padronizada de diretórios;
- geração automática dos artefatos da simulação;
- guia completo de instalação, execução e utilização do projeto.


# 16. ⚖️ Licença e Uso Acadêmico

Este projeto foi desenvolvido para fins **acadêmicos**, **científicos** e de **pesquisa**, como parte das atividades do projeto **Americas TechGuard**.

O simulador constitui uma prova de conceito destinada à validação de uma arquitetura híbrida baseada em **LoRaWAN**, **Meshtastic**, **Edge Computing** e comunicação de baixo consumo aplicada ao monitoramento ambiental.

Os conceitos, metodologias e tecnologias empregados fundamentam-se na literatura técnica e científica relacionada a redes LPWAN, comunicação Mesh, Internet das Coisas (IoT) e processamento em borda.

Este software é distribuído sob os termos da **Licença MIT**, permitindo sua utilização, estudo, modificação e redistribuição, desde que sejam preservados os créditos de autoria e os respectivos termos da licença.