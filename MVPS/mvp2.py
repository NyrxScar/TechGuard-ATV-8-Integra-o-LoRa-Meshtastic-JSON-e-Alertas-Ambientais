import json
import time
import uuid
from datetime import datetime, timezone

# MVP - Arquitetura Híbrida LoRaWAN + Meshtastic - Software-only Simulation with Deterministic Scenario

### Importações e Configurações Globais do Dispositivo

DEVICE_ID = "NODE_FLORIPA_001"
LATITUDE = -27.5954
LONGITUDE = -48.5480
SCHEMA_VERSION = "1.0.0"
FIRMWARE_VERSION = "1.2.4"


# 1. Hardware layer (Simulação dos sensores)
# Simula a leitura física dos sensores ambientais e acompanha a progressão de uma tempestade real ao longo dos ciclos.

def read_simulated_sensors(cycle_num):

    # Mapeamento do cenário para construir a narrativa lógica do desastre
    scenarios = {
        1: {"water_level": 0.6, "rain": 0.0, "temperature": 24.5, "humidity": 65, "battery": 100},
        2: {"water_level": 1.4, "rain": 12.5, "temperature": 22.1, "humidity": 80, "battery": 98},
        3: {"water_level": 2.2, "rain": 34.0, "temperature": 20.3, "humidity": 92, "battery": 96},
        4: {"water_level": 3.2, "rain": 52.8, "temperature": 19.0, "humidity": 98, "battery": 95},
        5: {"water_level": 3.5, "rain": 55.0, "temperature": 18.5, "humidity": 98, "battery": 94},
        6: {"water_level": 3.6, "rain": 55.0, "temperature": 18.2, "humidity": 98, "battery": 92}
    }
    return scenarios.get(cycle_num, scenarios[1])


# 2. Edge computing (Lógina Local)
# Motor de classificação de risco executado na borda (Edge Node).

class RiskEngine:

    @staticmethod
    def classify(water_level):
        if water_level < 1.0:
            return "Seguro", "Nível da água dentro da normalidade."
        elif water_level < 2.0:
            return "Atenção", "Elevação gradual do nível da água."
        elif water_level < 3.0:
            return "Alerta", "Possibilidade de transbordamento."
        return "Crítico", "Risco iminente de inundação."


# 3. Gerenciador de comunicação (Failover Ativo)
# Gerencia a conectividade do dispositivo de borda e Prioriza LoRaWAN e chaveia para o Meshtastic após falhas consecutivas do Gateway.

class CommunicationManager:

    def __init__(self):
        self.failures = 0

    def select_network(self, gateway_available):
        if gateway_available:
            self.failures = 0
            return "LoRaWAN"

        # Incrementa contador de falhas consecutivas quando o Gateway falha
        self.failures += 1

        # Mecanismo de Debounce: Chaveia para Mesh apenas no segundo ciclo de falhas
        if self.failures >= 2:
            return "Meshtastic"

        return "LoRaWAN"


# 4. Otimização de Telemetria para Rádio (LPWAN)

class TelemetryMinimizer:
    # Compacta o JSON completo para transmissão em redes de baixo consumo e banda reduzida.
    
    RISK_CODES = {
        "Seguro": "SG",
        "Atenção": "AT",
        "Alerta": "AL",
        "Crítico": "CR"
    }

    @staticmethod
    def compress(payload):
        # Otimização extrema do timestamp: ISO string convertido em Epoch Unix Time (4 bytes no hardware)
        dt_str = payload["timestamp"].replace("Z", "+00:00")
        epoch_time = int(datetime.fromisoformat(dt_str).timestamp())

        return {
            "id": payload["device_id"],
            "ts": epoch_time,
            "wl": payload["sensor_value"],  # Nível de água consolidado
            "rn": payload["rain_mm"],
            "tp": payload["temperature_c"],
            "hm": payload["humidity_pct"],
            "bt": payload["battery_percent"],
            "rk": TelemetryMinimizer.RISK_CODES[payload["risk_level"]],
            "nt": "LW" if payload["network_mode"] == "LoRaWAN" else "MT"
        }


# 5. Construtor de payloads
# Consolida as leituras e gera o payload original enriquecido.
# Configura o cenário de rede correspondente a cada fase do desastre.

