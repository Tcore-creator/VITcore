[app]

title = VITcore Terminal
package.name = vitcore
package.domain = org.vitcore

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas

version = 0.1

requirements = python3,kivy

orientation = portrait
fullscreen = 0

android.api = 36
android.minapi = 24
android.ndk = 28c
android.archs = arm64-v8a

android.accept_sdk_license = False

[buildozer]

log_level = 2
warn_on_root = 1
