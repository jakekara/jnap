### jnap - library for talking to Linksys router API

This library allows you to programatically talk to Linksys Smart Wi-Fi
routers that use HNAP (or JNAP, I'm not really sure what it's called).

### Install from this repo

Run this at the command line:

    pip install git+git://github.com/jakekara/jnap.git 

### Run the demo script

1. Download the script jnap-demo.py in the demo folder of this repo

2. Assuming your router is at 192.168.1.1 

    python demo/jnap-demo.py https://192.168.1.1 2> /dev/null

Enter your password when prompted. You can enter an invalid password, and
the router will just complain on all the actions that require authorization.

The reason I redirected stderr to /dev/null is it will warn that SSL
verification is off constantly. SSL verification fails because the router's
cert is not trusted. You could forego the stderr redirect if you want to
see the warnings. You could also use http:// in front of your router's IP
address.

### Using in your code

The demo script is well documented and uses all of the features I bothered
to implement. It serves as a better tutorial than I have the time to write
right now. Nonetheless, here is a quick synopsis of some key features


      # import the library
      from jnap.router import Linksys

      # set up a router connection with an optional admin password
      router = Linksys(IP_ADDRESS, pw="PASSWORD")

      # now you can just call actions that I've implemented, like...
      
      # check if the router has a default password
      router.has_default_password()

      # test a password string against the admin password to see if they
      #  match
      router.check_password("PASSWORD")

### API method documentation

All of the methods jnap/router.py are well documented in the comments. Here
is the documentation as it appears in the comments. These can all be called
on the router instance.

           
	    password - set the password to use for authentication
	        args -    pw - password string
	               uname - defaults to admin. I don't think anything
	                       else will work
	        rets - none
	   

	   
	    check_password - Check whether a supplied string is the admin password
	                     of the router. Yes, that's a thing.
	              args -     pw - the password to test
	                     [user] - the username (defaults to "admin"). this is
	                              optional and I'm not sure if any other user name
	                              would actually work here, although technically
	                              these routers support more than one user.
	              rets - same as do_action
	   


    
     has_default_password - Check whether the router still has its default password.
                            Yes, that's a thing. I believe these routers are not
                            hardcoded, they come with per-unit passwords printed on
                            a sticker.
                     args - none
                     rets - same as do_action
    

    
     get_users - list all the router's users. Generally just "admin" and "guest"
          args - none
          rets - same as do_action
    

    
     get_device_info - get a bunch of summary info about the device
                args - none
                rets - same as do_action

    
     stop_ping - stop pinging
          args - none
          rets - same as do_action
         notes - authentiation required
    

    
     start_ping - start pinging something
           args -      host - host to ping
                  byte_size - optional int between 32 and 65500 to specify
                              ping payload size
                      count - number of pings to send. (None for indefinite!)
           rets - same as do_action
          notes - authentication required
                   

    
     get_ping_status - check on how a ping action is going
                args - none
                rets - same as do_action
               notes - authentication required

    
     start_traceroute - start tracerouteing to some host
                 args - host - a hostname or IPv4 addr string
                 rets - same as do_action
                notes - authentication required
              

    
     stop_traceroute - stop a traceroute action
                args - none
                rets - same as do_action
               notes - authentication required

    
     get_traceroute_status - get the status of a traceroute action
                      args - none
                      rets - same as do-action
                     notes - authentication required

### Extending

All of the above methods are implemented by calling the following helper
method, so you can easily add support for JNAP API calls you want to make:

    
     do_action - Perform a specific API call. This is a helper function
                 used to build the methods below.
          args - action - the action to perform
               - [headers] - any additional header values to send
               - [data]    - optional POST data. Weirdly doesn't work with a
                             dict, so "{}" has to be in quotes. I think that might
                             have to do with the requests library, but I haven't looked
                             under the hood at whether it's replacing {} with nothing.
                             That seems to be what's going on based on the HTTP traffic.
          rets - returns a response to the HTTP POST request (see requests library)
         notes - maybe I should make this return the JSON
     




      

      





