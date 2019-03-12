import tornado.web
import tornado.escape
import json
import secrets
from rest_endpoint.orgs.meta import frame_msg
from rest_endpoint.sawtooth_client.tx import SawtoothClientStub

class OrgsHandler(tornado.web.RequestHandler):
    def post(self):
        payload = tornado.escape.json_decode(self.request.body)
        if "action" not in payload :
            self.write(json.dumps(
                frame_msg({
                    "msg" : "Action type missing",
                },status="BAD_REQUEST")
            ))
            self.finish()
        elif "org_name" not in payload :
            self.write(json.dumps(
                frame_msg({
                    "msg" : "Organization name missing",
                },status="BAD_REQUEST")
            ))
            self.finish()
        elif "creator_id" not in payload :
            self.write(json.dumps(
                frame_msg({
                    "msg" : "Creator's DigitalID missing",
                },status="BAD_REQUEST")
            ))
            self.finish()
        rnd_org_id = secrets.token_hex(32)
        payload["org_id"] = rnd_org_id
        sawtooth_rest_api =  SawtoothClientStub(tf_name="orgs",tf_version="1.0",payload=payload)
        sawtooth_rest_api.set_address_scope()
        response = sawtooth_rest_api.send()