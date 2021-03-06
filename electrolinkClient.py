import paho.mqtt.client as mqtt
import json
import Queue

###
# Electrolink Class
###
class Electrolink():

    def __init__(self, mqttHost, mqttPort):
        self.host = mqttHost
        self.port = mqttPort
        self.mqttTopicReq = '/electrolink/req'
        self.mqttTopicRsp = '/electrolink/rsp'
        self.authUuid = ''
        self.token = ''
        self.client = None
        self.msg = {}
        self.msgId = 0
        self.qs = Queue.Queue()

        # Define event callbacks
        def on_connect(mosq, obj, rc):
            print("rc: " + str(rc))
            self.client.subscribe(self.mqttTopicRsp)

        def on_message(mosq, obj, msg):
            print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

            p = json.loads(msg.payload);
            self.qs[p['id']].put(p)

        def on_publish(mosq, obj, mid):
            print("mid: " + str(mid))

        def on_subscribe(mosq, obj, mid, granted_qos):
            print("Subscribed: " + str(mid) + " " + str(granted_qos))

        def on_log(mosq, obj, level, string):
            print(string)


        self.client = mqtt.Client()

        self.client.on_connect = on_connect
        self.client.on_message = on_message
        self.client.on_publish = on_publish
        self.client.on_subscribe = on_subscribe

        print self.host, self.port
        self.client.connect(self.host, self.port, 60)

        # Start looping
        self.client.loop_start()

    def linkIt(self):

        payload = json.dumps(self.msg)
        (rc, mid) = self.client.publish(self.mqttTopicReq, payload, qos=1)

        # Block on queue waiting for response
        rsp = self.qs.get()

        return rsp


    # === GPIO ===

    ###
    # pinFunction()
    ###
    def pinFunction(self, pinId, pinFnc):
        """
        {
            'method': 'setFunction',
            'params': [<pinId>, <pinFnc>],
        }
        """
        self.msg['method'] = 'pinFunction'
        self.msg['params'] = [pinID, pinFnc]
        
        return self.linkIt()

    ###
    # pinMode()
    ###
    def pinMode(self, pinID, pinMode):

        self.msg['method'] = 'pinMode'
        self.msg['params'] = [pinID, pinMode]
        
        return self.linkIt()


    ###
    # digitalWrite()
    ###
    def digitalWrite(self, pinId, value):

        self.msg['method'] = 'digitalWrite'
        self.msg['params'] = [pinId, value]
        
        return self.linkIt() 

    
    ###
    # digitalRead()
    ###
    def digitalRead(self, pinId):

        self.msg['method'] = 'digitalRead'
        self.msg['params'] = [pinId]
        
        return self.linkIt()

    
    ###
    # attachInterrupt()
    ###
    def attachInterrupt(self, intId, pinId, mode):

        self.msg['method'] = 'attachInterrupt'
        self.msg['params'] = [intId, pinId, mode]
        
        return self.linkIt()

    
    ###
    # detachInterrupt()
    ###
    def detachInterrupt(self, intId):

        self.msg['method'] = 'detachInterrupt'
        self.msg['params'] = [intId]
        
        return self.linkIt()


    # === ADC ===

    ###
    # analogRead()
    ###
    def analogRead(self, pinId):

        self.msg['method'] = 'analogRead'
        self.msg['params'] = [pinId]
        
        return self.linkIt()

    ###
    # pulseIn()
    ###
    def pulseIn(self, pinId, level, tout):

        self.msg['method'] = 'pulseIn'
        self.msg['params'] = [pinId, level, tout]
        
        return self.linkIt()


    # === PWM ===

    ###
    # pwmStart()
    ###
    def pwmStart(self, pwmNb, period):

        self.msg['method'] = 'pwmStart'
        self.msg['params'] = [pwmNb, period]
        
        return self.linkIt()

    ###
    # pwmSet()
    ###
    def pwmSet(self, pwmNb, channel, hiTime):

        self.msg['method'] = 'pwmSet'
        self.msg['params'] = [pwmNb, channel, hiTime]
        
        return self.linkIt()

    ###
    # pwmStop()
    ###
    def pwmStop(self, pwmNb):

        self.msg['method'] = 'pwmStop'
        self.msg['params'] = [pwmNb]
        
        return self.linkIt()


    # === SPI ===

    ###
    # spiStart()
    ###
    def spiStart(self, spiNb, divider, mode):

        self.msg['method'] = 'spiStart'
        self.msg['params'] = [spiNb, divider, mode]
        
        return self.linkIt()

    ###
    # spiTransfer()
    ###
    def spiTransfer(self, spiNb, data, rsp):

        self.msg['method'] = 'spiTransfer'
        self.msg['params'] = [spiNb, data, rsp]
        
        return self.linkIt()

    ###
    # spiStop()
    ###
    def spiStop(self, spiNb):

        self.msg['method'] = 'spiStop'
        self.msg['params'] = [spiNb]
        
        return self.linkIt()


    # === I2C ===

    ###
    # i2cStart()
    ###
    def i2cStart(self):

        self.msg['method'] = 'i2cStart'
        self.msg['params'] = []
        
        return self.linkIt()

    ###
    # i2cTransfer()
    ###
    def i2cTransfer(self, addr, wrData, rdLen):

        self.msg['method'] = 'i2cTransfer'
        self.msg['params'] = [addr, wrData, rdLen]
        
        return self.linkIt()

    ###
    # i2cStop()
    ###
    def i2cStop(self):

        self.msg['method'] = 'i2cStop'
        self.msg['params'] = []
        
        return self.linkIt()


    # === System ===

    ###
    # registerWrite()
    ###
    def registerWrite(self, regAddr, val):

        self.msg['method'] = 'registerWrite'
        self.msg['params'] = [regAddr, val]
        
        return self.linkIt()

    ###
    # registerRead()
    ###
    def registerRead(self, regAddr):

        self.msg['method'] = 'registerRead'
        self.msg['params'] = [regAddr]
        
        return self.linkIt()

    ###
    # getDeviceInfo()
    ###
    def getDeviceInfo(self):

        self.msg['method'] = 'getDeviceInfo'
        self.msg['params'] = []
        
        return self.linkIt()
