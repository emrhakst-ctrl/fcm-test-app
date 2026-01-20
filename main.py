from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
import requests

class FCMTestApp(App):
    fcm_token = "test-token-123"  # Başlangıç için sahte token
    
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.status_label = Label(
            text='FCM Test Uygulamasi\\n\\nHazir!',
            size_hint=(1, 0.6),
            halign='center',
            valign='middle',
            font_size='16sp'
        )
        self.status_label.bind(size=self.status_label.setter('text_size'))
        
        token_btn = Button(
            text='Firebase Token Al',
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        token_btn.bind(on_press=self.get_firebase_token)
        
        register_btn = Button(
            text='Backend Kayit',
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        register_btn.bind(on_press=self.register_backend)
        
        instant_btn = Button(
            text='Aninda Bildirim',
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        instant_btn.bind(on_press=lambda x: self.test_notif('instant'))
        
        delayed_btn = Button(
            text='10 Saniye Sonra',
            size_hint=(1, 0.1),
            font_size='18sp'
        )
        delayed_btn.bind(on_press=lambda x: self.test_notif('10s'))
        
        layout.add_widget(self.status_label)
        layout.add_widget(token_btn)
        layout.add_widget(register_btn)
        layout.add_widget(instant_btn)
        layout.add_widget(delayed_btn)
        
        # Firebase'i arka planda başlat
        Clock.schedule_once(self.init_firebase, 2)
        
        return layout
    
    def init_firebase(self, dt):
        """Firebase'i güvenli başlat"""
        try:
            from jnius import autoclass
            
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            FirebaseApp = autoclass('com.google.firebase.FirebaseApp')
            
            activity = PythonActivity.mActivity
            
            # Başlatmayı dene
            try:
                FirebaseApp.initializeApp(activity)
            except:
                pass  # Zaten başlatılmış
            
            self.status_label.text = 'Firebase hazir\\n\\n"Token Al" butonuna basin'
            
        except Exception as e:
            self.status_label.text = f'Firebase yukleniyor...\\n\\nBir saniye bekleyin'
            # 3 saniye sonra tekrar dene
            Clock.schedule_once(self.init_firebase, 3)
    
    def get_firebase_token(self, instance):
        """FCM Token al"""
        self.status_label.text = 'Token aliniyor...'
        
        def _get_token():
            try:
                from jnius import autoclass, PythonJavaClass, java_method
                
                FirebaseMessaging = autoclass('com.google.firebase.messaging.FirebaseMessaging')
                
                messaging = FirebaseMessaging.getInstance()
                task = messaging.getToken()
                
                # Callback class
                class TokenCallback(PythonJavaClass):
                    __javainterfaces__ = ['com/google/android/gms/tasks/OnCompleteListener']
                    
                    def __init__(self, app_ref):
                        super().__init__()
                        self.app = app_ref
                    
                    @java_method('(Lcom/google/android/gms/tasks/Task;)V')
                    def onComplete(self, task):
                        if task.isSuccessful():
                            token = str(task.getResult())
                            self.app.fcm_token = token
                            short = token[:50] + "..."
                            self.app.status_label.text = f'Token alindi!\\n\\n{short}\\n\\nSimdi "Backend Kayit" yapin'
                        else:
                            self.app.status_label.text = 'Token alinamadi\\nTekrar deneyin'
                
                callback = TokenCallback(self)
                task.addOnCompleteListener(callback)
                
            except Exception as e:
                self.status_label.text = f'Hata: {str(e)[:100]}'
        
        # 0.5 saniye sonra çalıştır
        Clock.schedule_once(lambda dt: _get_token(), 0.5)
    
    def register_backend(self, instance):
        """Backend'e kayıt"""
        if not self.fcm_token or self.fcm_token == "test-token-123":
            self.status_label.text = 'Once token alin!'
            return
        
        self.status_label.text = 'Backend kayit yapiliyor...'
        
        def _register():
            try:
                # BURAYA KENDİ IP ADRESİNİZİ YAZIN!
                url = "http://192.168.1.6:8000/register"
                
                response = requests.post(
                    url,
                    json={"fcm_token": self.fcm_token},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json()
                    total = data.get('total_devices', '?')
                    self.status_label.text = f'Kayit basarili!\\n\\nToplam cihaz: {total}\\n\\nSimdi test edin'
                else:
                    self.status_label.text = f'Kayit hatasi\\nKod: {response.status_code}'
                    
            except requests.exceptions.ConnectionError:
                self.status_label.text = 'Backend baglanti hatasi\\n\\nIP adresini kontrol edin\\nBackend acik mi?'
            except requests.exceptions.Timeout:
                self.status_label.text = 'Zaman asimi\\n\\nBackend cevap vermiyor'
            except Exception as e:
                self.status_label.text = f'Hata:\\n{str(e)[:100]}'
        
        Clock.schedule_once(lambda dt: _register(), 0.1)
    
    def test_notif(self, test_type):
        """Test bildirimi gönder"""
        self.status_label.text = f'{test_type} bildirimi gonderiliyor...'
        
        def _send():
            try:
                # BURAYA KENDİ IP ADRESİNİZİ YAZIN!
                url = f"http://192.168.1.6:8000/test/{test_type}"
                
                response = requests.post(url, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    if test_type == 'instant':
                        self.status_label.text = 'Aninda bildirim gonderildi!\\n\\nTelefonu kontrol edin'
                    else:
                        saat = data.get('scheduled_time', '?')
                        self.status_label.text = f'10 saniye sonra\\ngelecek!\\n\\nBeklenen: {saat}'
                else:
                    self.status_label.text = f'Test hatasi\\nKod: {response.status_code}'
                    
            except Exception as e:
                self.status_label.text = f'Baglanti hatasi:\\n{str(e)[:80]}'
        
        Clock.schedule_once(lambda dt: _send(), 0.1)

if __name__ == '__main__':
    FCMTestApp().run()
