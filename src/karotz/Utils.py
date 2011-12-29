'''
Created on 29 dec. 2011

@author: Popotelle
'''
import hmac
import urllib
import time
import random
import hashlib
import base64
import re

APIKEY= '74f14f9e-a9e5-49f9-be08-031c2a46ccb6'
SECRET= 'fae4a0fd-c2d1-46ba-a691-17089815126c'
INSTALLID = '87deba37-69f8-4608-ad46-a3f73add62b2'

API_PREFIX="http://api.karotz.com/api/karotz/"
WEBCAM_SUFFIX="webcam?action=video"
INTERACTIVE_ID_SUFFIX="&interactiveid="

def getWebcamUrl(interactiveId):
    return "%s%s%s%s" % (API_PREFIX, WEBCAM_SUFFIX, INTERACTIVE_ID_SUFFIX, interactiveId)

def getInteractiveId():
    def sendHttpRequestForInteractiveId():
        # sign parameters in alphabetical order
        def sign(parameters, signature):
            keys = parameters.keys()
            keys.sort()
            sortedParameters = [(key, parameters[key]) for key in keys]
            query = urllib.urlencode(sortedParameters)
            digest_maker = hmac.new(signature, query, hashlib.sha1)
            signValue = base64.b64encode(digest_maker.digest())
            query = query + "&signature=" + urllib.quote(signValue)
            return query
        
        parameters = {}
        parameters['installid'] = INSTALLID
        parameters['apikey'] = APIKEY
        parameters['once'] = "%d" % random.randint(100000000, 99999999999)
        parameters['timestamp'] = "%d" % time.time()
        
        query = sign(parameters, SECRET)
        
        f = urllib.urlopen("http://api.karotz.com/api/karotz/start?%s" % query)
        token = f.read() # should return an hex string if auth is ok, error 500 if not
        print "sendHttpRequestForInteractiveId= %s" % token 
        return token
    
    response = sendHttpRequestForInteractiveId()
    #response = """<VoosMsg><id>0623bd1d-dfa3-46c5-bc52-c87c3ad38c7b</id><recipient>58a154cd272aefb3d9e0754ef0008ff2</recipient><interactiveMode><action>START</action><interactiveId>0199c9c0-6292-4348-afea-1d67a3464646</interactiveId><configId>aebe5bc5-0746-464a-a1bc-4b2d759f94a9</configId><access>asr</access><access>button</access><access>ears</access><access>file</access><access>http</access><access>led</access><access>multimedia</access><access>rfid</access><access>serial</access><access>tts</access><access>webcam</access></interactiveMode></VoosMsg>"""    
    #response="""<interactiveId>5b9c0b0c-8dd8-4131-8df8-faeb32a02bb1</interactiveId>"""
    result = re.search("<interactiveId>([a-z0-9\-]*)</interactiveId>", response)
    if(result == None):
        raise BaseException("No interactive id found dude.")
    
    print "interactiveId = %s" % result.group(1)
    
    return result.group(1)