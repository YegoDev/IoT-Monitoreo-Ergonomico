from machine import Pin, ADC, SoftI2C
from imu import MPU6050
import math
import time

# ── Configuración de pines ──────────────────────────────
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c)
fsr = ADC(Pin(34))
fsr.atten(ADC.ATTN_11DB)

# ── Constantes ──────────────────────────────────────────
UMBRAL_PRESION = 200
INTERVALO_SEG  = 30
tiempo_sentado = 0

# ── Funciones ───────────────────────────────────────────
def calcular_angulo(mpu):
    ax = mpu.accel.x
    ay = mpu.accel.y
    az = mpu.accel.z
    angulo = math.degrees(math.atan2(ay, math.sqrt(ax**2 + az**2)))
    return round(angulo, 1)

def leer_presion():
    return fsr.read()

def esta_ocupado(presion):
    return presion > UMBRAL_PRESION

# ── Bucle principal ──────────────────────────────────────
print("=" * 55)
print("  NODO SENSOR - MONITOREO ERGONOMICO")
print("=" * 55)
print(f"{'Timestamp':<12} {'Angulo':>8} {'Presion':>8} {'Ocupado':>8} {'T.Sentado':>10}")
print("-" * 55)

registro = 0
while True:
    angulo  = calcular_angulo(mpu)
    presion = leer_presion()
    ocupado = esta_ocupado(presion)

    if ocupado:
        tiempo_sentado += INTERVALO_SEG / 60
    else:
        tiempo_sentado = 0

    ts = time.localtime()
    timestamp = f"{ts[3]:02}:{ts[4]:02}:{ts[5]:02}"

    print(f"{timestamp:<12} {angulo:>7}° {presion:>8} {'SI' if ocupado else 'NO':>8} {tiempo_sentado:>8.1f} min")

    registro += 1
    time.sleep(INTERVALO_SEG)