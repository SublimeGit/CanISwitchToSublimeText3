# coding: utf-8
import json
import urllib2
import threading
import webbrowser
from functools import partial

import sublime
from sublime_plugin import ApplicationCommand


class CanSwitchCommand(ApplicationCommand):

    URL = 'http://www.caniswitchtosublimetext3.com/api/check'

    def run(self):
        installed_packages = self.get_installed_packages()
        thread = threading.Thread(target=partial(self.perform_check, installed_packages))
        sublime.status_message('Performing package check...')
        thread.start()

    def get_installed_packages(self):
        settings = sublime.load_settings('Package Control.sublime-settings')
        if not settings.has('installed_packages'):
            sublime.error_message("Could not find list of installed packages. Are you using Package Control?")
        packages = settings.get('installed_packages', [])
        if not packages:
            sublime.error_message("You don't have any plugins installed. Upgrade Away!")
        return packages

    def perform_check(self, packages):
        data = json.dumps({'installed_packages2': packages})
        req = urllib2.Request(self.URL, data, {'Content-Type': 'application/json'})

        try:
            res = urllib2.urlopen(req)
        except urllib2.HTTPError as e:
            sublime.error_message('Could not perform check. Server returned %s' % e.code)
            return
        except urllib2.URLError as e:
            sublime.error_message('Could not connect to http://www.caniswitchtosublimetext3.com')
            return

        location = res.info().get('Location')
        webbrowser.open(location)
