# Деплой «Микрозелени» (staging на VDS)

Стек делит сервер с другими проектами за **нативным nginx**. Поэтому:
- бэкенд (db + backend + bot) поднимается в Docker, backend слушает только `127.0.0.1:8001`;
- фронты собираются локально и раздаются статикой через системный nginx;
- HTTPS — Let's Encrypt на `sslip.io`-имя (без покупки домена).

Имя стенда: **`microgreen.31.57.250.98.sslip.io`** (резолвится в IP сервера).

---

## 1. Подготовка сервера (один раз)

```bash
# Swap (RAM в обрез) — 2 ГБ
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Docker + compose-плагин (официальный репозиторий)
curl -fsSL https://get.docker.com | sudo sh
```

## 2. Код и секреты

```bash
sudo git clone https://github.com/romankibenko/microgreen.git /opt/microgreen
cd /opt/microgreen
sudo cp .env.example .env
sudo nano .env   # заполнить значения ниже
```

`.env` для прода:

```ini
POSTGRES_USER=microgreen
POSTGRES_PASSWORD=<длинный случайный>
POSTGRES_DB=microgreen

BOT_TOKEN=<токен из BotFather>
ADMIN_CHAT_ID=307324169
SHOP_URL=https://microgreen.31.57.250.98.sslip.io

JWT_SECRET=<python3 -c "import secrets; print(secrets.token_urlsafe(48))">
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<надёжный пароль>
```

## 3. Поднять бэкенд-стек

```bash
cd /opt/microgreen
sudo docker compose -f docker-compose.prod.yml up -d --build
sudo docker compose -f docker-compose.prod.yml ps        # все healthy
curl -s http://127.0.0.1:8001/health                     # {"status":"ok"}
```

## 4. Фронты (собираются ЛОКАЛЬНО, заливаются статикой)

На рабочей машине:

```bash
npm --prefix landing run build      # → landing/dist  (base /)
npm --prefix admin run build        # → admin/dist    (base /admin/)

ssh c0d3sp1der@31.57.250.98 'sudo mkdir -p /var/www/microgreen/{landing,admin}'
rsync -az --delete landing/dist/ c0d3sp1der@31.57.250.98:/var/www/microgreen/landing/
rsync -az --delete admin/dist/   c0d3sp1der@31.57.250.98:/var/www/microgreen/admin/
```

## 5. Nginx + HTTPS

```bash
sudo cp /opt/microgreen/deploy/microgreen.nginx.conf /etc/nginx/sites-available/microgreen
sudo ln -s /etc/nginx/sites-available/microgreen /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# Сертификат + автоматический редирект 80→443
sudo certbot --nginx -d microgreen.31.57.250.98.sslip.io --redirect -n --agree-tos -m kozecki2000@gmail.com
```

## 6. Проверка

- `https://microgreen.31.57.250.98.sslip.io` — лендинг с замочком;
- `/admin/` — логин админки;
- оформить заказ → уведомление в Telegram → заказ виден в админке.

---

## Обновление (после изменений в коде)

```bash
# Бэкенд
cd /opt/microgreen && sudo git pull
sudo docker compose -f docker-compose.prod.yml up -d --build

# Фронты — пересобрать локально и повторить rsync из шага 4
```
