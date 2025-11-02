# 🚀 Deployment Guide

## Deploy to Remote Server (workstation.awal.com)

### Option 1: Using Docker (Recommended)

1. **SSH into your server:**
```bash
ssh user@workstation.awal.com
```

2. **Navigate to project directory:**
```bash
cd /path/to/ringtone
```

3. **Pull latest changes:**
```bash
git pull origin main
```

4. **Deploy:**
```bash
./deploy.sh
```

### Option 2: Manual Deployment

1. **SSH into server:**
```bash
ssh user@workstation.awal.com
```

2. **Pull changes:**
```bash
cd /path/to/ringtone
git pull origin main
```

3. **Restart service:**
```bash
# If using systemd
sudo systemctl restart ringtone

# If using docker
docker-compose down && docker-compose up -d --build

# If using screen/tmux
pkill -f uvicorn
uvicorn web_app:app --host 0.0.0.0 --port 8000 &
```

## Local Testing

Before deploying, test locally:

```bash
./start.sh
```

Visit: http://localhost:8000

## Verify Deployment

After deployment, check:
- http://workstation.awal.com/dashboard
- http://workstation.awal.com/upload
- http://workstation.awal.com/admin

## Troubleshooting

### Server not responding
```bash
# Check if service is running
docker-compose ps
# or
ps aux | grep uvicorn

# Check logs
docker-compose logs -f
# or
tail -f /var/log/ringtone.log
```

### Changes not showing
```bash
# Clear browser cache (Cmd+Shift+R)
# Restart server
docker-compose restart
```

### Database issues
```bash
# Reinitialize database
docker-compose exec api python3 init_db.py
```
