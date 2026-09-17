import requests, time, random

SERVER = "http://192.168.1.100:5000"   # <-- change to the server's IP

print(f"Sending to {SERVER}")
while True:
    temp = 20 + random.random() * 10
    try:
        requests.post(f"{SERVER}/api/sensor", json={"temp": temp}, timeout=2)
        print(f"sent {temp:.1f}°C")
    except Exception as e:
        print(f"error: {e}")
    time.sleep(2)