from PIL import Image
from kivy.base import EventLoop
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from pyzbar.pyzbar import decode
from camera4kivy import Preview
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy import utils
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class Scan_Analyze(Preview):
    extracted_data = ObjectProperty(None)

    def analyze_pixels_callback(self, pixels, image_size, image_pos, scale, mirror):

        pimage = Image.frombytes(mode='RGBA', size=image_size, data=pixels)
        list_of_all_barcodes = decode(pimage)

        if list_of_all_barcodes:
            if self.extracted_data:
                self.extracted_data(list_of_all_barcodes[0])
            else:
                print("NOt found")


class ExpireYear(MDTextField):
    def insert_text(self, substring, from_undo=False):
        if substring.isdigit():
            if len(self.text) == 0 and substring == "0":
                return
            elif len(self.text) >= 4:
                return
            else:
                return super(ExpireYear, self).insert_text(substring, from_undo=from_undo)


class ExpireMonth(MDTextField):
    def insert_text(self, substring, from_undo=False):
        if substring.isdigit():
            if len(self.text) == 0 and substring == "0":
                return
            elif len(self.text) >= 1:
                return
            else:
                return super(ExpireMonth, self).insert_text(substring, from_undo=from_undo)


class NumberOnlyField(MDTextField):
    def insert_text(self, substring, from_undo=False):
        if substring.isdigit():
            if len(self.text) == 0 and substring == "0":
                return
            else:
                return super(NumberOnlyField, self).insert_text(substring, from_undo=from_undo)


class Tab(MDBoxLayout, MDTabsBase):
    pass


class MainApp(MDApp):
    size_x, size_y = Window.size

    # screen
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # Cash data
    product_sold = StringProperty("0")
    today_amount = StringProperty("0")
    total_amount = StringProperty("0")

    # product details
    product_name = StringProperty("")
    product_price = StringProperty("")
    product_quantity = StringProperty("")
    product_barcode = StringProperty("")
    product_exp_year = StringProperty("")
    product_exp_month = StringProperty("")

    def on_start(self):
        self.keyboard_hooker()

    def keyboard_hooker(self, *args):
        EventLoop.window.bind(on_keyboard=self.hook_keyboard)

    def hook_keyboard(self, window, key, *largs):
        print(self.screens_size)
        if key == 27 and self.screens_size > 0:
            print(f"your were in {self.current}")
            last_screens = self.current
            self.screens.remove(last_screens)
            print(self.screens)
            self.screens_size = len(self.screens) - 1
            self.current = self.screens[len(self.screens) - 1]
            self.screen_capture(self.current)
            return True
        elif key == 27 and self.screens_size == 0:
            toast('Press Home button!')
            return True

    """
    
        CAMERA SCAN FUNCTION
    
    """

    def on_kv_post(self):
        self.root.ids.preview.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)
        print("connected")

    def stop_camera(self):
        self.root.ids.preview.disconnect_camera()

    @mainthread
    def get_barcode(self, result):
        barcode = str(result.data)
        code_type = str(result.type)
        print(barcode)
        if barcode:
            if code_type != "QRCODE":
                barcode = barcode.replace("b", "").replace("'", "")

                self.product_barcode = barcode

                self.root.ids.result_preview.text = barcode

    """

        screen functions

    """

    def screen_capture(self, screen):
        sm = self.root
        sm.current = screen
        if screen in self.screens:
            pass
        else:
            self.screens.append(screen)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        print(f'size {self.screens_size}')
        print(f'current screen {screen}')

    def screen_leave(self):
        print(f"your were in {self.current}")
        last_screens = self.current
        self.screens.remove(last_screens)
        print(self.screens)
        self.screens_size = len(self.screens) - 1
        self.current = self.screens[len(self.screens) - 1]
        self.screen_capture(self.current)

    def build(self):
        pass


MainApp().run()
