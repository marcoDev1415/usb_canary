# USB Canary - Python 3.11.2 Migration

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)

USB Canary migrado a Python 3.11.2 - Una herramienta de Linux que usa pyudev para monitorear dispositivos USB ya sea las 24 horas o solo cuando está bloqueada. Puede configurarse para enviar SMS vía Twilio API, notificar un canal de Slack, o enviar mensajes de Telegram.

## ⚠️ MIGRACIÓN A PYTHON 3.11.2

Este proyecto ha sido completamente migrado de Python 2.7 a **Python 3.11.2** con las siguientes mejoras:

### 🔄 Cambios Principales

- **Shebang actualizado**: `#!/usr/bin/env python3`
- **Librerías modernas**:
  - `slackclient` → `slack-sdk>=3.21.0`
  - `telepot` → `python-telegram-bot>=20.0`
  - `sander-daemon` → `python-daemon>=3.0.0`
  - `twilio` actualizado a versión 8.0.0+
- **Sintaxis Python 3**: f-strings, async/await, manejo de excepciones moderno
- **APIs actualizadas**: Slack Web API, Telegram Bot API v6+, Twilio v8+

### 📋 Prerrequisitos para Python 3.11.2

Instalar dependencias actualizadas:

```bash
# En Raspberry Pi con Python 3.11.2
pip3 install -r requirements.txt

# También necesitas (en Debian/Ubuntu):
sudo apt install python3-apt
```

### 📦 Nuevas dependencias (requirements.txt)

```
# Versiones actualizadas para Python 3.11.2
slack-sdk>=3.21.0
twilio>=8.0.0
pyudev>=0.24.0
python-daemon>=3.0.0
python-telegram-bot>=20.0
```

### 🚀 Instalación en Raspberry Pi

1. **Clona el repositorio**:
```bash
git clone https://github.com/Tonow/usb-canary-telegram.git
cd usb-canary-telegram/usb-canary-master
```

2. **Instala Python 3.11.2** (si no está instalado):
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv
```

3. **Crea un entorno virtual**:
```bash
python3.11 -m venv usb_canary_env
source usb_canary_env/bin/activate
```

4. **Instala las dependencias**:
```bash
pip install -r requirements.txt
sudo apt install python3-apt
```

5. **Configura settings.json**:
```json
{
  "settings": {
    "telegram": {
      "bot_token": "TU_BOT_TOKEN_AQUÍ",
      "id_client": "TU_CHAT_ID_AQUÍ"
    },
    "slack": {
      "api_key": "xoxb-tu-token-de-slack",
      "channel_name": "general"
    },
    "twilio": {
      "auth_token": "tu_auth_token",
      "account_sid": "tu_account_sid",
      "twilio_number": "+1234567890",
      "mobile_number": "+0987654321"
    },
    "general": {
      "paranoid": true,
      "screensaver": "xscreensaver",
      "slack": false,
      "twilio": false,
      "telegram": true
    }
  }
}
```

6. **Ejecutar**:
```bash
python3 usb_canary.py start
```

### 🆕 Nuevas características

- **Async/Await**: Telegram usa async para mejor rendimiento
- **Mejor manejo de errores**: Excepciones más específicas y descriptivas
- **F-strings**: Formateo de strings más eficiente
- **API modernas**: Compatibilidad con las últimas versiones de Slack, Telegram y Twilio

### 🔧 Configuración de Telegram Bot

1. Habla con [@BotFather](https://t.me/BotFather) en Telegram
2. Crea un nuevo bot: `/newbot`
3. Obtén tu token: `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`
4. Para obtener tu chat ID, habla con [@my_id_bot](https://t.me/my_id_bot)

### ✅ Comandos

```bash
# Iniciar el daemon
python3 usb_canary.py start

# Parar el daemon
python3 usb_canary.py stop

# Reiniciar el daemon
python3 usb_canary.py restart
```

### 🐛 Solución de problemas

- **Error de importación**: Verifica que todas las dependencias estén instaladas
- **Error de permisos**: Ejecuta con `sudo` si es necesario
- **Error de Telegram**: Verifica tu bot_token e id_client
- **Error de pyudev**: Asegúrate de estar en Linux con soporte USB

### 📝 Notas importantes

- **Solo funciona en Linux** (Raspberry Pi incluida)
- **Python 3.11.2 requerido**
- **Las APIs antiguas ya no funcionan** - usa esta versión migrada

---

**Migrado a Python 3.11.2 en 2025** 🐍✨
