#!/usr/bin/env python3
# coding=utf-8

# usb_canary - a Linux tool that uses pyudev to monitor devices while
# your computer is locked. In the case it detects someone plugging in
# or unplugging devices it can be configured to make a noise or send
# you an SMS alerting to you of the potential security breach.

# Copyright (C) 2017 errbufferoverfl
# Migrated to Python 3.11.2 in 2025
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
import os
import platform
import signal
import socket
import sys
import time

import pyudev
from daemon import DaemonContext
from daemon.pidfile import TimeoutPIDLockFile

from canary import message_handler
from canary import settings
from canary.message_handler import send_message
from canary.screensaver import helpers
from canary.slack import slack
from canary.twilleo import twilleo
from canary.telegram import telegram

twilio_settings = None
slack_settings = None
telegram_settings = None


class Usb_Canary:
    def __init__(self, pidfile):
        self.pidfile = pidfile
        
    def run(self):
        while True:
            self.main()
            time.sleep(5)

    def main(self):
        options_file = settings.open_settings()
        options = options_file['settings']['general']

        if options['twilio']:
            global twilio_settings
            twilio_settings = twilleo.load_twilio_settings()

        if options['slack']:
            global slack_settings
            slack_settings = slack.load_slack_settings()

        if options['telegram']:
            global telegram_settings
            telegram_settings = telegram.load_telegram_settings()

        if settings.check_paranoid_set(options['paranoid']):
            paranoid_setting = options['paranoid']

        screensaver_setting = helpers.set_screensaver(options['screensaver'])

        try:
            self.monitor(paranoid_setting, screensaver_setting)
        except AttributeError:
            print("Unable to start application, mode or screensaver have not been set properly")

    def monitor(self, paranoid, screensaver):
        operating_system = platform.system().lower()

        if operating_system in settings.get_supported_operating_systems():
            monitor, context = self.initialise_pyudev()
            if screensaver == 'xscreensaver':
                screensaver_monitor = os.popen('xscreensaver-command -watch')
                observer = pyudev.MonitorObserver(monitor, callback=self.set_device_event, name='monitor-observer')
                if paranoid:
                    observer.start()
                    settings.print_message('Observer started')
                elif not paranoid:
                    while True:
                        line = screensaver_monitor.readline()

                        if line.startswith('LOCK'):
                            observer.start()
                            settings.print_message('Observer started')

                        if line.startswith('UNLOCK'):
                            settings.print_message('Observer stopped')
                            observer.join()
                else:
                    sys.exit(127)
            elif screensaver == 'gnome-screensaver':
                if paranoid:
                    observer = pyudev.MonitorObserver(monitor, callback=self.set_device_event, name='monitor-observer')
                    observer.start()
                    settings.print_message('Observer started')
                    time.sleep(2)
                elif not paranoid:
                    observer = pyudev.MonitorObserver(monitor, callback=send_message, name='monitor-observer')
                    observer.start()
                    settings.print_message('Observer started')
                else:
                    sys.exit(127)
            else:
                sys.exit(126)

    def initialise_pyudev(self):
        context = pyudev.Context()

        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by(subsystem='usb', device_type='usb_device')

        return monitor, context

    def set_device_event(self, device):
        time.ctime()  # TODO: Do we need this line?
        if device.action == 'remove':
            fmt = '{0} - {1} reported a USB was {2.action}d from node {2.device_node}'
            time.sleep(5)
        else:
            fmt = '{0} - {1} reported a USB was {2.action}ed to node {2.device_node}'
        alert = fmt.format(time.strftime('%l:%M%p %Z on %b %d, %Y'), socket.gethostname(), device)
        print(alert)
        message_handler.send_message(alert)
    
    def start(self):
        """Start the daemon"""
        # Verificar si ya está corriendo
        if self._is_running():
            print("Daemon ya está ejecutándose")
            return 1
        
        try:
            # Crear el contexto del daemon
            pidfile = TimeoutPIDLockFile(self.pidfile)
            context = DaemonContext(
                pidfile=pidfile,
                working_directory=os.getcwd(),
                umask=0o002,
            )
            
            with context:
                self.run()
        except Exception as e:
            print(f"Error starting daemon: {e}")
            return 1
        return 0
    
    def stop(self):
        """Stop the daemon"""
        if not self._is_running():
            print("Daemon no está ejecutándose")
            return 1
            
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
        except (IOError, ValueError):
            print("PID file not found or invalid")
            return 1
        
        try:
            os.kill(pid, signal.SIGTERM)
            # Esperar un poco para que termine
            time.sleep(2)
            
            # Verificar si terminó
            if self._is_running():
                print("Forzando terminación...")
                os.kill(pid, signal.SIGKILL)
                time.sleep(1)
            
            # Limpiar PID file
            if os.path.exists(self.pidfile):
                os.remove(self.pidfile)
            print("Daemon stopped")
            return 0
        except OSError as e:
            print(f"Error stopping daemon: {e}")
            return 1
    
    def restart(self):
        """Restart the daemon"""
        self.stop()
        time.sleep(1)
        return self.start()
    
    def _is_running(self):
        """Check if daemon is running"""
        try:
            with open(self.pidfile, 'r') as pf:
                pid = int(pf.read().strip())
            # Verificar si el proceso existe
            os.kill(pid, 0)
            return True
        except (OSError, IOError, ValueError):
            return False


if __name__ == '__main__':
    daemon = Usb_Canary('/tmp/usbcanary.pid')
    try:
        func = {'start': daemon.start,
                'stop': daemon.stop,
                'restart': daemon.restart}.get(sys.argv[1].lower())
    except IndexError:
        print(f"usage: {sys.argv[0]} start|stop|restart")
        sys.exit(2)
    if func:
        #daemon.run() # test
        sys.exit(func())
    else:
        print("Unknown command")
        sys.exit(2)
