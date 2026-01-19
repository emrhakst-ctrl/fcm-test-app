[app]
title = Prayer Test
package.name = prayertest
package.domain = com.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,pyjnius,android,requests
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

android.permissions = INTERNET,WAKE_LOCK,VIBRATE,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED
android.api = 33
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 34.0.0
android.accept_sdk_license = True
android.gradle_dependencies = com.google.firebase:firebase-messaging:23.4.0
android.enable_androidx = True
android.gradle_repositories = google(), mavenCentral()
p4a.gradle_dependencies = classpath 'com.google.gms:google-services:4.4.0'
