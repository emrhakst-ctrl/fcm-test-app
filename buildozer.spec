[app]
title = Prayer Test
package.name = prayertest
package.domain = com.test
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 1.0
requirements = python3,kivy,pyjnius,android,requests
orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WAKE_LOCK,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE,VIBRATE

[buildozer]
log_level = 2
warn_on_root = 1

# Android ayarları
android.api = 33
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.enable_androidx = True

# Firebase için Gradle
android.gradle_dependencies = com.google.firebase:firebase-messaging:23.4.0
android.gradle_repositories = google(), mavenCentral()

# Google Services plugin
p4a.gradle_dependencies = classpath 'com.google.gms:google-services:4.4.0'

# Meta data (bildirim kanalı)
android.meta_data = com.google.firebase.messaging.default_notification_channel_id=default_channel
