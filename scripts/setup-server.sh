#!/bin/bash

set -e  # Прекратить выполнение при ошибке

echo "==== ====  ==== ==== Starting Yandex Cloud server setup... ==== ====  ==== ===="

echo "==== ==== Updating system packages... ==== ==== "
sudo apt-get update -y
sudo apt-get upgrade -y


echo "==== ==== Installing Docker...==== ==== "
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io


echo "==== ==== Installing Docker Compose... ==== ===="
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose


# Configure Docker -
echo "==== ==== Configuring Docker permissions... ==== ===="
echo "==== Add current user and your username to docker group ===="
sudo groupadd docker 2>/dev/null || true

# Получите фактического пользователя (не root) из SSH-соединения
if [ -n "$SUDO_USER" ]; then
    ACTUAL_USER="$SUDO_USER"
else
    ACTUAL_USER=$(who am i | awk '{print $1}')
fi

# Резервный вариант, если все ещё не найден
if [ -z "$ACTUAL_USER" ] || [ "$ACTUAL_USER" = "root" ]; then
    ACTUAL_USER="ubuntu"  # или ваш username из секретов
fi

echo "Adding user '$ACTUAL_USER' to docker group..."
sudo usermod -aG docker "$ACTUAL_USER"

echo "🔧 Fixing Docker socket permissions..."
sudo chmod 666 /var/run/docker.sock 2>/dev/null || true

sudo systemctl enable docker
sudo systemctl start docker



echo "==== ==== Creating application directories... ==== ===="
sudo mkdir -p /app/sql-replacer/static
sudo mkdir -p /app/sql-replacer/media
sudo chown -R "$ACTUAL_USER":"$ACTUAL_USER" /app
sudo chmod -R 755 /app


echo "==== ==== Creating environment file... ==== ===="
SERVER_IP=$(curl -s ifconfig.me || echo "localhost")
cat > /app/sql-replacer/.env << EOF
DEBUG=False
SECRET_KEY=$(openssl rand -base64 32)
ALLOWED_HOSTS=localhost,127.0.0.1,$SERVER_IP
DJANGO_SETTINGS_MODULE=sql_replacer.settings
PYTHONUNBUFFERED=1
EOF


echo "==== ====  ==== ==== Server setup completed! ==== ====  ==== ===="
echo "User added to docker group: $ACTUAL_USER"
echo "Docker: $(docker --version 2>/dev/null || echo 'Installed')"
echo "Docker Compose: $(docker-compose --version 2>/dev/null || echo 'Installed')"
echo "App directory: /app/sql-replacer"
echo "==== ====  ==== ==== Server setup completed! ==== ====  ==== ===="
