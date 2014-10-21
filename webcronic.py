import rumps
from rumps import *
import threading
import urllib2
import base64
import xml.etree.ElementTree as ET
import dateutil.parser

class WebcronicStatusBarApp(rumps.App):
    API_USERNAME = ''
    API_PASSWORD = ''

    def __init__(self):
        super(WebcronicStatusBarApp, self).__init__("Webcronic")
        self.title = None
        self.icon = 'webcronic-small.png'

        self.erroneous_monitors = []

        self.update_monitors_states()

    def update_monitors_states(self):
        try:
            erroneous_monitors = self.get_erroneous_monitors()
        except urllib2.URLError as e:
            rumps.alert(e)
        else:
            for monitor in erroneous_monitors:
                if not monitor in self.erroneous_monitors:
                    rumps.notification('Serveur indisponible', '', '%s est injoignable depuis %s' % (monitor['name'], monitor['since'].strftime('%H:%m')))
            for monitor in self.erroneous_monitors:
                if not monitor in erroneous_monitors:
                    rumps.notification('Serveur disponible', '', '%s est de nouveau joignable' % monitor['name'])
            self.erroneous_monitors = erroneous_monitors

        self.build_menu()
        threading.Timer(60*2, self.update_monitors_states).start()

    def get_erroneous_monitors(self):
        root = self.get_monitors_statuses
        erroneous_monitors = []
        for child in root:
            if child.attrib['enabled'] == '1' and child.attrib['state'] == 'error':
                erroneous_monitors.append({'name': child.attrib['name'], 'since': dateutil.parser.parse(child.attrib['since'])})
        return erroneous_monitors

    def get_monitors_statuses(self):
        req = urllib2.Request('https://api.webcron.org/monitor.state/')
        base64string = base64.encodestring('%s:%s' % (self.API_USERNAME, self.API_PASSWORD))[:-1]
        req.add_header("Authorization", "Basic %s" % base64string)
        handle = urllib2.urlopen(req)
        return ET.fromstring(handle.read())

    def build_menu(self):
        menu = []
        for monitor in self.erroneous_monitors:
            menu.append('%s (depuis %s)' % (monitor['name'], monitor['since'].strftime('%H:%m')))
        self.menu = menu

if __name__ == "__main__":
    app = WebcronicStatusBarApp()
    app.run()
