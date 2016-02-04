#! /usr/bin/env python2
 
import weechat
import urllib
import urllib2
import re
import HTMLParser

weechat.register("sms", "horgix", "0.1", "Beerware",
        "French to SMS via http://raphlight.free.fr/trad", "", "")

def sms_cb(data, buffer, args):
    # Basics parameters
    url = 'http://raphlight.free.fr/trad'
    values = {'message': args, 'convertir': 'Convertir'}

    # Execute request
    params = urllib.urlencode(values)
    req = urllib2.Request(url, params)
    the_page = urllib2.urlopen(req).read()
    # Parse answer page (why not an API that answers in json :( )
    result = [ e for e in the_page.splitlines() if 'result' in e ][0]
    result = re.sub('.*id=\'result\'> *', '', result)
    result = re.sub(' *</div>.*', '', result)
    result = re.sub('<img src="img/smile_sad.gif" alt=":\(">', ':(', result)
    # Decode, unescape, reencode
    result = HTMLParser.HTMLParser().unescape(result.decode('utf-8'))
    answer = result.encode('utf-8')
    # Send answer to weechat
    weechat.command("", answer)
    return weechat.WEECHAT_RC_OK

hook = weechat.hook_command("sms", "French to SMS", "text", "", "", "sms_cb", "")
