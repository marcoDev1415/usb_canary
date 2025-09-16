#!/bin/bash

# Script de instalación para USB Canary Python 3.11.2
# Para Raspberry Pi y sistemas Linux

echo "🐍 Instalando USB Canary para Python 3.11.2..."

# Verificar si estamos en Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo "❌ Error: Este script solo funciona en Linux"
    exit 1
fi

# Verificar si Python 3.11+ está disponible
PYTHON_CMD=""
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ $(echo "$PYTHON_VERSION >= 3.8" | bc -l) -eq 1 ]]; then
        PYTHON_CMD="python3"
    fi
fi

if [[ -z "$PYTHON_CMD" ]]; then
    echo "❌ Error: Python 3.8+ no encontrado. Instalando Python 3.11..."
    sudo apt update
    sudo apt install -y python3.11 python3.11-pip python3.11-venv python3.11-dev
    PYTHON_CMD="python3.11"
fi

echo "✅ Usando Python: $PYTHON_CMD"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
$PYTHON_CMD -m venv usb_canary_env
source usb_canary_env/bin/activate

# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del sistema
echo "🔧 Instalando dependencias del sistema..."
sudo apt update
sudo apt install -y python3-apt libudev-dev

# Instalar dependencias de Python
echo "📚 Instalando dependencias de Python..."
pip install -r requirements.txt

# Hacer ejecutable el script principal
chmod +x usb_canary.py

# Crear configuración de ejemplo si no existe
if [[ ! -f "settings.json" ]]; then
    echo "⚙️ Creando configuración de ejemplo..."
    cat > settings.json << 'EOF'
{
  "settings": {
    "telegram": {
      "bot_token": "CAMBIA_POR_TU_BOT_TOKEN",
      "id_client": "CAMBIA_POR_TU_CHAT_ID"
    },
    "slack": {
      "api_key": "xoxb-CAMBIA-POR-TU-TOKEN",
      "channel_name": "general"
    },
    "twilio": {
      "auth_token": "CAMBIA_POR_TU_AUTH_TOKEN",
      "account_sid": "CAMBIA_POR_TU_ACCOUNT_SID",
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
EOF
    echo "📝 Archivo settings.json creado. ¡EDÍTALO antes de usar!"
fi

echo ""
echo "🎉 ¡Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita settings.json con tus credenciales"
echo "2. Activa el entorno virtual: source usb_canary_env/bin/activate"
echo "3. Ejecuta: python3 usb_canary.py start"
echo ""
echo "📖 Lee README_PYTHON3.md para más información"
