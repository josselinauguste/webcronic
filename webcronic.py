# -*- coding: ISO-8859-15 -*-

import rumps
from rumps import *
import threading
import urllib2
import base64
import xml.etree.ElementTree as ET
import dateutil.parser
import keychain

class WebcronicStatusBarApp(rumps.App):
    def __init__(self):
        super(WebcronicStatusBarApp, self).__init__("Webcronic")

        self.erroneous_monitors = []

        self.title = None
        self.set_icon()

        self.load_credentials()

        threading.Timer(1, self.update_monitors_states).start()

    def load_credentials(self):
        session_keychain = keychain.Keychain()
        infos = session_keychain.get_generic_password('login', None, 'webcronic')
        if isinstance(infos, dict):
            self.API_USERNAME = infos['account']
            self.API_PASSWORD = infos['password']
        else:
            rumps.alert("Vous devez créer un élément 'webcronic' dans le trousseau d'accès !")

    def update_monitors_states(self):
        try:
            erroneous_monitors = self.get_erroneous_monitors()
        except urllib2.URLError:
            pass
        else:
            for monitor in erroneous_monitors:
                if not monitor in self.erroneous_monitors:
                    rumps.notification('Serveur indisponible', '', '%s est injoignable depuis %s' % (monitor['name'], monitor['since'].strftime('%H:%M')))
            for monitor in self.erroneous_monitors:
                if not monitor in erroneous_monitors:
                    rumps.notification('Serveur disponible', '', '%s est de nouveau joignable' % monitor['name'])
            self.erroneous_monitors = erroneous_monitors

        self.set_icon()
        self.build_menu()
        threading.Timer(60*2, self.update_monitors_states).start()

    def get_erroneous_monitors(self):
        root = self.get_monitors_statuses()
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
        self.menu.clear()
        if len(self.erroneous_monitors) > 0:
            for monitor in self.erroneous_monitors:
                self.menu.add('%s (depuis %s)' % (monitor['name'], monitor['since'].strftime('%H:%M')))
        else:
            self.menu.add('Aucun problème à déplorer actuellement :-)')

    def set_icon(self):
        if len(self.erroneous_monitors) > 0:
            self.icon = 'webcronic-small-error.png'
        else:
            self.icon = 'webcronic-small.png'

if __name__ == "__main__":
    app = WebcronicStatusBarApp()
    app.run()
