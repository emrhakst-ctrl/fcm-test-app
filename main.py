from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from android.runnable import run_on_ui_thread
from jnius import autoclass, PythonJavaClass, java_method
import requests
import traceback

PythonActivity = autoclass('org.kivy.android.PythonActivity')
FirebaseApp = autoclass('com.google.firebase.FirebaseApp')
FirebaseMessaging = autoclass('com.google.firebase.messaging.FirebaseMessaging')

class FCMTestApp(App):
    fcm_token = None
    firebase_initialized = False
    
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.status_label = Label(
            text='FCM Test\\n\\nFirebase baslatiliyor...',
            size_hint=(1, 0.6),
            halign='center',
            valign='middle',
            font_size='16sp'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        
        token_btn = Button(text='Token Al', size_hint=(1, 0.1), font_size='18sp')
        token_btn.bind(on_press=lambda x: self.get_fcm_token())
        
        register_btn = Button(text='Backend Kayit', size_hint=(1, 0.1), font_size='18sp')
        register_btn.bind(on_press=lambda x: self.register_to_backend())
        
        instant_btn = Button(text='Aninda Test', size_hint=(1, 0.1), font_size='18sp')
        instant_btn.bind(on_press=lambda x: self.test_notification('instant'))
        
        delayed_btn = Button(text='10 Saniye', size_hint=(1, 0.1), font_size='18sp')
        delayed_btn.bind(on_press=lambda x: self.test_notification('10s'))
        
        self.layout.add_widget(self.status_label)
        self.layout.add_widget(token_btn)
        self.layout.add_widget(register_btn)
        self.layout.add_widget(instant_btn)
        self.layout.add_widget(delayed_btn)
        
        Clock.schedule_once(lambda dt: self.initialize_firebase(), 1)
        return self.layout
    
    @run_on_ui_thread
    def initialize_firebase(self):
        try:
            self.status_label.text = "Firebase baslatiliyor..."
            activity = PythonActivity.mActivity
            context = activity.getApplicationContext()
            apps = FirebaseApp.getApps(context)
            
            if len(apps) == 0:
                FirebaseApp.initializeApp(context)
            
            self.status_label.text = "Firebase hazir!\\nToken Al basin"
            self.firebase_initialized = True
        except Exception as e:
            self.status_label.text = f"Hata:\\n{str(e)}"
            print(traceback.format_exc())
    
    @run_on_ui_thread
    def get_fcm_token(self):
        try:
            if not self.firebase_initialized:
                self.status_label.text = "Firebase henuz hazir degil"
                Clock.schedule_once(lambda dt: self.get_fcm_token(), 2)
                return
            
            self.status_label.text = "Token aliniyor..."
            messaging = FirebaseMessaging.getInstance()
            task = messaging.getToken()
            
            class TokenListener(PythonJavaClass):
                __javainterfaces__ = ['com/google/android/gms/tasks/OnCompleteListener']
                
                def __init__(self, app):
                    super().__init__()
                    self.app = app
                
                @java_method('(Lcom/google/android/gms/tasks/Task;)V')
                def onComplete(self, task):
                    if task.isSuccessful():
                        token = task.getResult()
                        self.app.fcm_token = str(token)
                        short = self.app.fcm_token[:60] + "..."
                        self.app.status_label.text = f"Token alindi:\\n{short}\\n\\nBackend Kayit yapin"
                        print(f"FCM Token: {self.app.fcm_token}")
                    else:
                        self.app.status_label.text = "Token alinamadi"
            
            task.addOnCompleteListener(TokenListener(self))
        except Exception as e:
            self.status_label.text = f"Hata:\\n{str(e)}"
            print(traceback.format_exc())
    
    def register_to_backend(self):
        if not self.fcm_token:
            self.status_label.text = "Once token alin"
            return
        
        try:
            BACKEND_URL = "http://192.168.1.6:8000"
            
            response = requests.post(
                f"{BACKEND_URL}/register",
                json={"fcm_token": self.fcm_token},
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                self.status_label.text = f"Kayit basarili!\\nToplam cihaz: {data.get('total_devices')}"
            else:
                self.status_label.text = f"Hata: {response.status_code}"
        except requests.exceptions.Timeout:
            self.status_label.text = "Zaman asimi\\nIP kontrol edin"
        except requests.exceptions.ConnectionError:
            self.status_label.text = "Baglanti hatasi\\nBackend calismiyor"
        except Exception as e:
            self.status_label.text = f"Hata:\\n{str(e)[:50]}"
    
    def test_notification(self, test_type):
        try:
            BACKEND_URL = "http://192.168.1.6:8000"
            
            response = requests.post(f"{BACKEND_URL}/test/{test_type}", timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                if test_type == 'instant':
                    self.status_label.text = "Bildirim gonderildi!\\nKontrol edin"
                else:
                    self.status_label.text = f"Zamanlandi\\nSaat: {data.get('scheduled_time')}"
            else:
                self.status_label.text = f"Hata: {response.status_code}"
        except Exception as e:
            self.status_label.text = f"Hata:\\n{str(e)[:50]}"

if __name__ == '__main__':
    FCMTestApp().run()
