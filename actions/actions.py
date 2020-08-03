from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher

def price_format(price):
    return '{:,.0f}'.format(price).replace(',', '.')

class ActionFeeOffVipPost(Action):
    def __init__(self):
        self.fee_table = {'vip1': {'fee': {1: 40000, 7: 266000, 15: 540000, 30: 10200000, 90: 28800000}, 'up_fee': 4000, 'name': 'Vip 1'},
                         'vip2': {'fee': {1: 25000, 7: 166250, 15: 337500, 30: 637500, 90: 18000000}, 'up_fee': 2500, 'name': 'Vip 2'},
                         'vip3': {'fee': {1: 15000, 7: 99750, 15: 202500, 30: 382500, 90: 1080000}, 'up_fee': 1500, 'name': 'Vip 3'}}
        self.coefficient = {'ngày': {'coef': 1, 'text': 'ngày'}, 'ngay': {'coef': 1, 'text': 'ngày'},
                            'tháng': {'coef': 30, 'text': 'tháng'}, 'thang': {'coef': 30, 'text': 'tháng'},
                            'tuan': {'coef': 7, 'text': 'tuần'}, 'tuần': {'coef': 7, 'text': 'tuần'}}

    def name(self) -> Text:
        return "action_fee_of_vip_post"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        post_package = tracker.get_slot('post_package')
        duration = tracker.get_slot('duration')
        if duration != None:
            duration = duration.lower()
            duration_value = ''.join(filter(str.isdigit, duration))
            duration_unit = duration.replace(duration_value, '').strip()
            duration_value = int(duration_value)
            if duration_value == '' or duration_unit not in self.coefficient:
                duration = None

        vip_type = 0
        if post_package != None:
            post_package = post_package.lower()
            if 'vip' in post_package:
                if '1' in post_package:
                    vip_type = 'vip1'
                elif '2' in post_package:
                    vip_type = 'vip2'
                elif '3' in post_package:
                    vip_type = 'vip3'

        fee_table = self.fee_table
        if vip_type != 0:
            # nếu chỉ bắt được post_package
            if duration == None:
                dispatcher.utter_message(text="Giá gói {} hiện tại là {}đ/tin/ngày ạ."
                                         .format(fee_table[vip_type]['name'],
                                                 price_format(fee_table[vip_type]['fee'][1])))
                message = 'Ngoài ra bên em còn có các gói'
                for package in fee_table:
                    if package != vip_type:
                        message += ' {} với giá {}đ/tin/ngày,'.format(fee_table[package]['name'],
                                                                      price_format(fee_table[package]['fee'][1]))
                message = message[:-1] + ' ạ.'
                dispatcher.utter_message(message)
                return []
            # nếu bắt dc cả 2
            else:
                cost = fee_table[vip_type]['fee'][1]*duration_value*self.coefficient[duration_unit]['coef']
                text_unit = self.coefficient[duration_unit]['text']
                message = 'Gói {} trong {} {} có giá {}đ ạ'.format(fee_table[vip_type]['name'],
                                                                   duration_value,
                                                                   text_unit,
                                                                   price_format(cost))
                dispatcher.utter_message(message)
                return []

        # Nếu chỉ bắt dc duration
        elif duration != None:
            message = 'Không biết bạn muốn hỏi về gói vip nào ạ'
            dispatcher.utter_message(message)
            message = 'Hiện tại bên em đang có 3 gói đăng tin vip là VIP1, VIP2 và VIP3 ạ.'
            dispatcher.utter_message(message)
            return []

        # Còn lại là trường hợp không bắt được gì
        message = 'Hiện tại Meeyland cung cấp {} gói tin VIP là'.format(len(fee_table))
        for package in fee_table:
            message += ' gói {} giá {}đ/tin/ngày,'.format(fee_table[package]['name'],
                                                          price_format(fee_table[package]['fee'][1]))
        message = message[:-1] + ' ạ.'
        dispatcher.utter_message(message)
        return []

#
# class GetCostForm(FormAction):
#
#     def name(self) -> Text:
#         return "get_cost_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["estate_type", "address", "area"]
#
#     def submit(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         pass
#         estate_type = tracker.get_slot('estate_type')
#         address = tracker.get_slot('address')
#         area = tracker.get_slot('area')
#         dispatcher.utter_message(
#             text="Giá {} tại {} với diện tích {} m2 có giá khoảng 2 tỷ đồng ạ.".format(estate_type, address, area))
#         return []

#
# class (FormAction):
#
#     def name(self) -> Text:
#         return "ren_house_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["estate_type", "address", "cost"]
#
#     def submit(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         pass
#         estate_type = tracker.get_slot('estate_type')
#         address = tracker.get_slot('address')
#         cost = tracker.get_slot('cost')
#         dispatcher.utter_message(
#             text="Gửi bạn một số {} đang cho thuê tại {} với giá khoảng {}:".format(estate_type, address, cost))
#         return []
#
#
# class BuyHouseForm(FormAction):
#
#     def name(self) -> Text:
#         return "buy_house_form"
#
#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["estate_type", "address", "cost"]
#
#     def submit(
#             self,
#             dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any],
#     ) -> List[Dict]:
#         pass
#         estate_type = tracker.get_slot('estate_type')
#         address = tracker.get_slot('address')
#         cost = tracker.get_slot('cost')
#         dispatcher.utter_message(
#             text="Gửi bạn một số {} đang được bán tại {} với giá khoảng {}:".format(estate_type, address, cost))
#         return []