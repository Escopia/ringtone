#!/bin/bash

echo "🚀 Deploying Escopia Distribution Portal..."

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down

# Pull latest changes
echo "Pulling latest changes..."
git pull origin main

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

# Wait for services to start
echo "Waiting for services to start..."
sleep 5

# Check status
echo "Checking container status..."
docker-compose ps

echo ""
echo "✅ Deployment complete!"
echo "Portal available at: http://localhost:8000"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
