import datetime

from kivymd.toast import toast


class DataBase:
    mnth_name = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    day = ["Mon", "Tue", "Wed", "Thu",
           "Fri", "Sat", "Sun"]

    def save_product(self, product_name, product_price, product_quantity, product_barcode, product_exp_year,
                     product_exp_month):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                data = {
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_quantity": product_quantity,
                    "product_barcode": product_barcode,
                    "product_expire": f"{product_exp_year}-{product_exp_month}",
                    "days_to_exp": self.day_remain(f"{product_exp_year}-{product_exp_month}")
                }
                ref = db.reference('ShopCode').child("Products").child(product_barcode)
                ref.set(data)
                toast("Saved!")

    def get_product(self, product_id):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('ShopCode').child("Products").child(product_id)
                data = ref.get()

                return data

    def sell_product(self, sold_amount, sold_quantity, product_id, name):
        data = self.get_product(product_id)
        today_data = self.get_today(product_id)
        self.today_sell(today_data, sold_amount, sold_quantity, product_id, name)
        if "sold_amount" not in data:
            trans_data = {
                "sold_amount": sold_amount,
                "sold_quantity": sold_quantity,
                "number_sold": 1,
            }

            self.sell_product_trans(trans_data, product_id)
        else:
            sold_amount = str(int(data["sold_amount"].replace("/=", "")) + int(sold_amount.replace("/=", "")))
            sold_quantity = str(int(data["sold_quantity"]) + int(sold_quantity))
            number_sold = str(int(data["number_sold"]) + 1)
            trans_data = {
                "sold_amount": sold_amount,
                "sold_quantity": sold_quantity,
                "number_sold": number_sold
            }
            self.sell_product_trans(trans_data, product_id)



    def today_sell(self, today_data, sold_amount, sold_quantity, product_id, name):
        if today_data:
            sold_amount = str(int(today_data["sold_amount"].replace("/=", "")) + int(sold_amount.replace("/=", "")))
            sold_quantity = str(int(today_data["sold_quantity"]) + int(sold_quantity))
            number_sold = str(int(today_data["number_sold"]) + 1)
            trans_data = {
                "sold_amount": sold_amount,
                "sold_quantity": sold_quantity,
                "number_sold": number_sold,
                "product_name": name
            }
            self.sell_product_today(product_id, trans_data)
        else:
            trans_data = {
                "sold_amount": sold_amount,
                "sold_quantity": sold_quantity,
                "number_sold": 1,
                "product_name":name
            }
            self.sell_product_today(product_id, trans_data)





    def sell_product_trans(self, data, product_id):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('ShopCode').child("Products").child(product_id)
                ref.update(data)

    def sell_product_today(self, product_id, data):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                ref = db.reference('ShopCode').child("Sold").child(str(datetime.datetime.now().date().year)).child(
                    self.date_format()).child(product_id)
                ref.set(data)

    def get_today(self, product_id):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                try:
                    ref = db.reference('ShopCode').child("Sold").child(str(datetime.datetime.now().date().year)).child(self.date_format()).child(product_id)
                    data = ref.get()

                    return data
                except:

                    return False

    def get_all_today(self):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})
                try:
                    ref = db.reference('ShopCode').child("Sold").child(str(datetime.datetime.now().date().year)).child(self.date_format())
                    data = ref.get()

                    return data
                except:

                    return False

    def add_debtor(self, phone, product, price, date):
        if True:
            import firebase_admin
            firebase_admin._apps.clear()
            from firebase_admin import credentials, initialize_app, db
            if not firebase_admin._apps:
                cred = credentials.Certificate("credential/farmzon-abdcb-c4c57249e43b.json")
                initialize_app(cred, {'databaseURL': 'https://farmzon-abdcb.firebaseio.com/'})

                data = {
                    "product_name": product,
                    "product_price": price,
                    "debtor_phone": phone,
                    "debt_date": date,
                }

                ref = db.reference('ShopCode').child("Debtors").child(phone)
                ref.set(data)
                toast("saved")

    def get_date(self):
        return str(datetime.datetime.now()).split(" ")[0]

    def date_format(self):
        date = self.get_date()
        year, month, day = date.strip().split("-")
        if int(month) >= 10:
            month_update = int(month) - 1
        else:
            month_update = int(month.replace("0", "")) - 1
        month_name = self.mnth_name[month_update]
        date_frmt = f"{month_name} {str(day)}"
        return date_frmt

    def get_pice(self, pric):
        coma = '{:,}'.format(int(pric))
        pric = coma

        len = pric.__len__()

        if len == 5:
            s = pric.index(",")
            num = pric[s - 1]
            num2 = pric[s + 1]

            pric = f"{num}{num2}00"

            return pric

        elif len == 3:
            s = pric[0]

            pric = f"{s}00"

            return pric

        elif len == 6:
            s = pric.index(",")
            num = pric[:s]
            num2 = pric[s + 1]

            pric = f"{num}{num2}00"

            return pric

    def get_data(self, data):
        pric, name = new_data = data.strip().split(" ")[1], data.strip().split(" ")[4:]

        new_name = ""
        for i in name:
            print(i)
            if name.index(i) == 0:
                new_name = i
            else:
                new_name = new_name + " " + i
        name = new_name
        pric = self.get_pice(pric)

        return [name, pric]

    def day_remain(self, exp_date):
        nowoy = datetime.datetime.now().date().year
        nowom = datetime.datetime.now().date().month

        now = f"{nowoy}-{nowom}"

        m1 = int(now.strip().split("-")[1])

        m2 = int(exp_date.strip().split("-")[1])

        y1 = int(now.strip().split("-")[0])

        y2 = int(exp_date.strip().split("-")[0])

        yd = (y2 - y1) * 365

        ytm1 = 30 * m1

        ytm2 = 30 * m2

        v = ytm2 - ytm1 + yd

        return v


