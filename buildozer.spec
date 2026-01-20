[app]
title = Prayer Test
package.name = prayertest
package.domain = com.test

source.dir = .
source.include_exts = py,png,jpg,kv,json

version = 1.0
requirements = kivy,pyjnius,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WAKE_LOCK,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED,ACCESS_NETWORK_STATE

[buildozer]
log_level = 2
warn_on_root = 1

android.api = 34
android.minapi = 24
android.ndk = 25b
android.build_tools_version = 34.0.0

android.accept_sdk_license = True
android.enable_androidx = True

# 🔥 Firebase Messaging
android.gradle_dependencies = com.google.firebase:firebase-messaging:23.4.1

android.add_gradle_repositories = google(), mavenCentral()

# 🔥 Java servis ekle
android.add_src = %(source.dir)s/android/src

# 🔥 Manifest'e servis ekle
android.manifest_extra = \
    <service \
        android:name="com.test.prayertest.MyFirebaseMessagingService" \
        android:exported="false"> \
        <intent-filter> \
            <action android:name="com.google.firebase.MESSAGING_EVENT"/> \
        </intent-filter> \
    </service>
