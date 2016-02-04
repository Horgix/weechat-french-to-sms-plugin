#! /usr/bin/env python2
 
import weechat
import urllib
import urllib2

import re
import HTMLParser

weechat.register("sms", "horgix", "0.1", "Beerware",
        "French to SMS via http://raphlight.free.fr/trad", "", "")

def sms_cb(data, buffer, args):
    #nick = weechat.buffer_get_string(weechat.current_buffer(), 'localvar_nick')

    url = 'http://raphlight.free.fr/trad'
    values = {'convertir': 'Convertir'}
    values['message'] = args

    #params = urllib.parse.urlencode(values).encode('utf-8')
    params = urllib.urlencode(values)#
    #req = urllib.request.Request(url, params)
    req = urllib2.Request(url, params)
    the_page = urllib2.urlopen(req).read()
    #req.add_header("Content-Type","application/x-www-form-urlencoded;charset=utf-8")
    #with urllib.request.urlopen(req) as response:
    #    the_page = response.read().decode('utf-8')
    result = [ e for e in the_page.splitlines() if 'result' in e ][0]
    result = re.sub('.*id=\'result\'> *', '', result)
    result = re.sub(' *</div>.*', '', result)
    h = HTMLParser.HTMLParser()
    result = h.unescape(result.decode('utf-8'))
    args = result.encode('utf-8')
    weechat.command("", args)
    return weechat.WEECHAT_RC_OK

hook = weechat.hook_command("sms", "French to SMS", "text", "", "", "sms_cb", "")

#sms_cb(None, None, "Bonjour ceci est un test")
