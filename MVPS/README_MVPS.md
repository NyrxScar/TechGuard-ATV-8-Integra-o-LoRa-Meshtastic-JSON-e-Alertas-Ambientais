# Americas TechGuard | MVP 2
## Simulação de Arquitetura Híbrida LoRaWAN + Meshtastic

Este MVP implementa uma **prova de conceito (Proof of Concept - PoC)** da arquitetura híbrida proposta para o projeto **Americas TechGuard**, simulando um sistema de monitoramento de inundações baseado em processamento local (Edge Computing), comunicação resiliente e transmissão otimizada para redes LPWAN.

---
# Sobre o Aproveitamento técnico referente as Referências Técnicas:

A fundamentação deste sistema baseia-se diretamente em duas pesquisas científicas de ponta:

**Artigo Principal (Monitoramento e Alerta LoRaWAN):** Development of a smart sensing unit for LoRaWAN-based IoT flood monitoring and warning system in catchment areas (2023).

**Aproveitamento técnico:** Conceito de monitoramento de bacias de captação, correlação matemática entre nível de água (sensor ultrassônico) e chuva acumulada (pluviômetro) e a estruturação de um motor local de risco de inundação.

**Artigo Complementar (Redes Mesh e Meshtastic):** A Meshtastic-based LoRa Mesh System for Smart Campus Applications: From Solar-Powered Sensing to Containerized Data Management (arXiv, 2026).*

**Aproveitamento técnico:** Topologia de rede mesh descentralizada para replicação de dados por saltos (hops), permitindo que nós isolados usem seus vizinhos para alcançar a infraestrutura ativa.

---

# Objetivo

Validar, por meio de uma simulação determinística, o funcionamento de um nó inteligente capaz de:

- simular sensores ambientais;
- processar dados localmente (Edge Computing);
- classificar automaticamente o nível de risco;
- gerar payloads JSON padronizados;
- validar os dados antes da transmissão;
- selecionar automaticamente entre LoRaWAN e Meshtastic;
- realizar failover da comunicação;
- otimizar o payload para redes LPWAN;
- simular a publicação MQTT.

---

# Funcionalidades Implementadas

O MVP implementa:

- Simulação determinística de sensores ambientais;
- Motor de classificação de risco (Risk Engine);
- Construção de payload JSON enriquecido;
- Validação dos campos obrigatórios;
- Gerenciador de comunicação híbrida;
- Failover automático entre LoRaWAN e Meshtastic;
- Compressão de telemetria para redes LPWAN;
- Simulação de publicação MQTT;
- Exibição de métricas de comunicação e processamento no terminal.

---

# Arquitetura da Simulação

```
Sensores Simulados
        │
        ▼
Edge Computing
(Risk Engine)
        │
        ▼
Construção do Payload
        │
        ▼
Communication Manager
        │
        ├───────────────┐
        │               │
        ▼               ▼
     LoRaWAN      Meshtastic
        │               │
        └───────┬───────┘
                ▼
         MQTT (Simulado)
                │
                ▼
      Saída no Terminal
```

---

# Cenário Simulado

A simulação representa a evolução de um evento hidrológico ao longo de **seis ciclos consecutivos**.

| Ciclo | Situação |
|--------|----------|
| 1 | Condições normais |
| 2 | Chuva moderada |
| 3 | Elevação do nível da água |
| 4 | Situação crítica |
| 5 | Falha inicial do Gateway |
| 6 | Segunda falha consecutiva e failover para Meshtastic |

Essa sequência permite demonstrar o comportamento do sistema em condições normais e durante um cenário de desastre.

---

# Métricas de Risco

O processamento é realizado localmente através do **Risk Engine**, responsável por classificar o nível de risco com base na altura da água.

| Nível da Água | Classificação |
|---------------|---------------|
| < 1,0 m | Seguro |
| 1,0 – 1,99 m | Atenção |
| 2,0 – 2,99 m | Alerta |
| ≥ 3,0 m | Crítico |

Cada classificação gera automaticamente uma mensagem de alerta correspondente.

