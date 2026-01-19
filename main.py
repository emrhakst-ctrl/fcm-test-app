from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform
import requests
import traceback


def _fallback_run_on_ui_thread(func):
    return func


# Android'de run_on_ui_thread güvenli import
if platform == "android":
    try:
        from android.runnable import run_on_ui_thread  # type: ignore
    except Exception:
        run_on_ui_thread = _fallback_run_on_ui_thread
else:
    run_on_ui_thread = _fallback_run_on_ui_thread


class FCMTestApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fcm_token = None
        self.firebase_initialized = False

        # Lazy-loaded Java class refs
        self._PythonActivity = None
        self._FirebaseApp = None
        self._FirebaseMessaging = None
        self._PythonJavaClass = None
        self._java_method = None

    def build(self):
        self.layout = BoxLayout(orientation="vertical", padding=20, spacing=10)

        self.status_label = Label(
            text="FCM Test\n\nFirebase baslatiliyor...",
            size_hint=(1, 0.6),
            halign="center",
            valign="middle",
            font_size="16sp",
        )
        self.status_label.bind(size=self.status_label.setter("text_size"))

        token_btn = Button(
            text="Token Al",
            size_hint=(1, 0.1),
            font_size="18sp",
            background_color=(0.2, 0.6, 1, 1),
        )
        token_btn.bind(on_press=lambda x: self.get_fcm_token())

        register_btn = Button(
            text="Backend Kayit",
            size_hint=(1, 0.1),
            font_size="18sp",
            background_color=(0.2, 0.8, 0.4, 1),
        )
        register_btn.bind(on_press=lambda x: self.register_to_backend())

        instant_btn = Button(
            text="Anlik Test",
            size_hint=(1, 0.1),
            font_size="18sp",
            background_color=(1, 0.6, 0.2, 1),
        )
        instant_btn.bind(on_press=lambda x: self.test_notification("instant"))

        delayed_btn = Button(
            text="10 Saniye Gecikmeli",
            size_hint=(1, 0.1),
            font_size="18sp",
            background_color=(0.8, 0.4, 0.8, 1),
        )
        delayed_btn.bind(on_press=lambda x: self.test_notification("10s"))

        self.layout.add_widget(self.status_label)
        self.layout.add_widget(token_btn)
        self.layout.add_widget(register_btn)
        self.layout.add_widget(instant_btn)
        self.layout.add_widget(delayed_btn)

        if platform == "android":
            Clock.schedule_once(lambda dt: self.initialize_firebase(), 1)
        else:
            self.status_label.text = "Bu uygulama sadece\nAndroid'de calisir"

        return self.layout

    # ---------- Lazy loader ----------
    def _load_android_classes(self):
        """Load jnius + Firebase classes only when needed (prevents startup crash)."""
        if platform != "android":
            return

        if self._PythonActivity is not None:
            return  # already loaded

        try:
            from jnius import autoclass, PythonJavaClass, java_method  # type: ignore

            self._PythonActivity = autoclass("org.kivy.android.PythonActivity")
            self._FirebaseApp = autoclass("com.google.firebase.FirebaseApp")
            self._FirebaseMessaging = autoclass("com.google.firebase.messaging.FirebaseMessaging")
            self._PythonJavaClass = PythonJavaClass
            self._java_method = java_method
        except Exception as e:
            # This is the key: show error instead of crashing app
            self.status_label.text = "JNI/Firebase yukleme hatasi:\n" + str(e)[:120]
            print("JNI/Firebase class load error:")
            print(traceback.format_exc())
            raise

    @run_on_ui_thread
    def initialize_firebase(self):
        try:
            if platform != "android":
                return

            self.status_label.text = "Firebase baslatiliyor..."

            # Load classes lazily
            self._load_android_classes()

            activity = self._PythonActivity.mActivity
            context = activity.getApplicationContext()

            apps = self._FirebaseApp.getApps(context)
            # getApps bazen Java list döndürür; güvenli kontrol:
            has_any = False
            try:
                has_any = apps is not None and len(apps) > 0
            except Exception:
                has_any = apps is not None

            if not has_any:
                self._FirebaseApp.initializeApp(context)
                self.status_label.text = "Firebase baslatildi!\nToken Al basin"
            else:
                self.status_label.text = "Firebase zaten hazir!\nToken Al basin"

            self.firebase_initialized = True

        except Exception as e:
            self.status_label.text = f"Firebase Hatasi:\n{str(e)[:120]}"
            print("Firebase initialization error:")
            print(traceback.format_exc())

    @run_on_ui_thread
    def get_fcm_token(self):
        try:
            if platform != "android":
                self.status_label.text = "Sadece Android'de\ncalisir"
                return

            # Ensure Firebase classes loaded (and firebase init attempted)
            if not self.firebase_initialized:
                self.status_label.text = "Firebase henuz hazir degil\nTekrar denenecek..."
                Clock.schedule_once(lambda dt: self.initialize_firebase(), 0.5)
                Clock.schedule_once(lambda dt: self.get_fcm_token(), 2)
                return

            self._load_android_classes()

            self.status_label.text = "Token aliniyor..."
            messaging = self._FirebaseMessaging.getInstance()
            task = messaging.getToken()

            PythonJavaClass = self._PythonJavaClass
            java_method = self._java_method

            app_ref = self

            class TokenListener(PythonJavaClass):
                __javainterfaces__ = ["com/google/android/gms/tasks/OnCompleteListener"]

                def __init__(self):
                    super().__init__()

                @java_method("(Lcom/google/android/gms/tasks/Task;)V")
                def onComplete(self, task):
                    try:
                        if task.isSuccessful():
                            token = task.getResult()
                            app_ref.fcm_token = str(token)
                            short = app_ref.fcm_token[:60] + "..."
                            app_ref.status_label.text = (
                                f"Token alindi:\n{short}\n\n"
                                "Simdi 'Backend Kayit' yapin"
                            )
                            print(f"FCM Token: {app_ref.fcm_token}")
                        else:
                            exception = task.getException()
                            error = str(exception) if exception else "Bilinmeyen hata"
                            app_ref.status_label.text = f"Token alinamadi:\n{error[:120]}"
                    except Exception as e:
                        app_ref.status_label.text = f"Listener hatasi:\n{str(e)[:120]}"
                        print(traceback.format_exc())

            task.addOnCompleteListener(TokenListener())

        except Exception as e:
            self.status_label.text = f"Token Hatasi:\n{str(e)[:120]}"
            print("Token error:")
            print(traceback.format_exc())

    def register_to_backend(self):
        if not self.fcm_token:
            self.status_label.text = "Once token alin!"
            return

        try:
            BACKEND_URL = "http://192.168.1.6:8000"
            self.status_label.text = "Backend'e kaydediliyor..."

            response = requests.post(
                f"{BACKEND_URL}/register",
                json={"fcm_token": self.fcm_token},
                timeout=10,
            )

            if response.status_code == 200:
                data = response.json()
                total = data.get("total_devices", "N/A")
                self.status_label.text = (
                    f"Kayit basarili!\n"
                    f"Toplam cihaz: {total}\n\n"
                    f"Simdi bildirim testi yapabilirsiniz"
                )
            else:
                self.status_label.text = f"Hata: {response.status_code}\n{response.text[:120]}"

        except requests.exceptions.Timeout:
            self.status_label.text = "Zaman asimi\nIP adresini kontrol edin"
        except requests.exceptions.ConnectionError:
            self.status_label.text = (
                "Baglanti hatasi\n"
                "Backend calismiyor olabilir\n"
                "veya IP yanlis"
            )
        except Exception as e:
            self.status_label.text = f"Hata:\n{str(e)[:120]}"
            print("Registration error:")
            print(traceback.format_exc())

    def test_notification(self, test_type):
        try:
            BACKEND_URL = "http://192.168.1.6:8000"
            self.status_label.text = f"Bildirim gonderiliyor ({test_type})..."

            response = requests.post(f"{BACKEND_URL}/test/{test_type}", timeout=10)

            if response.status_code == 200:
                data = response.json()
                if test_type == "instant":
                    self.status_label.text = (
                        "Anlik bildirim gonderildi!\n\n"
                        "Birkac saniye icinde\n"
                        "bildirim gelecek"
                    )
                else:
                    scheduled = data.get("scheduled_time", "N/A")
                    self.status_label.text = (
                        f"Bildirim zamanlandi!\n\n"
                        f"Saat: {scheduled}\n"
                        f"10 saniye sonra gelecek"
                    )
            else:
                self.status_label.text = f"Hata: {response.status_code}\n{response.text[:120]}"

        except requests.exceptions.Timeout:
            self.status_label.text = "Zaman asimi"
        except requests.exceptions.ConnectionError:
            self.status_label.text = "Backend'e baglanilmiyor"
        except Exception as e:
            self.status_label.text = f"Hata:\n{str(e)[:120]}"
            print("Notification test error:")
            print(traceback.format_exc())


if __name__ == "__main__":
    FCMTestApp().run()
