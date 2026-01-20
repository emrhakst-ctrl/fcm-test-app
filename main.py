from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.utils import platform
from jnius import autoclass

class FCMTestApp(App):

    def build(self):
        self.label = Label(
            text="Uygulama calisiyor.\nBildirim bekleniyor...",
            halign="center"
        )
        return BoxLayout(padding=20, children=[self.label])

    def on_start(self):
        if platform == "android":
            Clock.schedule_once(self.show_info, 1)

    def show_info(self, dt):
        try:
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            FirebaseApp = autoclass("com.google.firebase.FirebaseApp")

            activity = PythonActivity.mActivity
            FirebaseApp.initializeApp(activity)

            self.label.text = "Firebase aktif.\nFCM hazir."
        except Exception as e:
            self.label.text = "Firebase hata:\n" + str(e)

if __name__ == "__main__":
    FCMTestApp().run()
