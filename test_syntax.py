#!/usr/bin/env python3
"""
Script para probar la sintaxis del código migrado a Python 3.11.2
"""

import ast
import sys
from pathlib import Path

def test_python_syntax(file_path):
    """Prueba la sintaxis de un archivo Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        
        # Compilar el código para verificar sintaxis
        ast.parse(source_code)
        return True, "✅ Sintaxis correcta"
    except SyntaxError as e:
        return False, f"❌ Error de sintaxis: {e}"
    except Exception as e:
        return False, f"❌ Error: {e}"

def main():
    """Probar todos los archivos Python del proyecto"""
    project_root = Path(__file__).parent
    python_files = [
        'usb_canary.py',
        'canary/settings.py',
        'canary/message_handler.py',
        'canary/slack/slack_bot.py',
        'canary/telegram/telegram_bot.py',
    ]
    
    print("🔍 Probando sintaxis de archivos migrados a Python 3.11.2...")
    print("=" * 60)
    
    all_passed = True
    for file_path in python_files:
        full_path = project_root / file_path
        if full_path.exists():
            passed, message = test_python_syntax(full_path)
            print(f"{file_path:<35} {message}")
            if not passed:
                all_passed = False
        else:
            print(f"{file_path:<35} ❌ Archivo no encontrado")
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("🎉 ¡Todos los archivos tienen sintaxis correcta para Python 3.11.2!")
        print("\n📋 Resumen de migración:")
        print("  • Python 2.7 → Python 3.11.2")
        print("  • slackclient → slack-sdk")
        print("  • telepot → python-telegram-bot")
        print("  • sander-daemon → python-daemon")
        print("  • Twilio API actualizada")
        print("  • Sintaxis moderna (f-strings, async/await)")
        return 0
    else:
        print("❌ Algunos archivos tienen errores de sintaxis")
        return 1

if __name__ == "__main__":
    sys.exit(main())
