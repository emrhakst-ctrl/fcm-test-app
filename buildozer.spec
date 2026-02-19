[app]
title = OneSignalTest
package.name = onesignaltest
package.domain = com.test
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0

requirements = python3,kivy,pyjnius,android

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WAKE_LOCK,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE,VIBRATE

android.enable_androidx = True

android.gradle_dependencies = \
    com.onesignal:OneSignal:4.8.6, \
    com.google.firebase:firebase-messaging:23.2.1

android.gradle_repositories = google(),mavenCentral()

[buildozer]
log_level = 2
warn_on_root = 1

android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True