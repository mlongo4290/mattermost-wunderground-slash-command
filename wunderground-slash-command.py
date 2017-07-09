from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import urllib.parse
import json

# Define server address and port, use localhost if you are running this on your Mattermost server.
HOSTNAME = ''
PORT = 7800

# guarantee unicode string
_u = lambda t: t.decode('UTF-8', 'replace') if isinstance(t, str) else t

#Handles mattermost slash command get request
class PostHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        length = int(self.headers['Content-Length'])
        data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        
        response_url = ""
        text = ""
        token = ""
        channel_id = ""
        team_id = ""
        command = ""
        team_domain = ""
        user_name = ""
        channel_name = ""
        # Get POST data and initialize MattermostRequest object
        for key in data:
            if key == 'response_url':
                response_url = data[key]
            elif key == 'text':
                text = data[key]
            elif key == 'token':
                token = data[key]
            elif key == 'channel_id':
                channel_id = data[key]
            elif key == 'team_id':
                team_id = data[key]
            elif key == 'command':
                command = data[key]
            elif key == 'team_domain':
                team_domain = data[key]
            elif key == 'user_name':
                user_name = data[key]
            elif key == 'channel_name':
                channel_name = data[key]

        responsetext = ''
        
        print("Found command %s" % token)
        if token[0] == u'<your-slash-command-token>':
            if len(text) > 0:
                responsetext = getweather(text[0])
            else:
                responsetext = getweather()

        if responsetext:
            res = {}
            res['response_type'] = 'in_channel'
            res['text'] = responsetext
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(res).encode("utf-8"))
        return

#The command search in wunderground for the specified city and return weather info
def getweather(city="Rovereto, Italy"):
    print("Searching cities containing %s" % city)
    r = requests.get("http://autocomplete.wunderground.com/aq?query=%s" % urllib.parse.quote_plus(city))
    cities = r.json()
    
    if "RESULTS" not in cities or len(cities["RESULTS"]) == 0:
        print("No result")
        return u"**No city found**"
    elif len(cities["RESULTS"]) > 1:
        print("Found more than 1 city")
        res = u"**Available cities**:\r\n"
        for c in cities["RESULTS"]:
            res = u"%s* %s\r\n" % (res, c["name"])
        return res
    else:
        print("Requesting weather info from wunderground")
        res = ""
        c = cities["RESULTS"][0]
        r = requests.get('http://api.wunderground.com/api/<your-wunderground-api-here>/geolookup/conditions%s.json' % c["l"])
        data = r.json()
        
        co = data['current_observation']
        
        res = u'#### Weather conditions in **%s**:\n\n' % data['location']['city']
        res += u"![%s](%s)\n\n" % (co['weather'], co['icon_url'])
        res += u"| Field | Value |\n"
        res += u'| :---- | :----: |\n'
        res += u'| Temperature : | %s °C |\n' % str(co['temp_c'])
        res += u'| Feelslike : | %s °C |\n' % str(co['feelslike_c'])
        res += u'| Wind : | %s |\n' % str(co['wind_string'])
        res += u'| Wind direction : | %s |\n' % str(co['wind_dir'])
        res += u'| Wind speed : | %s kn |\n' % str(round(co['wind_kph']*1/1.852, 1))
        res += u'| Wind gust : | %s kn |\n' % str(round(float(co['wind_gust_kph'])*1/1.852, 1))
        return res

#Start the app listening on specified port for http GET requests incoming from mattermost slash command
if __name__ == '__main__':
    server = HTTPServer((HOSTNAME, PORT), PostHandler)
    print('Starting matterslash server, use <Ctrl-C> to stop')
    server.serve_forever()
