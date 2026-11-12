[app]
title = Motivation Quotidienne
package.name = motivation
package.domain = org.motivation
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0.0
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0
orientation = portrait
fullscreen = 0

# Android 7.0 = API 24
android.minapi = 24
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
