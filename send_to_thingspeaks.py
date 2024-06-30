import dht
import machine
import network
import urequests
import time

# Replace with your Wi-Fi credentials
SSID = 'YOUR SSID'
PASSWORD = 'YOUR PASSWORD'

# ThingSpeak API parameters
API_KEY = 'API_KEY'
THINGSPEAK_URL = 'Api_Key_url'

# DHT11 sensor connected to GPIO 4 (D2)
dht_pin = machine.Pin(5)
dht_sensor = dht.DHT11(dht_pin)

# Function to connect to Wi-Fi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('Network connected:', wlan.ifconfig())

# Function to read data from DHT11
def read_dht11():
    dht_sensor.measure()
    temp = dht_sensor.temperature()
    hum = dht_sensor.humidity()
    return temp, hum

# Function to send data to ThingSpeak
def send_to_thingspeak(temp, hum):
    response = urequests.get(f'{THINGSPEAK_URL}?api_key={API_KEY}&field1={temp}&field2={hum}')
    print(response.text)
    response.close()

# Connect to Wi-Fi
connect_wifi(SSID, PASSWORD)

# Main loop to read and send data every 15 seconds
while True:
    try:
        temperature, humidity = read_dht11()
        print(f'Temperature: {temperature}°C, Humidity: {humidity}%')
        send_to_thingspeak(temperature, humidity)
    except Exception as e:
        print('Error:', e)
    time.sleep(10)
