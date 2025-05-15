// acceso_leds_nano33iot.ino
const uint8_t LED_VERDE = 10;   // cámbialo a LED_BUILTIN (13) si lo prefieres
const uint8_t LED_ROJO  = 9;

void setup() {
  pinMode(LED_VERDE, OUTPUT);
  pinMode(LED_ROJO,  OUTPUT);
  Serial.begin(115200);         // USB CDC
  while (!Serial) ;             // espera a que abra el puerto
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();
    if (c == '1') {                         // acceso correcto
      digitalWrite(LED_VERDE, HIGH);
      digitalWrite(LED_ROJO,  LOW);
      Serial.println("LED verde ON");
    }
    else if (c == '0') {                    // acceso denegado
      digitalWrite(LED_VERDE, LOW);
      digitalWrite(LED_ROJO,  HIGH);
      Serial.println("LED rojo ON");
    }
  }
}
