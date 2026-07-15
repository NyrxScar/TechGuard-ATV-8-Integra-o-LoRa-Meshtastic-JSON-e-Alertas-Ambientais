# Americas TechGuard | ATIVIDADE PROPOSTA 8 - Integração LoRa-Meshtastic, JSON e Alertas Ambientais

**Estudante:** Nyrx Oliveira de Aquino Farias  
**Eixo:** Sistemas Embarcados | LoRa, Meshtastic, LoRaWAN, JSON, IoT, Integração de Dados e Alertas Ambientais  
**Período:** ATIVIDADE 8 | 08/07/2026 até 18/07/2026  
**Docentes:** Valério Piana, Lucas Lacerda e Alex Salazar  
**Entrega:** Trilha B - Software-only / Simulação

---
## Sobre o Projeto

Este repositório apresenta uma simulação em software de uma arquitetura IoT resiliente para monitoramento ambiental e emissão de alertas móveis, desenvolvida como parte da Atividade 8 do projeto Americas TechGuard.

A solução implementa uma cadeia completa de processamento de dados, desde a simulação de sensores ambientais até a geração de payloads JSON, classificação de risco, seleção da arquitetura de comunicação (LoRaWAN ou Meshtastic), publicação via MQTT e visualização dos dados em dashboard.

O projeto foi desenvolvido na modalidade Software-only, permitindo a reprodução completa da solução sem a necessidade de hardware físico.

---

## Objetivos

- Simular sensores ambientais.
- Construir payloads JSON padronizados.
- Validar mensagens.
- Classificar automaticamente o risco.
- Simular comunicação LoRa/Meshtastic.
- Utilizar MQTT para integração.
- Demonstrar uma arquitetura híbrida resiliente.
- Registrar dados para análise.
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

---

## 5. 📝 Modelagem de Dados: Exemplo de Estrutura do Payload JSON com os Rquisitos Mínimos Exigidos pelos Orientadores

O payload utilizado pelo simulador foi modelado estritamente para representar a leitura de dados ambientais, estado do risco e avisos direcionados aos cidadãos através da rede móvel Meshtastic:

### Exemplo de Entrada do Cenário A: Condição Segura (Safe) e Gateway Disponível (LoRaWAN):
```json
{
  "device_id": "NODE_FLORIPA_001",
  "timestamp": "2026-07-15T14:30:00Z",
  "latitude": -27.5954,
  "longitude": -48.5480,
  "sensor_type": "ultrasonic_level",
  "sensor_value": 0.45,
  "unit": "m",
  "risk_level": "SAFE",
  "alert_message": "Nivel dentro da normalidade.",
  "network_mode": "LoRaWAN",
  "gateway_active": true,
  "mesh_hops": 0,
  "battery_percent": 98,
  "signal_rssi": -75,
  "signal_snr": 9.5
}

```
### Exemplo de Entrada do Cenário B: Alerta de Desastre Off-Grid via Meshtastic (Risco: CRITICAL):
```json

{
  "device_id": "NODE_FLORIPA_001",
  "timestamp": "2026-07-15T14:35:12Z",
  "latitude": -27.5954,
  "longitude": -48.5480,
  "water_level_m": 3.25,
  "rain_mm": 45.8,
  "temperature_c": 19.2,
  "humidity_pct": 95,
  "risk_level": "CRITICAL",
  "alert_message": "ALERTA: Risco iminente de enchente! Transbordo detectado.",
  "gateway_available": false,
  "network_mode": "Meshtastic",
  "mesh_hops": 2,
  "battery_percent": 84,
  "signal_rssi": -114,
  "signal_snr": -4.1
}