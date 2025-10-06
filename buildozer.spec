[app]
title = Graphing Calculator
package.name = graphingapp
package.domain = com.yourname

version = 1.0
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt

requirements = python3,kivy,numpy

[buildozer]
log_level = 2

[android]
api = 33
minapi = 21
ndk = 25b
android.arch = armeabi-v7a, arm64-v8a
permissions = INTERNET

[android:meta-data]
android.app.uses_cleartext_traffic = true