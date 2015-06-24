#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
import RPi.GPIO as GPIO
import time
 
class button:
    def __init__(self, port, stat = GPIO.LOW, pud = GPIO.PUD_OFF):
        self.port = port
        self.stat = stat
        self.detect = False
        self.dt = time.time()
        GPIO.setup(self.port, GPIO.IN, pud)
    def get(self):
        stat = GPIO.input(self.port)
        dt = time.time()
        if stat != self.stat and dt > self.dt + 0.02:
            self.stat = stat
            self.dt = dt
            self.detect = True
        return self.stat        
    def check(self):
        stat = self.get()
        detect = self.detect
        self.detect = False
        return stat,detect


from requests_oauthlib import OAuth1Session

def tweet():
	CK = ''                             # Consumer Key
	CS = ''         # Consumer Secret
	AT = '' # Access Token
	AS = ''         # Accesss Token Secert

	# ツイート投稿用のURL
	url = "https://api.twitter.com/1.1/statuses/update.json"
	
	# ツイート本文
	params = {"status": "おはよーモーニング!!"}
	
	# OAuth認証で POST method で投稿
	twitter = OAuth1Session(CK, CS, AT, AS)
	req = twitter.post(url, params = params)
	
	# レスポンスを確認
	if req.status_code == 200:
	    print ("OK")
	else:
	    print ("Error: %d" % req.status_code)

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    btns = [button(17, GPIO.LOW, GPIO.PUD_DOWN),
            button(22, GPIO.LOW, GPIO.PUD_DOWN)]
    try:
        while True:
            for btn in btns:
                stat,detect = btn.check()
                if(detect):
                    if(stat == GPIO.LOW):
                        print btn.port,'FALLING'
			tweet()
                    else:
                        print btn.port,'RISING'
    except KeyboardInterrupt:
        print '\nbreak'
        GPIO.cleanup()


