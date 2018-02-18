#
# jnap-demo.py - demonstrate methods in the jnap library
# by Jake Kara
# February 2018
# jake@jakekara.com
#

from jnap.router import Linksys
from time import sleep
import json
import sys

router = Linksys(sys.argv[1])

if len(sys.argv) > 2:
    # Try to set router password if one is supplied.
    # Some tests won't work if invalid password is supplied
    router.password(sys.argv[2])
    print router.check_password(sys.argv[2]).content

# Checking whether router has default password
print router.has_default_password().content

# Listing all users
print router.get_users().content

# Getting a bunch of device info
print router.get_device_info().content

# Testing out the ping functionality
print router.stop_ping().content
print router.start_ping(host="192.168.1.197",count=10).content

# Check every 2 seconds to see if ping is done. TIMEOUT after 1 minute
TIMEOUT=60
SLEEPFOR=2

while TIMEOUT > 0:
    status = router.get_ping_status().json()["output"]["isRunning"]
    if status != True: break
    else:
        print ("Still pinging: " + str(status))
    TIMEOUT -= SLEEPFOR
    sleep(SLEEPFOR)

print router.get_ping_status().content
print router.stop_ping().content

# Test out the traceroute functionality from the router to google.com
print router.stop_traceroute().content
print router.start_traceroute("google.com").content

# Reset the clock
TIMEOUT = 60
while TIMEOUT > 0:
    status = router.get_traceroute_status().json()["output"]["isRunning"]
    if status != True: break
    else:
        print ("Still tracing: " + str(status))
    TIMEOUT -= SLEEPFOR
    sleep(SLEEPFOR)

print router.stop_traceroute().content
print router.get_traceroute_status().content



