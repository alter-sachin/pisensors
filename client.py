import time
import board
import adafruit_dht
import threading
import requests


def temperature_sensor():
    global temperature_value_c,temperature_value_f
    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT22(board.D18)

    # you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
    # This may be necessary on a Linux single board computer like the Raspberry Pi,
    # but it will not work in CircuitPython.
    # dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)

    while True:
        try:
            # Print the values to the serial port
            temperature_c = dhtDevice.temperature
            temperature_f = temperature_c * (9 / 5) + 32
            humidity = dhtDevice.humidity
            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )
            temperature_value_c,temperature_value_f= str(temperature_c),str(temperature_f)

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count


def light_sensor():
    global light_value
    #Catch when script is interrupted, cleanup correctly
    try:
        # Main loop
        while True:
            print(rc_time(pin_to_circuit))
            light_value = rc_time(pin_to_circuit)
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()



if __name__ == "__main__":
# creating thread
    t1 = threading.Thread(target=temperature)
    t2 = threading.Thread(target=light_sensor)
    #t3= threading.Thread(target=send_values)
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
    while True:
        r = requests.post("http://127.0.0.1:8000", data={'temperature_value_c': temperature_value_c,
            'temperature_value_f': temperature_value_f,
         'light_value': light_value})
        time.sleep(10)

    # both threads completely executed
    print("Done!")
