[app]
title = Prayer Test
package.name = prayertest
package.domain = com.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

requirements = kivy,pyjnius,requests

orientation = portrait
fullscreen = 0


[buildozer]
log_level = 2
warn_on_root = 1


# -------- ANDROID --------
android.permissions = INTERNET,WAKE_LOCK,VIBRATE,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED

android.api = 34
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 34.0.0

android.accept_sdk_license = True
android.enable_androidx = True

android.gradle_dependencies = com.google.firebase:firebase-messaging:23.4.1
android.add_gradle_repositories = google(), mavenCentral()
