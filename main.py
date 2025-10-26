%%writefile main.py
# main_app.py - исправленная версия
import base64
import requests
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivy.clock import Clock
from kivy.metrics import dp

class LicenseManager:
    def decrypt_license(self, encrypted_key):
        """Расшифровка лицензионного ключа"""
        try:
            print(f"🔍 Decrypting: {encrypted_key}")
            
            if not encrypted_key.startswith("Karich-"):
                raise ValueError("❌ Key must start with 'Karich-'")
            
            # Убираем форматирование
            clean_key = encrypted_key.replace('Karich-', '').replace('-', '')
            print(f"🔍 Clean key: {clean_key}")
            
            # Восстанавливаем base64
            for padding in ['', '=', '==', '===']:
                try:
                    full_key = clean_key + padding
                    decoded_bytes = base64.b64decode(full_key)
                    original_key = decoded_bytes.decode('utf-8')
                    print(f"✅ Decoded: {original_key}")
                    return original_key
                except Exception as e:
                    continue
            
            raise ValueError("❌ Invalid license key format")
            
        except Exception as e:
            raise ValueError(f"❌ Decryption failed: {str(e)}")

class KeyAuth:
    def __init__(self, name, ownerid, version):
        self.name = name
        self.ownerid = ownerid
        self.version = version
        self.session_id = None
        
    def init(self):
        try:
            data = {
                'type': 'init',
                'name': self.name,
                'ownerid': self.ownerid,
                'ver': self.version
            }
            
            response = requests.post('https://keyauth.win/api/1.2/', data=data, timeout=10)
            result = response.json()
            
            if result['success']:
                self.session_id = result['sessionid']
                return True, "✅ Connected to license server"
            else:
                return False, "❌ Connection failed"
                
        except Exception as e:
            return False, f"❌ Network error"
    
    def license(self, key):
        try:
            print(f"🔍 Checking KeyAuth for: {key}")
            data = {
                'type': 'license',
                'key': key,
                'name': self.name,
                'ownerid': self.ownerid,
                'sessionid': self.session_id
            }
            
            response = requests.post('https://keyauth.win/api/1.2/', data=data, timeout=10)
            result = response.json()
            
            if result['success']:
                return True, "✅ License verified successfully!"
            else:
                return False, f"❌ {result.get('message', 'Invalid license key')}"
                
        except Exception as e:
            return False, f"❌ Verification failed"

class AuthScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.license_manager = LicenseManager()
        self.auth = KeyAuth("Hernya", "fHgp2uewcP", "1.0")
        self.dialog = None
        
        # Главный layout
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(15)
        )
        
        # Карточка авторизации
        card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(25),
            size_hint=(None, None),
            size=(dp(340), dp(500)),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            elevation=4
        )
        
        # Заголовок
        title = MDLabel(
            text="🔐 Hernya Pro",
            halign="center",
            theme_text_color="Primary",
            font_style="H4",
            bold=True
        )
        card.add_widget(title)
        
        # Инструкция
        instruction = MDLabel(
            text="Enter your encrypted license key",
            halign="center",
            theme_text_color="Secondary",
            font_style="Body2"
        )
        card.add_widget(instruction)
        
        # Поле для ввода
        self.key_input = MDTextField(
            hint_text="Karich-XXXXX-XXXXX-XXXXX",
            mode="rectangle",
            size_hint_x=0.9,
            height=dp(50),
            pos_hint={"center_x": 0.5},
            helper_text="Enter key received from seller",
            helper_text_mode="persistent"
        )
        card.add_widget(self.key_input)
        
        # Кнопка активации
        self.activate_btn = MDRaisedButton(
            text="ACTIVATE LICENSE",
            size_hint_x=0.8,
            height=dp(50),
            pos_hint={"center_x": 0.5},
            md_bg_color=(0.2, 0.5, 0.9, 1),
            font_size='16sp'
        )
        self.activate_btn.bind(on_press=self.activate_license)
        card.add_widget(self.activate_btn)
        
        # Статус
        self.status_label = MDLabel(
            text="Ready to activate your license",
            halign="center",
            theme_text_color="Hint",
            font_style="Body1"
        )
        card.add_widget(self.status_label)
        
        main_layout.add_widget(card)
        self.add_widget(main_layout)
        
        Clock.schedule_once(self.initialize_auth, 1)
    
    def show_dialog(self, title, text):
        """Показать диалоговое окно"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            title=title,
            text=text,
            size_hint=(0.8, 0.4)
        )
        self.dialog.open()
    
    def initialize_auth(self, dt):
        """Инициализация KeyAuth"""
        success, message = self.auth.init()
        self.status_label.text = message
        if success:
            self.status_label.theme_text_color = "Primary"
        else:
            self.status_label.theme_text_color = "Error"
    
    def activate_license(self, instance):
        """Активация лицензии"""
        encrypted_key = self.key_input.text.strip()
        
        if not encrypted_key:
            self.show_dialog("Error", "❌ Please enter a license key")
            return
            
        if not encrypted_key.startswith("Karich-"):
            self.show_dialog("Error", "❌ Key must start with 'Karich-'")
            return
        
        self.activate_btn.disabled = True
        self.activate_btn.text = "PROCESSING..."
        
        try:
            # Расшифровываем ключ
            decrypted_key = self.license_manager.decrypt_license(encrypted_key)
            self.status_label.text = "🔓 Key decrypted successfully!"
            self.status_label.theme_text_color = "Primary"
            
            # Проверяем через KeyAuth
            Clock.schedule_once(lambda dt: self.check_keyauth(decrypted_key), 1)
            
        except Exception as e:
            self.status_label.text = "❌ Activation failed"
            self.status_label.theme_text_color = "Error"
            self.activate_btn.disabled = False
            self.activate_btn.text = "ACTIVATE LICENSE"
            self.show_dialog("Error", str(e))
    
    def check_keyauth(self, decrypted_key):
        """Проверка ключа через KeyAuth"""
        success, message = self.auth.license(decrypted_key)
        
        if success:
            self.status_label.text = "✅ License activated!"
            self.activate_btn.md_bg_color = (0, 0.7, 0, 1)
            self.activate_btn.text = "SUCCESS!"
            self.show_dialog("Success", "🎉 License activated successfully!\n\nYou now have access to all premium features.")
            Clock.schedule_once(self.go_to_main, 3)
        else:
            self.status_label.text = "❌ Activation failed"
            self.status_label.theme_text_color = "Error"
            self.activate_btn.disabled = False
            self.activate_btn.text = "ACTIVATE LICENSE"
            self.show_dialog("Error", message)
    
    def go_to_main(self, dt):
        """Переход к основному приложению"""
        self.manager.current = 'main'

class MainAppScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        main_layout = MDBoxLayout(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(20)
        )
        
        # Приветственная карточка
        welcome_card = MDCard(
            orientation="vertical",
            padding=dp(30),
            spacing=dp(20),
            elevation=4
        )
        
        welcome_card.add_widget(MDLabel(
            text="🎉 Welcome to Hernya Pro!",
            halign="center",
            theme_text_color="Primary", 
            font_style="H4",
            bold=True
        ))
        
        welcome_card.add_widget(MDLabel(
            text="Premium Edition • Full Access",
            halign="center",
            theme_text_color="Secondary",
            font_style="Subtitle1"
        ))
        
        main_layout.add_widget(welcome_card)
        
        # Функции приложения
        features_card = MDCard(
            orientation="vertical",
            padding=dp(25),
            spacing=dp(15),
            elevation=4
        )
        
        features_card.add_widget(MDLabel(
            text="🚀 Premium Features",
            theme_text_color="Primary",
            font_style="H5",
            bold=True
        ))
        
        features = [
            "• High Performance Mode",
            "• Advanced Security Tools", 
            "• Analytics Dashboard",
            "• Custom Themes",
            "• Priority Support",
            "• Lifetime Updates"
        ]
        
        for feature in features:
            feature_label = MDLabel(
                text=feature,
                theme_text_color="Secondary",
                font_style="Body1"
            )
            features_card.add_widget(feature_label)
        
        main_layout.add_widget(features_card)
        
        self.add_widget(main_layout)

class HernyaApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.title = "Hernya Pro"
        
        sm = MDScreenManager()
        sm.add_widget(AuthScreen(name='auth'))
        sm.add_widget(MainAppScreen(name='main'))
        return sm

if __name__ == '__main__':
    HernyaApp().run()
