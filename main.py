import datetime

from PIL import Image
from kivy.base import EventLoop
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from pyzbar.pyzbar import decode
from camera4kivy import Preview
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy import utils
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField

from database import DataBase as DB

Window.keyboard_anim_args = {"d": .2, "t": "linear"}
Window.softinput_mode = "below_target"
Clock.max_iteration = 250

if utils.platform != 'android':
    Window.size = (412, 732)


class RowCard(MDCard):
    date = StringProperty("")
    icon = StringProperty("")
    cate = StringProperty("")
    name = StringProperty("")
    price = StringProperty("")

    def price_symb(self, cat, prc):
        if cat == "expenses":
            self.price = "-" + prc + "/="
        else:
            self.price = "+" + prc + "/="
        return self.price


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


class DictionaryProperty:
    pass


class MainApp(MDApp):
    size_x, size_y = Window.size

    # screen
    screens = ['home']
    screens_size = NumericProperty(len(screens) - 1)
    current = StringProperty(screens[len(screens) - 1])

    # Cash data
    product_sold = StringProperty("0")
    total_amount = StringProperty("0")
    date_frm = StringProperty(DB.date_format(DB()))
    today_sold = StringProperty("0")
    today_amount = StringProperty("0")

    # product details
    product_name = StringProperty("")
    product_price = StringProperty("")
    product_quantity = StringProperty("")
    product_barcode = StringProperty("")
    product_exp_year = StringProperty("")
    product_exp_month = StringProperty("")
    data = DictionaryProperty()

    # Selling data
    amount_sold = StringProperty("")
    quantity_sold = StringProperty("")

    def on_start(self):
        self.keyboard_hooker()
        self.works()

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
            PRODUCT FUNCTIONS
    
    """

    def save_product(self, product_name, product_price, product_quantity, product_barcode, product_exp_year,
                     product_exp_month):
        DB.save_product(DB(), product_name, product_price, product_quantity, product_barcode, product_exp_year,
                        product_exp_month)

    def caller_details(self):
        Clock.schedule_once(self.get_product_details, .2)

    def get_product_details(self, *args):
        product_id = self.root.ids.sell_preview.text
        self.data = DB.get_product(DB(), product_id)

        self.product_name = self.data["product_name"]
        self.product_price = self.data["product_price"]
        self.product_quantity = self.data["product_quantity"]
        self.product_barcode = self.data["product_barcode"]

        print(self.data)

    def amount_calc(self):
        qnty = self.root.ids.quantity_sell.text
        amnt = self.root.ids.sold_amount

        if qnty != "" and self.product_price != "":
            amnt.text = str(int(qnty) * int(self.product_price)) + "/="
        else:
            amnt.text = "0/="

    def sell_product(self):
        self.amount_sold = self.root.ids.sold_amount.text
        self.quantity_sold = self.root.ids.quantity_sell.text

        DB.sell_product(DB(), self.amount_sold, self.quantity_sold, self.product_barcode, self.product_name)

    """
            DATA FUNCTION
    
    """
    # small vars
    counter = 0
    count = 0

    def add_item(self, *args):
        self.root.ids.customers.data = {}
        main = DB.get_all_today(DB())
        print(main)
        if main:
            for i, y in main.items():
                self.today_amount = str(int(y["sold_amount"].replace("/=", "")) + int(self.today_amount))
                if self.counter < 9:
                    self.root.ids.customers.data.append(
                        {
                            "viewclass": "RowCard",
                            "icon": "shopping-outline",
                            "name": y["product_name"],
                            "price": f"{y['sold_amount']}/=",
                            "id": i
                        }
                    )
                else:
                    if self.count == 0:
                        self.root.ids.customers.data.append(
                            {
                                "viewclass": "More",
                                "icon": "dots-horizontal"
                            }
                        )
                        self.count = + 1
                self.counter = self.counter + 1
                self.today_sold = str(self.counter)
        else:
            img = self.root.ids.nodata
            img.source = "components/icons/file-plus.jpg"

    def stream_work(self, message):
        if True:
            print("working!")
            try:
                Clock.schedule_once(self.add_item, .2)
            except:
                pass

    def works(self):
        try:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
            initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
            self.my_stream = db.reference('ShopCode').child("Sold").child(str(datetime.datetime.now().date().year)).child(
                    DB.date_format(DB())).listen(
                self.stream_work)
        except:
            print("Woks sorry!!!")

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

        else:
            print("Reaaly")

    def sell_preview(self):
        self.root.ids.preview_sell.connect_camera(enable_analyze_pixels=True, default_zoom=0.0)
        print("connected")

    def stop_camera_sell(self):
        self.root.ids.preview_sell.disconnect_camera()

    @mainthread
    def get_barcode_sell(self, result):
        barcode = str(result.data)
        code_type = str(result.type)
        print(barcode)
        if barcode:
            if code_type != "QRCODE":
                barcode = barcode.replace("b", "").replace("'", "")

                self.product_barcode = barcode

                self.root.ids.sell_preview.text = barcode

        else:
            print("Reaaly")

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
