from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.utils import platform
import requests
import traceback

# -------------------------------------------------
# ANDROID IMPORTLARI
# -------------------------------------------------
if platform == "android":
    from android.runnable import run_on_ui_thread
    from jnius import autoclass, PythonJavaClass, java_method

    PythonActivity = autoclass("org.kivy.android.PythonActivity")
    FirebaseApp = autoclass("com.google.firebase.FirebaseApp")
    FirebaseMessaging = autoclass("com.google.firebase.messaging.FirebaseMessaging")
else:
    # Android değilse decorator boş geçsin
    def run_on_ui_thread(func):
        return func


class FCMTestApp(App):
    fcm_token = None
    firebase_initialized = False

    def build(self):
        self.layout = BoxLayout(
            orientation="vertical",
            padding=20,
            spacing=10
        )

        self.status_label = Label(
            text="FCM Test\n\nFirebase baslatiliyor...",
            size_hint=(1, 0.6),
            halign="center",
            valign="middle",
            font_size="16sp"
        )
        self.status_label.bind(size=self.status_label.setter("text_size"))

        btn_token = Button(
            text="Token Al",
            size_hint=(1, 0.1),
            font_size="18sp"
        )
        btn_token.bind(on_press=lambda x: self.get_fcm_token())

        btn_register = Button(
            text="Backend Kayit",
            size_hint=(1, 0.1),
            font_size="18sp"
        )
        btn_register.bind(on_press=lambda x: self.register_to_backend())

        btn_instant = Button(
            text="Anlik Test",
            size_hint=(1, 0.1),
            font_size="18sp"
        )
        btn_instant.bind(on_press=lambda x: self.test_notification("instant"))

        btn_delayed = Button(
            text="10 Saniye Gecikmeli",
            size_hint=(1, 0.1),
            font_size="18sp"
        )
        btn_delayed.bind(on_press=lambda x: self.test_notification("10s"))

        self.layout.add_widget(self.status_label)
        self.layout.add_widget(btn_token)
        self.layout.add_widget(btn_register)
        self.layout.add_widget(btn_instant)
        self.layout.add_widget(btn_delayed)

        if platform == "android":
            Clock.schedule_once(self.initialize_firebase, 1)
        else:
            self.status_label.text = "Bu uygulama sadece Android'de calisir"

        return self.layout

    # -------------------------------------------------
    # FIREBASE INIT (HATASIZ)
    # -------------------------------------------------
    @run_on_ui_thread
    def initialize_firebase(self, *args):
        if platform != "android":
            return

        try:
            self.status_label.text = "Firebase baslatiliyor..."

            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()

            # ❗ getApps KULLANILMAZ
            try:
                FirebaseApp.initializeApp(context)
                self.status_label.text = "Firebase baslatildi!\nToken Al basin"
            except Exception:
                # Zaten başlatılmış olabilir (normal)
                self.status_label.text = "Firebase hazir!\nToken Al basin"

            self.firebase_initialized = True

        except Exception as e:
            self.status_label.text = "Firebase Hatasi!"
            print("Firebase init error:")
            print(traceback.format_exc())

    # -------------------------------------------------
    # TOKEN ALMA
    # -------------------------------------------------
    @run_on_ui_thread
    def get_fcm_token(self):
        if platform != "android":
            self.status_label.text = "Sadece Android'de calisir"
            return

        if not self.firebase_initialized:
            self.status_label.text = "Firebase hazir degil, bekleyin..."
            Clock.schedule_once(lambda dt: self.get_fcm_token(), 2)
            return

        try:
            self.status_label.text = "Token aliniyor..."
            messaging = FirebaseMessaging.getInstance()
            task = messaging.getToken()

            class TokenListener(PythonJavaClass):
                __javainterfaces__ = ["com/google/android/gms/tasks/OnCompleteListener"]

                def __init__(self, app):
                    super().__init__()
                    self.app = app

                @java_method("(Lcom/google/android/gms/tasks/Task;)V")
                def onComplete(self, task):
                    if task.isSuccessful():
                        token = str(task.getResult())
                        self.app.fcm_token = token
                        self.app.status_label.text = (
                            "Token alindi:\n"
                            f"{token[:60]}...\n\n"
                            "Backend Kayit yapabilirsiniz"
                        )
                        print("FCM TOKEN:", token)
                    else:
                        self.app.status_label.text = "Token alinamadi"

            task.addOnCompleteListener(TokenListener(self))

        except Exception:
            self.status_label.text = "Token hatasi!"
            print(traceback.format_exc())

    # -------------------------------------------------
    # BACKEND KAYIT
    # -------------------------------------------------
    def register_to_backend(self):
        if not self.fcm_token:
            self.status_label.text = "Once token alin!"
            return

        try:
            BACKEND_URL = "http://192.168.1.6:8000"

            response = requests.post(
                f"{BACKEND_URL}/register",
                json={"fcm_token": self.fcm_token},
                timeout=10
            )

            if response.status_code == 200:
                self.status_label.text = "Backend kaydi basarili!"
            else:
                self.status_label.text = f"Hata: {response.status_code}"

        except Exception:
            self.status_label.text = "Backend baglanti hatasi"
            print(traceback.format_exc())

    # -------------------------------------------------
    # TEST BILDIRIM
    # -------------------------------------------------
    def test_notification(self, test_type):
        try:
            BACKEND_URL = "http://192.168.1.6:8000"
            requests.post(f"{BACKEND_URL}/test/{test_type}", timeout=5)
            self.status_label.text = "Bildirim gonderildi"
        except Exception:
            self.status_label.text = "Bildirim hatasi"


if __name__ == "__main__":
    FCMTestApp().run()