def build_payload(cycle_num, sensor_data, comm_manager):
    start = time.perf_counter()
    message_id = str(uuid.uuid4())

    # Orquestração determinística do estado da rede por ciclo
    if cycle_num <= 4:
        gateway_available = True
        # RSSI degrada conforme a chuva piora
        rssi_steps = {1: -75, 2: -85, 3: -105, 4: -115}
        rssi = rssi_steps[cycle_num]
        snr = round(10.0 - (cycle_num * 3), 1)
    else:
        # Gateway cai fisicamente a partir do Ciclo 5
        gateway_available = False
        rssi = -120
        snr = -12.0

    # Lógicas do processamento de borda e seleção de rede
    risk, message = RiskEngine.classify(sensor_data["water_level"])
    network = comm_manager.select_network(gateway_available)

    # Simulação da contagem de hops da topologia Mesh
    mesh_hops = 2 if network == "Meshtastic" else 0

    # Geração do timestamp robusto (padrão Python 3.12+)
    timestamp_utc = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    payload = {
        "schema_version": SCHEMA_VERSION,
        "firmware_version": FIRMWARE_VERSION,
        "simulation": True,
        "message_id": message_id,
        "device_id": DEVICE_ID,
        "timestamp": timestamp_utc,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "sensor_type": "ultrasonic_level",
        "sensor_value": sensor_data["water_level"],  # Mantido apenas sensor_value para evitar redundâncias
        "unit": "m",
        "rain_mm": sensor_data["rain"],
        "temperature_c": sensor_data["temperature"],
        "humidity_pct": sensor_data["humidity"],
        "risk_level": risk,
        "alert_message": message,
        "source": network,
        "network_mode": network,
        "gateway_available": gateway_available,
        "mesh_hops": mesh_hops,
        "battery_percent": sensor_data["battery"],
        "signal_rssi": rssi,
        "signal_snr": snr
    }

    payload["processing_time_ms"] = round(
        (time.perf_counter() - start) * 1000, 3
    )

    return payload


# 6. Validação de contrato (Edge Security)
# Garante que nenhum dado essencial esteja ausente ou nulo.

def validate(payload):
    required = [
        "device_id",
        "timestamp",
        "latitude",
        "longitude",
        "sensor_type",
        "sensor_value",
        "unit",
        "risk_level",
        "alert_message",
        "source"
    ]

    for field in required:
        if field not in payload or payload[field] is None:
            raise ValueError(
                f"Contrato violado! Campo obrigatório ausente ou nulo: '{field}'"
            )


# 7. Exposição / Publicação (MQTT Simulator)
# Simula a transmissão MQTT adaptando os tópicos e aplicando compressão de rádio.

def publish(payload):
    if payload["network_mode"] == "LoRaWAN":
        topic = f"americas-techguard/lorawan/{DEVICE_ID}/telemetry"
    else:
        topic = f"americas-techguard/meshtastic/{DEVICE_ID}/alerts"

    compact = TelemetryMinimizer.compress(payload)

    # Métricas de análise de compressão
    original_size = len(json.dumps(payload).encode("utf-8"))
    compact_size = len(json.dumps(compact).encode("utf-8"))
    reduction = 100 * (1 - compact_size / original_size)

    # Exposição amigável e legível para a banca avaliadora
    print(f"Device............... {payload['device_id']} (Firmware: {payload['firmware_version']})")
    print(f"Gateway Status....... {'ONLINE' if payload['gateway_available'] else 'OFFLINE (Falha de Comunicação)'}")
    print(f"Network Selection.... {payload['network_mode']}")
    print(f"Mesh Hops............ {payload['mesh_hops']}")
    print(f"Signal Integrity..... RSSI: {payload['signal_rssi']} dBm | SNR: {payload['signal_snr']} dB")
    print(f"Local Risk Engine.... {payload['risk_level']} -> {payload['alert_message']}")
    print(f"MQTT Target Topic.... {topic}")
    print(f"Edge Processing...... {payload['processing_time_ms']} ms")
    print(f"Payload Original..... {original_size} bytes")
    print(f"Payload Compactado... {compact_size} bytes (Redução de {reduction:.1f}%)")

    print("\n[DEBUG] JSON COMPACTADO ENVIADO VIA RÁDIO:")
    print(json.dumps(compact, indent=4, ensure_ascii=False))


# Execução do fluxo do sistema

manager = CommunicationManager()

print("\n")
print("=" * 70)
print("             AMERICAS TECHGUARD - SIMULADOR HÍBRIDO IoT             ")
print("=" * 70)

for cycle in range(1, 7):
    print("\n" + "-" * 70)
    print(f"                             CICLO {cycle}                             ")
    print("-" * 70)

    # 1. Hardware: Leitura dos sensores
    sensor_data = read_simulated_sensors(cycle)

    # 2. Edge / Decision Layer: Construção e decisão da melhor rede
    payload = build_payload(cycle, sensor_data, manager)

    # 3. Security Check: Validação
    validate(payload)

    # 4. Ingest / Network layer: Publicação
    publish(payload)

    time.sleep(2)

print("\n" + "-" * 70)
print("Simulação finalizada com sucesso. Failover operacional demonstrado!\n")