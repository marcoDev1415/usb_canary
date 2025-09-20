#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del daemon
"""

import sys
import os

# Agregar el directorio actual al path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_daemon_imports():
    """Prueba que los imports del daemon funcionen"""
    try:
        from daemon import DaemonContext
        from daemon.pidfile import TimeoutPIDLockFile
        print("✅ Imports de daemon: OK")
        return True
    except ImportError as e:
        print(f"❌ Error importando daemon: {e}")
        return False

def test_daemon_creation():
    """Prueba crear una instancia del daemon"""
    try:
        from usb_canary import Usb_Canary
        daemon = Usb_Canary('/tmp/test_usbcanary.pid')
        print("✅ Creación de daemon: OK")
        return True
    except Exception as e:
        print(f"❌ Error creando daemon: {e}")
        return False

def test_pidfile_creation():
    """Prueba crear un PIDFile"""
    try:
        from daemon.pidfile import TimeoutPIDLockFile
        pidfile = TimeoutPIDLockFile('/tmp/test_pidfile.pid')
        print("✅ Creación de PIDFile: OK")
        return True
    except Exception as e:
        print(f"❌ Error creando PIDFile: {e}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🔍 Probando funcionalidad del daemon...")
    print("=" * 50)
    
    tests = [
        ("Imports de daemon", test_daemon_imports),
        ("Creación de daemon", test_daemon_creation),
        ("Creación de PIDFile", test_pidfile_creation),
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\n🧪 {name}:")
        if test_func():
            passed += 1
        else:
            print("   Revisar instalación de python-daemon")
    
    print("\n" + "=" * 50)
    if passed == total:
        print(f"🎉 Todas las pruebas pasaron ({passed}/{total})")
        print("✅ El daemon debería funcionar correctamente")
        return 0
    else:
        print(f"❌ Algunas pruebas fallaron ({passed}/{total})")
        print("💡 Instala: pip install python-daemon>=3.0.0")
        return 1

if __name__ == "__main__":
    sys.exit(main())
