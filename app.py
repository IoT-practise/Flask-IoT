from flask import Flask, request, jsonify, render_template_string
import time

app = Flask(__name__)

readings = []
led_state = "off"
last_seen = 0

DASHBOARD = """
<!DOCTYPE html>
<html>
<head>
  <title>IoT Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui; text-align: center; padding: 2rem; background:#111; color:#eee; }
    h1 { font-size: 1.4rem; }
    #temp { font-size: 4rem; font-weight: bold; color: #4ade80; }
    button { font-size: 1.2rem; padding: 1rem 2rem; margin: 0.5rem; border:none; border-radius:8px; cursor:pointer; }
    #on  { background:#4ade80; }
    #off { background:#f87171; }
    #status { margin-top:1rem; color:#888; font-size:0.9rem; }
  </style>
</head>
<body>
  <h1>🌡️ Live Temperature</h1>
  <div id="temp">--</div>
  <div id="status">waiting for device...</div>

  <h1>💡 LED Control</h1>
  <button id="on"  onclick="setLed('on')">ON</button>
  <button id="off" onclick="setLed('off')">OFF</button>

<script>
async function refresh() {
  const r = await fetch('/api/latest');
  const d = await r.json();
  document.getElementById('temp').textContent =
      d.temp !== null ? d.temp.toFixed(1) + '°C' : '--';
  document.getElementById('status').textContent =
      d.online ? 'device online' : 'device offline';
  document.getElementById('status').style.color =
      d.online ? '#4ade80' : '#f87171';
}
async function setLed(state) {
  await fetch('/api/led/' + state);
}
setInterval(refresh, 2000);
refresh();
</script>
</body>
</html>
"""

@app.route("/")
def dashboard():
    return render_template_string(DASHBOARD)

@app.route("/api/sensor", methods=["POST"])
def receive_sensor():
    global last_seen
    data = request.get_json()
    readings.append({"temp": data["temp"], "time": time.time()})
    if len(readings) > 100:
        readings.pop(0)
    last_seen = time.time()
    return {"ok": True}

@app.route("/api/latest")
def latest():
    online = (time.time() - last_seen) < 10
    return jsonify({
        "temp": readings[-1]["temp"] if readings else None,
        "online": online,
        "led": led_state
    })

@app.route("/api/led/<state>")
def set_led(state):
    global led_state
    if state in ("on", "off"):
        led_state = state
    return {"led": led_state}

@app.route("/api/led")
def get_led():
    return {"led": led_state}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)