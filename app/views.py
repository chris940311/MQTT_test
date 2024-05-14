import paho.mqtt.client as mqtt
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 設定 MQTT 代理伺服器的地址和端口
MQTT_BROKER = "broker.MQTTGO.io"
MQTT_PORT = 1883

LED_STATUS = 'led off'

# 設定訂閱的主題
TOPIC = "test/topic"

# 當接收到 MQTT 消息時的處理函數
def on_message(client, userdata, message):
    global LED_STATUS
    # 在這裡處理 MQTT 消息
    # 例如，將收到的數據保存到數據庫中或者進行其他處理
    print("Received message:", message.payload.decode())
    # 更新 LED 狀態
    LED_STATUS = message.payload.decode()

# 創建 MQTT 客戶端
client = mqtt.Client()

# 設置接收消息的函式
client.on_message = on_message

# 連接到 MQTT 代理伺服器
client.connect(MQTT_BROKER, MQTT_PORT)

# 主題設置
client.subscribe(TOPIC)

# 啟動 MQTT 客戶端的消息循環
client.loop_start()

def send_message_to_mqtt(msg):
    client.publish(TOPIC, msg)

@csrf_exempt
def index(request):
    global LED_STATUS
    if request.method == 'POST':
        if LED_STATUS == 'led off':
            LED_STATUS = "led on"
        else:
            LED_STATUS = "led off"
        send_message_to_mqtt(LED_STATUS)
    return render(request, "index.html", {"LED_STATUS": LED_STATUS})
