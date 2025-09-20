import sys
import subprocess
import shutil
import canary.settings

supported_screensavers = ('gnome-screensaver', 'xscreensaver')


def set_screensaver(screensaver_option):
    """
    Detects the screensaver - this can be specified by the user at install time, or detected if not set.
    If screensaver is specified, it is checked against the supported screensavers list.
    :param screensaver_option: the screensaver returned by the command line.
    :return: the identified screensaver as specified by the user, or detected by the program
    """
    if screensaver_option == "":
        screensaver_option = identify_screensaver()
        save_screensaver(screensaver_option)
    else:
        if screensaver_option in supported_screensavers:
            save_screensaver(screensaver_option)
        else:
            print('')
            sys.exit(126)
    return screensaver_option


def save_screensaver(screensaver):
    """
    Writes the screensaver to the settings.json file
    :param screensaver: the screensaver
    :return:
    """
    settings = canary.settings.open_settings()
    general_settings = settings['settings']['general']
    if general_settings['screensaver']:
        print("Writing over screensaver value {}".format(general_settings['screensaver']))
    general_settings['screensaver'] = screensaver
    canary.settings.save_settings(settings)


def identify_screensaver():
    """
    Identifica el screensaver instalado usando métodos compatibles con múltiples distribuciones
    """
    installed_screensavers = []
    
    # Método 1: Verificar binarios ejecutables
    for screensaver in supported_screensavers:
        if screensaver == 'xscreensaver':
            if shutil.which('xscreensaver') or shutil.which('xscreensaver-command'):
                installed_screensavers.append(screensaver)
        elif screensaver == 'gnome-screensaver':
            if shutil.which('gnome-screensaver') or shutil.which('gnome-screensaver-command'):
                installed_screensavers.append(screensaver)
    
    # Método 2: Si no encontramos con shutil.which, intentar con dpkg (Debian/Ubuntu)
    if not installed_screensavers:
        for screensaver in supported_screensavers:
            try:
                result = subprocess.run(['dpkg', '-l', screensaver], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0 and 'ii' in result.stdout:
                    installed_screensavers.append(screensaver)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # dpkg no disponible o timeout, continuar
                pass
    
    # Método 3: Intentar con rpm (Red Hat/Fedora/CentOS)
    if not installed_screensavers:
        for screensaver in supported_screensavers:
            try:
                result = subprocess.run(['rpm', '-q', screensaver], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    installed_screensavers.append(screensaver)
            except (subprocess.TimeoutExpired, FileNotFoundError):
                # rpm no disponible o timeout, continuar
                pass
    
    # Evaluar resultados
    if not installed_screensavers:
        print("No se detectó ningún screensaver soportado. Por favor, especifica manualmente en settings.json")
        print(f"Screensavers soportados: {', '.join(supported_screensavers)}")
        sys.exit(126)
    elif len(installed_screensavers) == 1:
        print(f"Screensaver detectado automáticamente: {installed_screensavers[0]}")
        return installed_screensavers[0]
    else:
        print("Múltiples screensavers detectados. Por favor, especifica cuál usar en settings.json")
        print(f"Detectados: {', '.join(installed_screensavers)}")
        sys.exit(125)


def get_supported_screensavers():
    return supported_screensavers
