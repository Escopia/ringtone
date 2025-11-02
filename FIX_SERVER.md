# 🔧 Fix Server Issues

## Your Situation

You're accessing: **workstation.awal.com** (remote server)
The server is currently down and design hasn't updated.

## Quick Fix Steps

### Step 1: SSH into Your Server

```bash
ssh your-username@workstation.awal.com
```

### Step 2: Navigate to Project

```bash
cd /path/to/ringtone
# Common paths:
# cd /var/www/ringtone
# cd /home/user/ringtone
# cd /opt/ringtone
```

### Step 3: Pull Latest Changes

```bash
git pull origin main
```

### Step 4: Restart the Server

**If using Docker:**
```bash
./deploy.sh
```

**If using systemd:**
```bash
sudo systemctl restart ringtone
```

**If using screen/tmux:**
```bash
pkill -f uvicorn
uvicorn web_app:app --host 0.0.0.0 --port 8000 &
```

**If using PM2:**
```bash
pm2 restart ringtone
```

### Step 5: Verify

Visit: http://workstation.awal.com/upload

## If You Don't Have SSH Access

Contact your server administrator to:
1. Pull latest changes from GitHub
2. Restart the application
3. Clear any caches

## What Was Fixed

✅ Fixed route handlers (all async now)
✅ Fixed Dockerfile to use web_app:app
✅ Fixed docker-compose.yml
✅ Added proper error handling
✅ Consistent encoding (UTF-8)

## Test Locally First

Before deploying to remote server:

```bash
cd /Users/ofentsephukubye/Downloads/ringtone-main/ringtone
./start.sh
```

Visit: http://localhost:8000/upload

If it works locally, deploy to remote server.

## Need Help?

1. Check server logs
2. Verify git pull worked
3. Ensure server restarted
4. Clear browser cache (Cmd+Shift+R)
