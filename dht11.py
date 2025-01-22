import adafruit_dht
import board
import websocket
import json
import time

# Inisialisasi sensor DHT11 pada pin GPIO
dht_device = adafruit_dht.DHT11(board.D4)  # Gunakan GPIO 4

# URL WebSocket server
WEBSOCKET_URL = "wss://e-mon.rsudrsoetomo.jatimprov.go.id/ws_monitoring_suhu/"  #URL server WebSocket

# Fungsi untuk membaca data dari DHT11
def read_dht11():
    try:
        # Baca data dari DHT11
        temperature = dht_device.temperature
        humidity = dht_device.humidity

        # Pastikan data tidak kosong
        if temperature is not None and humidity is not None:
            return {"temperature": temperature, "humidity": humidity}
        else:
            return None
    except RuntimeError as error:
        print(f"RuntimeError: {error}")
        return None

# Fungsi untuk mengirim data ke WebSocket
def send_data_to_websocket():
    try:
        # Membuka koneksi WebSocket
        ws = websocket.create_connection(WEBSOCKET_URL)
        print("Connected to WebSocket server!")

        # Loop untuk membaca dan mengirim data
        while True:
            # Baca data dari DHT11
            sensor_data = read_dht11()

            # Jika data berhasil dibaca, kirim ke WebSocket
            if sensor_data:
                ws.send(json.dumps(sensor_data))
                print(f"Sent data: {sensor_data}")
            else:
                print("Data not available")

            # Tunggu 2 detik sebelum pembacaan berikutnya
            time.sleep(2)

    except KeyboardInterrupt:
        print("Program dihentikan.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Pastikan koneksi WebSocket dan sensor dilepas saat program selesai
        ws.close()
        dht_device.exit()
        print("WebSocket connection closed.")
        print("Sensor closed.")

# Program utama
if __name__ == "__main__":
    send_data_to_websocket()
