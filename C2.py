
"""
Reconocimiento facial → LED verde/rojo en Arduino Nano 33 IoT

"""

import time
import cv2
import serial
import serial.tools.list_ports as list_ports
from pathlib import Path

# ──────────────── CONFIGURACIÓN BÁSICA ─────────────────
BAUD       = 115200              
CAMERA_ID  = 0                   # 0 = webcam integrada
CASCADE    = Path(__file__).with_name("haarcascade_frontalface_default.xml")
PORT       = None
# ────────────────────────────────────────────────────────


def detect_arduino_port() -> str | None:
    """Devuelve el primer puerto que contenga la palabra 'Arduino'."""
    for p in list_ports.comports():
        if "Arduino" in p.description or "Nano" in p.description:
            return p.device
    return None


def main() -> None:
    # 1. Resolver el puerto
    global PORT
    if PORT is None:
        PORT = detect_arduino_port()
        if PORT is None:
            raise SystemExit("[ERROR] No se encontró un puerto Arduino. "
                             "Conéctalo y, si es necesario, fija PORT manualmente.")

    # 2. Abrir Serial
    try:
        ser = serial.Serial(PORT, BAUD, timeout=1)
        time.sleep(2)  # el Nano 33 IoT se reinicia al abrir CDC
        print(f"[INFO] Puerto {PORT} abierto a {BAUD} bps")
    except serial.SerialException as e:
        raise SystemExit(f"[ERROR] No se pudo abrir {PORT}: {e}")

    # 3. Cargar Haar Cascade
    if not CASCADE.exists():
        raise SystemExit(f"[ERROR] No existe el archivo {CASCADE}.")
    face_cascade = cv2.CascadeClassifier(str(CASCADE))
    if face_cascade.empty():
        raise SystemExit("[ERROR] Error al cargar el clasificador Haar Cascade")

    # 4. Abrir cámara
    cap = cv2.VideoCapture(CAMERA_ID)
    if not cap.isOpened():
        raise SystemExit("[ERROR] No se pudo abrir la cámara")

    print("[INFO] ESC para salir")
    last_state = None

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                continue

            gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.2, minNeighbors=5, minSize=(80, 80)
            )

            state = '1' if len(faces) else '0'
            if state != last_state:
                ser.write(state.encode())
                print("acceso correcto" if state == '1' else "acceso denegado")
                last_state = state

            # Dibujar rectángulos (solo demo)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            cv2.imshow("Face Access – Nano 33 IoT", frame)
            if cv2.waitKey(1) & 0xFF == 27:   # ESC
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        ser.close()
        print("[INFO] Cerrado correctamente")


if __name__ == "__main__":
    main()
