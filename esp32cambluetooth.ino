#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>
#include "BluetoothSerial.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"

// Configuración de red WiFi
const char* WIFI_SSID = "RAMARO2021";
const char* WIFI_PASS = "51228131RRM@";

// Configuración del servidor web y Bluetooth
WebServer server(80); // servidor web en el puerto 80
BluetoothSerial SerialBT; // para comunicación Bluetooth
const char* btDeviceName = "ESP32CAM";

// Resoluciones de cámara
static auto loRes = esp32cam::Resolution::find(320, 240); // baja resolución
static auto hiRes = esp32cam::Resolution::find(800, 600); // alta resolución

// Dirección MAC del dispositivo Bluetooth preferido (reemplaza con la real)
const char* preferredDeviceAddress = "43:42:79:BD:00:00"; 

// Ruta de la API para la recepción de audio
const char* AUDIO_PATH = "/audio";

// Función para capturar imagen y enviarla
void serveJpg() {
  auto frame = esp32cam::capture();
  if (frame == nullptr) {
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));

  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);  // enviar imagen al cliente
}

// Función para capturar imagen en baja resolución
void handleJpgLo() {
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");
  }
  serveJpg();
}

// Función para capturar imagen en alta resolución
void handleJpgHi() {
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}

// Función para manejar la recepción de audio vía HTTP
void handleAudioUpload() {
  if (server.hasArg("plain")) {
    String audioData = server.arg("plain");

    // Enviar audio recibido al dispositivo Bluetooth
    SerialBT.write((uint8_t*)audioData.c_str(), audioData.length());
    
    // Confirmar recepción
    server.send(200, "text/plain", "Audio recibido y enviado por Bluetooth.");
  } else {
    server.send(400, "text/plain", "No se recibió audio.");
  }
}

// Función para conectarse al dispositivo Bluetooth
bool connectToBluetoothDevice(const char* targetAddress) {
  if (SerialBT.connect(targetAddress)) {
    Serial.print("Conectado a dispositivo Bluetooth con MAC: ");
    Serial.println(targetAddress);
    return true;
  } else {
    Serial.print("No se pudo conectar a dispositivo con MAC: ");
    Serial.println(targetAddress);
    return false;
  }
}


// Escaneo y conexión Bluetooth
void scanAndConnectBluetooth() {
  
  

  Serial.println("Escaneando dispositivos Bluetooth...");

  // No es posible escanear dispositivos directamente usando BluetoothSerial,
  // pero puedes intentar conectar directamente si conoces la dirección MAC:
  String deviceAddress = "41:42:79:BD:00:00"; // Dirección MAC del dispositivo a conectar
  bool connected = SerialBT.connect(deviceAddress.c_str());

  if (connected) {
    Serial.println("Conectado a " + deviceAddress);
  } else {
    Serial.println("No se pudo conectar a " + deviceAddress);
  }
  Serial.println("No se pudo conectar a ningún dispositivo Bluetooth.");
  }

  


// Configuración inicial
void setup() {
  Serial.begin(115200);

  // Conectar a WiFi
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Conectado a WiFi. Dirección IP: ");
  Serial.println(WiFi.localIP());

  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/cam-lo.jpg");//para conectarnos IP res baja

  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/cam-hi.jpg");//pa

  // Iniciar servidor web
  server.on("/cam-lo.jpg", handleJpgLo);  // enviar imagen en baja resolución
  server.on("/cam-hi.jpg", handleJpgHi);  // enviar imagen en alta resolución
  server.on(AUDIO_PATH, HTTP_POST, handleAudioUpload);  // recibir audio vía HTTP
  server.begin();

  // Configurar Bluetooth
  if (!SerialBT.begin(btDeviceName)) {
    Serial.println("Error al iniciar Bluetooth.");
  } else {
    Serial.println("Bluetooth iniciado. Escaneando y conectando...");
    scanAndConnectBluetooth(); // Escanear y conectar al dispositivo Bluetooth
  }

  // Configurar la cámara
  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);

    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMARA OK" : "CAMARA FAIL");
  }
  SerialBT.begin("ESP32CAM"); // Nombre del dispositivo Bluetooth
  Serial.println("El Bluetooth está listo para emparejarse"); 
}

// Bucle principal
void loop() {
  server.handleClient();  // manejar solicitudes HTTP entrantes

  // Manejar la conexión Bluetooth (si es necesario)
  if (SerialBT.hasClient()) {
    Serial.println("Dispositivo Bluetooth conectado.");
  }
  scanAndConnectBluetooth();
  delay(10000);
}
