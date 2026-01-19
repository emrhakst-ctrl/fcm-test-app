[app]

# Uygulama bilgileri
title = Prayer Test
package.name = prayertest
package.domain = com.test

# Kaynak dosyaları
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# Versiyon
version = 1.0

# Python gereksinimleri
requirements = python3,kivy==2.2.1,pyjnius,requests,urllib3,charset-normalizer,idna,certifi

# Uygulama ayarları
orientation = portrait
fullscreen = 0

# Android izinleri
android.permissions = INTERNET,WAKE_LOCK,VIBRATE,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE

# Opsiyonel: Icon ve presplash
# icon.filename = %(source.dir)s/icon.png
# presplash.filename = %(source.dir)s/presplash.png

[buildozer]

# Log seviyesi (2 = INFO)
log_level = 2
warn_on_root = 1

# Build klasörleri
# build_dir = ./.buildozer
# bin_dir = ./bin

# ============================================================
# ANDROID AYARLARI
# ============================================================

# Android API seviyeleri
android.api = 34
android.minapi = 24

# NDK versiyonu
android.ndk = 25b

# Build tools versiyonu
android.build_tools_version = 34.0.0

# SDK lisansını otomatik kabul et
android.accept_sdk_license = True

# AndroidX desteği (modern Android için gerekli)
android.enable_androidx = True

# Gradle bağımlılıkları
android.gradle_dependencies = com.google.firebase:firebase-messaging:23.4.1,androidx.core:core:1.12.0,com.google.android.gms:play-services-tasks:18.0.2

# Gradle repositories
android.add_gradle_repositories = google(), mavenCentral()

# Meta-data (Firebase için)
android.meta_data.icon = com.google.firebase.messaging.default_notification_icon=@android:drawable/ic_dialog_info
android.meta_data.color = com.google.firebase.messaging.default_notification_color=#FF6200EE

# CPU mimarileri (modern cihazlar için)
android.archs = arm64-v8a, armeabi-v7a

# Firebase servisi ekle
android.add_src = %(source.dir)s/android/src

# Manifest'e servis ekle
android.manifest_extra = <service android:name="com.test.prayertest.MyFirebaseMessagingService" android:exported="false"><intent-filter><action android:name="com.google.firebase.MESSAGING_EVENT" /></intent-filter></service>

# Google Services plugin ekle (Firebase için gerekli)
android.gradle_dependencies = com.google.gms:google-services:4.4.0

# p4a (python-for-android) ayarları
p4a.branch = develop

# Bootstrap (firebase için sdl2)
# p4a.bootstrap = sdl2

# Release için (opsiyonel - şimdilik debug kullanıyoruz)
# android.release_artifact = apk
# android.keystore = %(source.dir)s/keystore.jks
# android.keystore_alias = myalias

# Logcat filtreleme (opsiyonel)
# android.logcat_filters = *:S python:D

[buildozer:linux]
# Linux spesifik ayarlar (GitHub Actions için)
