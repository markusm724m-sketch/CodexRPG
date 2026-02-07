[app]
# Application title
title = CodexRPG

# Package name (no spaces, lowercase)
package.name = codexrpg

# Package domain
package.domain = org.codexrpg

# Version
version = 1.0

# Requirements
# List of Python dependencies
requirements = python3,kivy,requests,flask,flask-cors

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE

# Architecture
android.archs = arm64-v8a,armeabi-v7a

# Features
android.features = android.hardware.touchscreen

# API version
android.api = 31
android.minapi = 21
android.ndk = 25b

# Orientation
orientation = portrait

# Allow backup
android.allow_backup = True

# Icon (192x192 PNG)
# Leave empty for automatic generation
# icon.filename = %(source.dir)s/assets/icon.png

# Presplash (512x512 PNG) 
# presplash.filename = %(source.dir)s/assets/presplash.png

# Meta data for theme
android.meta_data = com.google.android.gms.version=@integer/google_play_services_version

# Icon definition
android.icon_path = assets/icon.png

# Application entry point
# This runs the Flask server instead of Kivy app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt,md

# Build directory
build_dir = .buildozer

# Gradle options
android.gradle_options = org.gradle.jvmargs=-Xmx2048m

[buildozer]

# Log level (0 = error, 1 = info, 2 = debug, 3 = trace)
log_level = 2

# Display warning when buildozer is executed as root
warn_on_root = 1

# Path to build artifacts
bin_dir = ./bin
