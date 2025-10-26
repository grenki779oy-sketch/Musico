[app]
title = Spotify Premium
package.name = spotifypremium
package.domain = com.spotify
source.dir = .
source.main = main.py
version = 1.0
requirements = python3,kivy,kivymd,requests,openssl,android
orientation = portrait
android.api = 33
android.minapi = 21
android.archs = arm64-v8a
android.permissions = INTERNET
android.release_artifact = .apk
android.signed_apk = True
icon.filename = assets/icon.png
p4a.branch = master
android.accept_sdk_license = True
