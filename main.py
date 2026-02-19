from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.utils import platform
from kivy.clock import Clock


ONESIGNAL_APP_ID = "BURAYA_ONESIGNAL_APP_ID_YAZ"


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", spacing=20, padding=40, **kwargs)

        self.status = Label(text="OneSignal Test", size_hint=(1, 0.2))
        self.add_widget(self.status)

        btn = Button(text="OneSignal Başlat", size_hint=(1, 0.2))
        btn.bind(on_press=self.init_onesignal)
        self.add_widget(btn)

        btn2 = Button(text="Player ID Göster", size_hint=(1, 0.2))
        btn2.bind(on_press=self.get_player_id)
        self.add_widget(btn2)

    def init_onesignal(self, instance):
        if platform != "android":
            self.status.text = "Android değil"
            return

        try:
            from jnius import autoclass

            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            OneSignal = autoclass("com.onesignal.OneSignal")

            context = PythonActivity.mActivity

            OneSignal.initWithContext(context)
            OneSignal.setAppId(ONESIGNAL_APP_ID)

            # Android 13+ izin
            OneSignal.promptForPushNotifications()

            self.status.text = "OneSignal Başlatıldı ✅"

        except Exception as e:
            self.status.text = f"Hata: {str(e)}"
            print("ONESIGNAL INIT ERROR:", e)

    def get_player_id(self, instance):
        if platform != "android":
            self.status.text = "Android değil"
            return

        try:
            from jnius import autoclass

            OneSignal = autoclass("com.onesignal.OneSignal")

            device_state = OneSignal.getDeviceState()

            if device_state:
                player_id = device_state.getUserId()
                self.status.text = f"Player ID:\n{player_id}"
                print("PLAYER ID:", player_id)
            else:
                self.status.text = "Device state boş"

        except Exception as e:
            self.status.text = f"Hata: {str(e)}"
            print("PLAYER ID ERROR:", e)


class OneSignalApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    OneSignalApp().run()