#!/bin/bash
# =============================================================================
# install.sh — stylethesaurus
#
# Run this from the repo root on the server after cloning.
# It sets up the virtualenv, installs dependencies, and registers
# the app as a systemd service.
#
# Usage:
#   bash server_setup.sh
# =============================================================================

set -e

APP_NAME="stylethesaurus"
GIT_NAME="thesaurusx"
APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"  # repo root, wherever it is
PYTHON="python3"

echo "=== [$APP_NAME] Installing from $APP_DIR ==="

# ── 1. Virtual environment ────────────────────────────────────────────────────
echo "--- Creating virtualenv ---"
$PYTHON -m venv "$APP_DIR/venv"
source "$APP_DIR/venv/bin/activate"
pip install --upgrade pip
pip install wheel
pip install -r "$APP_DIR/requirements.txt"
pip install uwsgi
deactivate
echo "Virtualenv ready."

# ── 2. systemd service file ───────────────────────────────────────────────────
# Written here rather than committed to the repo because it contains
# absolute paths that depend on where the repo was cloned and who the user is.
echo "--- Writing systemd service ---"
sudo bash -c "cat > /etc/systemd/system/${APP_NAME}.service << EOF
[Unit]
Description=uWSGI instance for $APP_NAME
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$APP_DIR
Environment=\"PATH=$APP_DIR/venv/bin\"
ExecStart=$APP_DIR/venv/bin/uwsgi --ini $APP_DIR/$GIT_NAME.ini

Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl daemon-reload
sudo systemctl enable "$APP_NAME"
sudo systemctl start "$APP_NAME"
echo "systemd service '$APP_NAME' started."

echo ""
echo "=== [$APP_NAME] Install complete ==="
echo ""
echo "The app is now running. To connect it to nginx, add this location"
echo "block to the central nginx server config:"
echo ""
echo "    location /stylethesaurus {"
echo "        include uwsgi_params;"
echo "        uwsgi_pass unix:/tmp/${APP_NAME}.sock;"
echo "    }"
echo ""
echo "Useful commands:"
echo "  sudo systemctl status $APP_NAME"
echo "  sudo systemctl restart $APP_NAME"
echo "  sudo journalctl -u $APP_NAME -f"