---

# Comunicação Híbrida

O sistema possui um **Communication Manager**, responsável por decidir qual arquitetura utilizar.

## Operação Normal

Enquanto o gateway permanece disponível, a comunicação utiliza o modo **LoRaWAN**.

```
Sensor
   │
Gateway
   │
MQTT
```
## Operação em Contingência

Após duas falhas consecutivas do gateway, ocorre automaticamente o failover para **Meshtastic**.

```
Sensor
   │
Rede Mesh
   │
Nós vizinhos
```

Esse mecanismo evita mudanças constantes entre as arquiteturas de comunicação.

---

# Failover

Foi implementado um mecanismo de **Debounce Temporal** para evitar alternâncias indevidas entre LoRaWAN e Meshtastic.

Funcionamento:

| Ciclo | Gateway | Rede Utilizada |
|--------|----------|----------------|
|1|Online|LoRaWAN|
|2|Online|LoRaWAN|
|3|Online|LoRaWAN|
|4|Online|LoRaWAN|
|5|Offline (1ª falha)|LoRaWAN|
|6|Offline (2ª falha)|Meshtastic|

ps: O failover somente ocorre após duas falhas consecutivas

# Payload JSON

Cada leitura gera um payload contendo informações do dispositivo, sensores, comunicação e processamento.

Campos obrigatórios:

- device_id
- timestamp
- latitude
- longitude
- sensor_type
- sensor_value
- unit
- risk_level
- alert_message
- source

Campos adicionais implementados:

- message_id
- simulation
- firmware_version
- schema_version
- rain_mm
- temperature_c
- humidity_pct
- battery_percent
- gateway_available
- network_mode
- mesh_hops
- signal_rssi
- signal_snr
- processing_time_ms

---

# Compressão LPWAN

Antes da transmissão simulada, o payload completo é convertido para um formato reduzido contendo apenas os dados essenciais para comunicação por rádio.

Exemplo de payload compactado:

```json
{
    "id": "NODE_FLORIPA_001",
    "ts": 1784160000,
    "wl": 3.2,
    "rn": 52.8,
    "tp": 19.0,
    "hm": 98,
    "bt": 95,
    "rk": "CR",
    "nt": "LW"
}
```

Durante a execução são exibidos:

- tamanho do payload original;
- tamanho do payload compactado;
- percentual de redução obtido.

---

# MQTT (Simulado)

Após a seleção da arquitetura de comunicação, o sistema simula a publicação do payload em um broker MQTT.

Tópicos simulados:

```
americas-techguard/lorawan/NODE_FLORIPA_001/telemetry
```

ou

```
americas-techguard/meshtastic/NODE_FLORIPA_001/alerts
```

Nesta etapa, a publicação é apenas simulada, sendo utilizada para demonstrar o fluxo de comunicação da arquitetura proposta.

---

#  Como Executar

Execute o arquivo principal:

```bash
Entre na pasta MVPS: cd MVPS
Execute o programa: python mvp2.py
```

Durante a execução serão exibidas informações como:

- status do gateway;
- arquitetura selecionada;
- nível de risco;
- métricas RSSI e SNR;
- número de Mesh Hops;
- tempo de processamento;
- payload original;
- payload compactado;
- percentual de compressão.

<p align="center">
  <img src="/MVPS/assets/Saída do MVP2.png" alt="Saída do MVP2" height="400">
  &nbsp;&nbsp;&nbsp;
  <img src="/MVPS/assets/Saída do MVP26.png" alt="Saída do MVP26" height="400">
</p>

---

# Tabela Comparativa da Evolução da Arquitetura: MVP 1 × MVP 2

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

---
# Limitações do MVP

Este MVP possui caráter acadêmico e representa uma prova de conceito.

Nesta versão:

- os sensores são simulados;
- não existe hardware LoRa;
- não existe Gateway LoRaWAN físico;
- não existe dispositivo Meshtastic real;
- a publicação MQTT é simulada;
- toda a interação ocorre através do terminal.

