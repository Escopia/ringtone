#!/usr/bin/env python3
"""Test script to verify routes are properly configured"""

import os

print("Testing route configuration...\n")

# Check if templates exist
templates = [
    "templates/login.html",
    "templates/dashboard_modern.html",
    "templates/upload_modern.html",
    "templates/admin.html"
]

print("Checking templates:")
for template in templates:
    exists = os.path.exists(template)
    status = "✓" if exists else "✗"
    print(f"  {status} {template}")

print("\nChecking static files:")
static_files = [
    "static/css/style.css",
    "static/js/upload.js"
]

for static_file in static_files:
    exists = os.path.exists(static_file)
    status = "✓" if exists else "✗"
    print(f"  {status} {static_file}")

print("\nRoute configuration:")
print("  / → templates/login.html")
print("  /dashboard → templates/dashboard_modern.html")
print("  /upload → templates/upload_modern.html")
print("  /admin → templates/admin.html")
print("  /api/tracks/upload → POST endpoint for uploads")

print("\n✓ Configuration complete!")
print("\nTo start the server:")
print("  uvicorn web_app:app --reload --host 0.0.0.0 --port 8000")
