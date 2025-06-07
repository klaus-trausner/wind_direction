from machine import Pin, SoftI2C, UART, WDT
import ssd1306
from time import sleep
from dht import DHT22
import wlan
import mqtt
import wind
import gc


# You can choose any other combination of I2C pins
i2c = SoftI2C(scl=Pin(17, Pin.PULL_UP), sda=Pin(
    16, Pin.PULL_UP), freq=400000, timeout=1000)

led = Pin(5, Pin.OUT)

oled_width = 128
oled_height = 64
i2c_devices = i2c.scan()
if i2c_devices:
    print("I2C Address      : "+hex(i2c_devices[0]).upper())
else:
    print("No I2C devices found!")
    # Hier ggf. Programm anhalten oder Fehlerbehandlung
sleep(5)
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

dht22 = DHT22(Pin(15, Pin.IN, Pin.PULL_UP))

wlan.wlanConnect()

# Watchdog initialisieren (z.B. 8 Sekunden Timeout)
wdt = WDT(timeout=8000)

# Continuous reading loop


def read_registers():
    try:
        print('Reading qty={} from starting address {}:'.format(
            wind.qty, wind.starting_address))

        # Read holding registers from the slave device
        values = wind.read_registers()

        # Print the result
        print('Result: {}'.format(values))
        return values

    except Exception as e:
        print('An error occurred:', e)
        return (None, -1)


    # Connect to MQTT broker, start MQTT client
client = mqtt.connect_mqtt()

# Publish as MQTT payload
mqtt.publish_mqtt(client, "test", "Greeting from Pico")

sleep(0.5)

while True:
    wdt.feed()  # Watchdog füttern

    oled.fill(0)
    oled.text('My Home!', 0, 0)
    led.value(not led.value())
    # oled.framebuf.rect(0,35,70,20,0,True)
    client.check_msg()
    try:
        dht22.measure()

        temperatur = dht22.temperature()
        humidity = dht22.humidity()
        oled.text(f"Temp: {temperatur}", 0, 20)
        oled.text(f"Hum : {humidity}", 0, 30)
        print(temperatur, humidity)
        mqtt.publish_mqtt(client, "ext2/temperature", f"{temperatur}")
        mqtt.publish_mqtt(client, "ext2/humidity", f"{humidity}")
    except OSError as e:
        print("failed to read dht-sensor.", OSError(), e)

    wind_direction = read_registers()
    i = 0
    if wind_direction[0] is not None:
        i = int(wind_direction[0])
    else:
        i = -1

    cd = wind.Corresponding_direction.get(i, "??")  # Sicherere Abfrage
    mqtt.publish_mqtt(client, "wind_dir", f"{wind_direction[1]}, {cd}")
    oled.text(f"Dir : {wind_direction[1]}, {cd}", 0, 40)
    oled.show()

    gc.collect()  # Garbage Collection durchführen
    # print(f"Free memory: {gc.mem_free()} bytes") # Optional für Debugging
    sleep(3)
