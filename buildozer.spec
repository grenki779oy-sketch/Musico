[app]
title = Musico
package.name = musico
package.domain = com.musico
source.dir = .
source.main = main.py
version = 1.0
requirements = python3,kivy
orientation = portrait

# Android настройки
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.permissions = INTERNET

# Release настройки
android.release_artifact = .apk
android.signed_apk = True

# Иконка приложения
icon.filename = assets/icon.png

# Включение аудио файлов
source.include_exts = py,png,jpg,kv,atlas,mp3,wav,ttf,json

# Дополнительные настройки
android.accept_sdk_license = True
p4a.branch = master
