[app]
# ================= APP INFO =================
title = Prayer Test
package.name = prayertest
package.domain = com.test

# ================= SOURCE =================
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

# ================= VERSION =================
version = 1.0

# ================= PYTHON =================
requirements = kivy,pyjnius,requests

# ================= UI =================
orientation = portrait
fullscreen = 0


[buildozer]
# ================= BUILD =================
log_level = 2
warn_on_root = 1


# ================= ANDROID =================
android.permissions = INTERNET,WAKE_LOCK,VIBRATE,POST_NOTIFICATIONS,RECEIVE_BOOT_COMPLETED

android.api = 34
android.minapi = 24
android.ndk = 25b

android.accept_sdk_license = True
android.enable_androidx = True

# ================= FIREBASE =================
android.gradle_dependencies = \
    com.google.firebase:firebase-messaging:23.4.1

android.add_gradle_repositories = google(), mavenCentral()

android.add_src = google-services.json

# Firebase plugin hook
android.add_gradle_files = android.gradle

# ================= MISC =================
android.gradle_build_features = buildConfig
