[app]
title = Prayer Test
package.name = prayertest
package.domain = com.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

# SADE ve GÜVENLİ
requirements = kivy,pyjnius,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WAKE_LOCK,VIBRATE,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE


[buildozer]
log_level = 2
warn_on_root = 1

# ================= ANDROID =================
android.api = 34
android.minapi = 24

android.ndk = 25b
android.build_tools_version = 34.0.0

android.accept_sdk_license = True
android.enable_androidx = True

# TEK SATIR – ÇAKIŞMA YOK
android.gradle_dependencies = com.google.firebase:firebase-messaging:23.4.1

android.add_gradle_repositories = google(), mavenCentral()

# FCM default icon & color
android.meta_data = \
    com.google.firebase.messaging.default_notification_icon=@android:drawable/ic_dialog_info, \
    com.google.firebase.messaging.default_notification_color=#FF6200EE

android.archs = arm64-v8a, armeabi-v7a
