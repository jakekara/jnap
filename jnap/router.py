import requests, json
from base64 import b64encode as b64

#
# Linksys Router class
#
class Linksys:

    def __init__(self, url, pw=""):
        self.url = url
        self.pw = pw

    #
    # auth - internal helper for creating auth header
    #        to send for privileged commands
    # args -   pw - password string. optional. if nothing
    #               is supplied, use the password string
    #               supplied to the constructor, or set
    #               after construction via the password method
    #        user - optional. defaults to "admin." I am
    #               not sure if any other username will
    #               work even though technically the router
    #               says it can have up to 10 usernames
    # rets - none
    #                         
    def auth(self, pw=None, user="admin"):
        if pw is None: pw = self.pw
            
        return {
            "X-JNAP-Authorization":"Basic " +b64(user + ":" + pw)
        }

    #
    # password - set the password to use for authentication
    #     args -    pw - password string
    #            uname - defaults to admin. I don't think anything
    #                    else will work
    #     rets - none
    #
    def password(self, pw, uname="admin"):
        self.pw = pw

    # 
    # def do_get(self, action):
    #     return self.s.get(self.url + action)

    #
    # do_action - Perform a specific API call. This is a helper function
    #             used to build the methods below.
    #      args - action - the action to perform
    #           - [headers] - any additional header values to send
    #           - [data]    - optional POST data. Weirdly doesn't work with a
    #                         dict, so "{}" has to be in quotes. I think that might
    #                         have to do with the requests library, but I haven't looked
    #                         under the hood at whether it's replacing {} with nothing.
    #                         That seems to be what's going on based on the HTTP traffic.
    #      rets - returns a response to the HTTP POST request (see requests library)
    #     notes - maybe I should make this return the JSON
    #
    def do_action(self, action, headers={}, data={}):

        self.s = requests.session()

        self.s.headers.update(headers)
    
        self.s.headers.update({
            "Content-Type": "application/json; charset=UTF-8",
            "Accept": "application/json",
            "X-JNAP-Action":"http://linksys.com/jnap/" + action,
        })

        resp = self.s.post(self.url + "/JNAP/", data=json.dumps(data), verify=False)

        return resp

    #
    # check_password - Check whether a supplied string is the admin password
    #                  of the router. Yes, that's a thing.
    #           args -     pw - the password to test
    #                  [user] - the username (defaults to "admin"). this is
    #                           optional and I'm not sure if any other user name
    #                           would actually work here, although technically
    #                           these routers support more than one user.
    #           rets - same as do_action
    #
    def check_password(self, pw, user="admin"):
        return self.do_action("core/CheckAdminPassword",
                              headers=self.auth(pw, user))
                              

    #
    # has_default_password - Check whether the router still has its default password.
    #                        Yes, that's a thing. I believe these routers are not
    #                        hardcoded, they come with per-unit passwords printed on
    #                        a sticker.
    #                 args - none
    #                 rets - same as do_action
    #
    def has_default_password(self):
        return self.do_action("core/IsAdminPasswordDefault")

    #
    # get_users - list all the router's users. Generally just "admin" and "guest"
    #      args - none
    #      rets - same as do_action
    #
    def get_users(self):
        return self.do_action("storage/GetUsers")

    #
    # get_device_info - get a bunch of summary info about the device
    #            args - none
    #            rets - same as do_action
    def get_device_info(self):
        return self.do_action("core/GetDeviceInfo")

    #
    # stop_ping - stop pinging
    #      args - none
    #      rets - same as do_action
    #     notes - authentiation required
    #
    def stop_ping(self):
        return self.do_action("diagnostics/StopPing",
                              headers=self.auth())

    #
    # start_ping - start pinging something
    #       args -      host - host to ping
    #              byte_size - optional int between 32 and 65500 to specify
    #                          ping payload size
    #                  count - number of pings to send. (None for indefinite!)
    #       rets - same as do_action
    #      notes - authentication required
    #               
    def start_ping(self, host="localhost", byte_size=31337, count=10):

        data={
            "host":host,
            "packetSizeBytes":byte_size
        }

        if count is not None:
            data["pingCount"] = count

        print data
        
        return self.do_action("diagnostics/StartPing",
                              headers=self.auth(),
                              data=data)

    #
    # get_ping_status - check on how a ping action is going
    #            args - none
    #            rets - same as do_action
    #           notes - authentication required
    def get_ping_status(self):
        return self.do_action("diagnostics/GetPingStatus",headers=self.auth())

    #
    # state_traceroute - start tracerouteing to some host
    #             args - host - a hostname or IPv4 addr string
    #             rets - same as do_action
    #            notes - authentication required
    #          
    def start_traceroute(self, host):
        return self.do_action("diagnostics/StartTraceroute",headers=self.auth(),
                              data={"host":host})

    #
    # stop_traceroute - stop a traceroute action
    #            args - none
    #            rets - same as do_action
    #           notes - authentication required
    def stop_traceroute(self):
        return self.do_action("diagnostics/StopTraceroute",headers=self.auth())            

    #
    # get_traceroute_status - get the status of a traceroute action
    #                  args - none
    #                  rets - same as do-action
    #                 notes - authentication required
    def get_traceroute_status(self):
        return self.do_action("diagnostics/GetTracerouteStatus",headers=self.auth())
