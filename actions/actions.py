from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
import random
from numpy import random as rd
from rasa_sdk.forms import FormAction
from rasa_sdk.events import FollowupAction, SlotSet, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher


fee_table = {'vip1': {'fee': {1: 40000, 7: 266000, 15: 540000, 30: 1020000, 90: 2880000}, 'up_fee': 4000, 'name': 'Vip 1'},
             'vip2': {'fee': {1: 25000, 7: 166250, 15: 337500, 30: 637500, 90: 1800000}, 'up_fee': 2500, 'name': 'Vip 2'},
             'vip3': {'fee': {1: 15000, 7: 99750, 15: 202500, 30: 382500, 90: 1080000}, 'up_fee': 1500, 'name': 'Vip 3'}}
discounts = {1: 0.00, 7: 0.05, 15: 0.10, 30: 0.15, 90: 0.20}
coefficient = {'ngày': {'coef': 1, 'text': 'ngày'}, 'ngay': {'coef': 1, 'text': 'ngày'},
                'tháng': {'coef': 30, 'text': 'tháng'}, 'thang': {'coef': 30, 'text': 'tháng'},
                'tuan': {'coef': 7, 'text': 'tuần'}, 'tuần': {'coef': 7, 'text': 'tuần'}}


def price_format(price):
    return '{:,.0f}'.format(price).replace(',', '.')


def convert_duration(duration):
    duration_value = None
    duration_unit = 'ngày'
    days = None
    if duration != None:
        duration = duration.lower()
        duration_value = ''.join(filter(str.isdigit, duration))
        duration_unit = duration.replace(duration_value, '').strip()
        duration_value = int(duration_value)
        days = duration_value * coefficient[duration_unit]['coef']
        if duration_value == '' or duration_unit not in coefficient:
            duration = None

    return duration, duration_value, duration_unit, days


def convert_post_package(post_package):
    vip_type = None
    if post_package != None:
        post_package = post_package.lower()
        if 'vip' in post_package:
            if '1' in post_package:
                vip_type = 'vip1'
            elif '2' in post_package:
                vip_type = 'vip2'
            elif '3' in post_package:
                vip_type = 'vip3'
    return vip_type


class ActionFeeOffVipPost(Action):
    def __init__(self):
        self.fee_table = fee_table
        self.coefficient = coefficient
        pass

    def name(self) -> Text:
        return "action_fee_of_vip_post"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        post_package = tracker.get_slot('post_package')
        duration = tracker.get_slot('duration')
        duration, duration_value, duration_unit, _ = convert_duration(duration)

        vip_type = convert_post_package(post_package)

        fee_table = self.fee_table
        if vip_type is not None:
            # nếu chỉ bắt được post_package
            if duration == None:
                dispatcher.utter_message(text="Giá gói {} hiện tại là {}đ/tin/ngày ạ."
                                         .format(fee_table[vip_type]['name'],
                                                 price_format(fee_table[vip_type]['fee'][1])))
                message = 'Ngoài ra MeeyLand còn có các gói'
                for package in fee_table:
                    if package != vip_type:
                        message += ' {} với giá {}đ/tin/ngày,'.format(fee_table[package]['name'],
                                                                      price_format(fee_table[package]['fee'][1]))
                message = message[:-1] + ' ạ.'
                dispatcher.utter_message(message)
                return [SlotSet("post_package", None), SlotSet("duration", None)]
            # nếu bắt dc cả 2
            else:
                cost = fee_table[vip_type]['fee'][1]*duration_value*self.coefficient[duration_unit]['coef']
                text_unit = self.coefficient[duration_unit]['text']
                message = 'Gói {} trong {} {} có giá {}đ ạ'.format(fee_table[vip_type]['name'],
                                                                   duration_value,
                                                                   text_unit,
                                                                   price_format(cost))
                dispatcher.utter_message(message)
                return [SlotSet("post_package", None), SlotSet("duration", None)]

        # Nếu chỉ bắt dc duration
        elif duration != None:
            message = 'Không biết bạn muốn hỏi về gói vip nào ạ'
            dispatcher.utter_message(message)
            message = 'Hiện tại bên em đang có 3 gói đăng tin vip là VIP1, VIP2 và VIP3 ạ.'
            dispatcher.utter_message(message)
            return [SlotSet("post_package", None), SlotSet("duration", None)]

        # Còn lại là trường hợp không bắt được gì
        text = tracker.get_last_event_for('user')['text']
        if 'vip' in text:
            message = 'Hiện tại Meeyland cung cấp {} gói tin VIP là'.format(len(fee_table))
            for package in fee_table:
                message += ' gói {} giá {}đ/tin/ngày,'.format(fee_table[package]['name'],
                                                              price_format(fee_table[package]['fee'][1]))
            message = message[:-1] + ' ạ.'
            dispatcher.utter_message(message)
            dispatcher.utter_message("Bạn có thể tham khảo chi tiết bảng giá tại [đây](https://meeyland.com/page/bao-gia)")
            return [SlotSet("post_package", None), SlotSet("duration", None)]
        else:
            message = 'Hiện tại Meeyland cung cấp {} gói tin là'.format(len(fee_table) + 1)
            for package in fee_table:
                message += ' gói {} giá {}đ/tin/ngày,'.format(fee_table[package]['name'],
                                                              price_format(fee_table[package]['fee'][1]))
            message = message[:-1] + ' và gói tin thường miễn phí ạ.'
            dispatcher.utter_message(message)
            dispatcher.utter_message(
                "Bạn có thể tham khảo chi tiết bảng giá tại [đây](https://meeyland.com/page/bao-gia)")
            return [SlotSet("post_package", None), SlotSet("duration", None)]


class ActionVipPostDetails(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_vip_post_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        post_package = tracker.get_slot('post_package')
        results = []
        if post_package != None:
            post_package = post_package.lower()
            if post_package in ['tin thuong', 'tin thường', 'tinthường', 'tinthuong']:
                results.append('utter_vip0_info')
            elif 'vip' in post_package:
                if '1' in post_package:
                    results.append('utter_vip1_info')
                elif '2' in post_package:
                    results.append('utter_vip2_info')
                elif '3' in post_package:
                    results.append('utter_vip3_info')
        if len(results) < 1:
            results = ['utter_vip0_info', 'utter_vip1_info', 'utter_vip2_info', 'utter_vip3_info']
        for utter in results:
            dispatcher.utter_template(utter, tracker)
        return [SlotSet("post_package", None)]


class ActionVipPackageCompare(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_vip_post_compare"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        results = []
        list_entity = tracker.get_last_event_for('user')["parse_data"]["entities"]
        dispatcher.utter_message('Giữa các gói tin có sự khác nhau về mức độ ưu tiên hiển thị, màu và độ lớn của tiêu đề ạ.')
        for entity in list_entity:
            if entity['entity'] == 'post_package':
                value = entity['value'].lower()
                if value in ['tin thuong', 'tin thường', 'tinthường', 'tinthuong']:
                    results.append('utter_vip0_info')
                elif 'vip' in value:
                    if '1' in value:
                        results.append('utter_vip1_info')
                    elif '2' in value:
                        results.append('utter_vip2_info')
                    elif '3' in value:
                        results.append('utter_vip3_info')
        if len(results) <= 1:
            results = ['utter_vip0_info', 'utter_vip1_info', 'utter_vip2_info', 'utter_vip3_info']
        for utter in results:
            dispatcher.utter_template(utter, tracker)
        return [SlotSet("post_package", None)]


class ActionHowToSearch(Action):
    def __init__(self):
        self.opposition = {'mua': 'bán', 'thuê': 'cho thuê', 'sang nhượng': 'mua sang nhượng',
                      'bán':  'mua', 'cho thuê': 'cần thuê', 'mua sang nhượng': 'sang nhượng'}
        self.links = {'mua': ['https://meeyland.com/articles/new?category=mua-ban-nha-dat', 'https://meeyland.com/mua-ban-nha-dat'],
                      'thuê': ['https://meeyland.com/articles/new?category=cho-thue-nha-dat', 'https://meeyland.com/cho-thue-nha-dat'],
                      'sang nhượng': ['https://meeyland.com/articles/new?category=sang-nhuong-nha-dat', 'https://meeyland.com/sang-nhuong-nha-dat'],
                      'bán':  ['https://meeyland.com/articles/new?category=mua-ban-nha-dat', 'https://meeyland.com/mua-ban-nha-dat'],
                      'cho thuê': ['https://meeyland.com/articles/new?category=cho-thue-nha-dat', 'https://meeyland.com/cho-thue-nha-dat'],
                      'mua sang nhượng': ['https://meeyland.com/articles/new?category=sang-nhuong-nha-dat', 'https://meeyland.com/sang-nhuong-nha-dat']}
        pass

    def name(self) -> Text:
        return "action_how_to_search"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        post_purpose = tracker.get_slot('post_purpose')
        if post_purpose != None:
            post_purpose = post_purpose.lower()
        if post_purpose == None or post_purpose not in self.opposition:
            message = "Để tìm kiếm, bạn nhập từ khoá vào thanh công cụ tìm kiếm, hệ thống tự động đưa ra các kết quả tìm kiếm dựa trên từ khoá đã nhập. \n• [Mua/ Bán Nhà Đất](https://meeyland.com/mua-ban-nha-dat) \n• [Thuê/ Cho Thuê Nhà Đất](https://meeyland.com/cho-thue-nha-dat) \n• [Sang Nhượng](https://meeyland.com/sang-nhuong-nha-dat)"
        else:
            link1 = self.links[post_purpose][0]
            link2 = self.links[post_purpose][1]
            message = 'Để {} BĐS, bạn có thể đăng tin {} BĐS hoặc tìm kiếm tin đăng {} BĐS trên trang [meeyland.com](https://meeyland.com). \nVào [đây]({}) để đăng tin {} BĐS. \nVào [đây]({}) để tìm kiếm tin đăng {} BĐS.'.format(post_purpose, post_purpose, self.opposition[post_purpose], link1, post_purpose, link2, self.opposition[post_purpose])
            pass

        dispatcher.utter_message(message)
        return [SlotSet("post_purpose", None)]


class ActionGreet(Action):
    def __init__(self):
        self.samples = ['Xin chào bạn, mình là MeeyBot. Mình có thể giúp gì cho bạn ạ?',
                        'Xin chào, mình là MeeyBot. Rất vui khi được hỗ trợ bạn.',
                        'Chào bạn, tên mình là MeeyBot. Bạn cần mình giúp gì không?',
                        'Chào bạn, mình là MeeyBot. Mình giúp gì được cho bạn ạ!']
        self.utters = ['Mình có thể giúp gì cho bạn?',
                       'Mình đây ạ.',
                       'Bạn cần giúp đỡ gì nào?'
                       ]
        pass

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        is_greeted = tracker.get_slot('is_greeted')
        username = tracker.get_slot('name')

        td_index = rd.choice(range(len(self.samples)))
        sample = rd.choice(self.samples)
        if is_greeted == 'True':
            dispatcher.utter_message(rd.choice(self.utters))
        else:
            dispatcher.utter_message(sample)

        return [SlotSet("is_greeted", "True")]

class ActionUserAskUserName(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_user_ask_username"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        username = tracker.get_slot('name')
        if username is None:
            dispatcher.utter_message('Bạn chưa giới thiệu tên cho mình mà :D'.format(username))
            return [FollowupAction('utter_ask_name')]
        username = username.title()
        dispatcher.utter_message('Tên bạn là {} ạ :D'.format(username))
        return []


class ActionUserIntroduceName(Action):
    def __init__(self):
        self.samples = ['Xin chào {}{}. Mình có thể giúp gì cho bạn ạ?',
                        'Xin chào {}. Rất vui khi được hỗ trợ bạn.',
                        'Chào {}{}. Bạn cần mình giúp gì không?',
                        'Chào {}{}. Mình giúp gì được cho bạn ạ!']
        self.botintro = ', mình là MeeyBot'
        pass

    def name(self) -> Text:
        return "action_user_introduce_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        is_greeted = tracker.get_slot('is_greeted')
        username = tracker.get_slot('name')
        if username == None:
            username = "bạn"
        else:
            username = username.title()

        sample = rd.choice(self.samples)
        if is_greeted == 'True':
            self.botintro = ''
        dispatcher.utter_message(sample.format(username, self.botintro))
        return [SlotSet("is_greeted", "True")]

class ActionSetSourcePackage(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_set_source_post_package"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        post_package = tracker.get_slot('post_package')
        return [SlotSet("source_post_package", post_package), SlotSet("post_package", None)]

class ActionSetBuyNewPostDuration(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_set_buy_new_vip_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        new_duration = tracker.get_slot('duration')
        _, _, _, bought_days = convert_duration(new_duration)
        fees = fee_table['vip1']['fee']
        if bought_days not in fees:
            return [FollowupAction('utter_request_valid_buy_vip_duration')]
        return [SlotSet("buy_new_vip_duration", new_duration), SlotSet("duration", None)]

class ActionSetDestinationPackage(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_set_destination_post_package"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        post_package = tracker.get_slot('post_package')
        return [SlotSet("destination_post_package", post_package), SlotSet("post_package", None)]


class ActionSetBuyPostDuration(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_set_buy_vip_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        duration = tracker.get_slot('duration')
        _, _, _, bought_days = convert_duration(duration)
        fees = fee_table['vip1']['fee']
        if bought_days not in fees:
            return [FollowupAction('utter_request_valid_buy_vip_duration'), SlotSet("duration", None)]
        return [SlotSet("buy_vip_duration", duration), SlotSet("duration", None)]


class ActionSetUsedPostDuration(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_set_used_vip_duration"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        duration = tracker.get_slot('duration').replace('-', '')
        _, _, _, used_days = convert_duration(duration)
        buy_vip_duration = tracker.get_slot('buy_vip_duration')
        if buy_vip_duration is not None:
            _, _, _, bought_days = convert_duration(buy_vip_duration)
            if used_days > bought_days:
                return [FollowupAction('utter_request_valid_used_vip_duration'), SlotSet("duration", None)]

        if used_days < 1:
            return [FollowupAction('utter_request_valid_used_vip_duration'), SlotSet("duration", None)]
        return [SlotSet("used_vip_duration", duration), SlotSet("duration", None)]


class CalculateDownPostForm(FormAction):
    def name(self) -> Text:
        return "calculate_down_post_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["source_post_package", "buy_vip_duration", "used_vip_duration"]

    def validate_source_post_package(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'source_post_package':
            return {"source_post_package": tracker.get_slot('source_post_package')}

        post_package = convert_post_package(value)
        if post_package:
            return {'post_package': None, "source_post_package": value}
        else:
            return {'post_package': None, "source_post_package": None}

    def validate_buy_vip_duration(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'buy_vip_duration':
            return {"buy_vip_duration": tracker.get_slot('buy_vip_duration')}

        _, _, _, bought_days = convert_duration(value)
        fees = fee_table['vip1']['fee']
        if bought_days in fees:
            return {"duration": None, "buy_vip_duration": value}
        else:
            dispatcher.utter_template('utter_request_valid_buy_vip_duration', tracker)
            return {"duration": None, "buy_vip_duration": None}

    def validate_used_vip_duration(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'used_vip_duration':
            return {"used_vip_duration": tracker.get_slot('used_vip_duration')}

        _, _, _, used_days = convert_duration(value)
        buy_vip_duration = tracker.get_slot('buy_vip_duration')
        if buy_vip_duration is not None:
            _, _, _, bought_days = convert_duration(buy_vip_duration)
            if used_days > bought_days:
                dispatcher.utter_template('utter_request_valid_used_vip_duration', tracker)
                return {"used_vip_duration": None, "duration": None}
        if used_days < 1:
            dispatcher.utter_template('utter_request_valid_used_vip_duration', tracker)
            return {"duration": None, "used_vip_duration": None}

        return {"duration": None, "used_vip_duration": value}


    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {
            "source_post_package": self.from_entity(entity="post_package", intent=["enter_data"]),
            "buy_vip_duration": self.from_entity(entity="duration", intent=["enter_data"]),
            "used_vip_duration": self.from_entity(entity="duration", intent=["enter_data"])
        }
    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        source_post_package = tracker.get_slot('source_post_package')
        buy_vip_duration = tracker.get_slot('buy_vip_duration')
        used_vip_duration = tracker.get_slot('used_vip_duration')

        vip_type = convert_post_package(source_post_package)
        _, _, _, bought_days = convert_duration(buy_vip_duration)
        _, _, _, used_days = convert_duration(used_vip_duration)

        if vip_type != vip_type:
            return [FollowupAction('utter_ask_source_post_package')]

        discount_real = 0
        discount_bought = 0
        for i in discounts.keys():
            if used_days >= i:
                discount_real = discounts[i]
            if bought_days >= i:
                discount_bought = discounts[i]

        used_cost = fee_table[vip_type]['fee'][1]*used_days*(1-discount_real)
        paid_cost = fee_table[vip_type]['fee'][bought_days]
        message1 = 'Gói tin bạn đã mua là gói {}, số ngày là {} ngày nên được chiết khấu {}%, tổng số tiền đã thanh toán là {}đ.'.format(
            fee_table[vip_type]['name'], bought_days, int(discount_bought*100), price_format(paid_cost))
        message2 = 'Số ngày đã sử dụng là {} ngày, thì chỉ được chiết khấu {}% nên số tiền bạn đã dùng là {}đ.'.format(
            used_days, int(discount_real*100), price_format(used_cost))
        refund = paid_cost - used_cost
        if refund < 0:
            message3 = "Số tiền bạn đã dùng vượt quá số tiền bạn thanh toán ban đầu. Vậy khi hạ tin bạn sẽ không được hoàn trả và cũng không cần phải nạp thêm ạ."
        elif refund == 0:
            message3 = "Bạn đã dùng hết số tiền thanh toán ban đầu. Vậy khi hạ tin bạn sẽ không được hoàn trả tiền vào tài khoản nữa ạ."
        else:
            message3 = 'Như vậy khi hạ tin bạn sẽ được hoàn lại {}đ vào tài khoản khuyến mại bạn nhé!'.format(price_format(paid_cost - used_cost))
        dispatcher.utter_message(message1)
        dispatcher.utter_message(message2)
        dispatcher.utter_message(message3)
        return [SlotSet("source_post_package", None),SlotSet("buy_vip_duration", None),SlotSet("used_vip_duration", None)]

class CalculateChangePostForm(FormAction):
    def name(self) -> Text:
        return "calculate_change_post_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["source_post_package", "buy_vip_duration", "used_vip_duration", "destination_post_package", "buy_new_vip_duration"]

    def validate_source_post_package(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'source_post_package':
            return {"source_post_package": tracker.get_slot('source_post_package')}

        post_package = convert_post_package(value)
        if post_package:
            return {'post_package': None, "source_post_package": value}
        else:
            return {'post_package': None, "source_post_package": None}

    def validate_buy_vip_duration(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'buy_vip_duration':
            return {"buy_vip_duration": tracker.get_slot('buy_vip_duration')}

        _, _, _, bought_days = convert_duration(value)
        fees = fee_table['vip1']['fee']
        if bought_days in fees:
            return {"duration": None, "buy_vip_duration": value}
        else:
            dispatcher.utter_template('utter_request_valid_buy_vip_duration', tracker)
            return {"duration": None, "buy_vip_duration": None}

    def validate_used_vip_duration(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'used_vip_duration':
            return {"used_vip_duration": tracker.get_slot('used_vip_duration')}

        _, _, _, used_days = convert_duration(value)
        buy_vip_duration = tracker.get_slot('buy_vip_duration')
        if buy_vip_duration is not None:
            _, _, _, bought_days = convert_duration(buy_vip_duration)
            if used_days > bought_days:
                dispatcher.utter_template('utter_request_valid_used_vip_duration', tracker)
                return {"used_vip_duration": None, "duration": None}
        if used_days < 1:
            dispatcher.utter_template('utter_request_valid_used_vip_duration', tracker)
            return {"duration": None, "used_vip_duration": None}

        return {"duration": None, "used_vip_duration": value}

    def validate_destination_post_package(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'destination_post_package':
            return {"destination_post_package": tracker.get_slot('destination_post_package')}

        post_package = convert_post_package(value)
        if post_package:
            return {'post_package': None, "destination_post_package": value}
        else:
            return {'post_package': None, "destination_post_package": None}

    def validate_buy_new_vip_duration(
            self,
            value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        requested_slot = tracker.current_state()['slots']['requested_slot']
        if requested_slot != 'buy_new_vip_duration':
            return {"buy_new_vip_duration": tracker.get_slot('buy_new_vip_duration')}

        _, _, _, bought_days = convert_duration(value)
        fees = fee_table['vip1']['fee']
        if bought_days in fees:
            return {"duration": None, "buy_new_vip_duration": value}
        else:
            dispatcher.utter_template('utter_request_valid_buy_vip_duration', tracker)
            return {"duration": None, "buy_new_vip_duration": None}

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "source_post_package": self.from_entity(entity="post_package", intent=["enter_data"]),
            "buy_vip_duration": self.from_entity(entity="duration", intent=["enter_data"]),
            "used_vip_duration": self.from_entity(entity="duration", intent=["enter_data"]),
            "destination_post_package": self.from_entity(entity="post_package", intent=["enter_data"]),
            "buy_new_vip_duration": self.from_entity(entity="duration", intent=["enter_data"])
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        source_post_package = tracker.get_slot('source_post_package')
        buy_vip_duration = tracker.get_slot('buy_vip_duration')
        used_vip_duration = tracker.get_slot('used_vip_duration')

        vip_type = convert_post_package(source_post_package)
        _, _, _, bought_days = convert_duration(buy_vip_duration)
        _, _, _, used_days = convert_duration(used_vip_duration)

        if vip_type is None:
            return [FollowupAction('utter_ask_source_post_package')]

        discount = 0
        for i in discounts.keys():
            if used_days >= i:
                discount = discounts[i]

        used_cost = fee_table[vip_type]['fee'][1] * used_days * (1 - discount)
        paid_cost = fee_table[vip_type]['fee'][bought_days]

        message1 = 'Bạn đã dùng gói {} được {} ngày trên tổng số {} ngày. Vậy số tiền bạn đã dùng là {}đ. Số tiền còn lại của bạn là {}đ'.format(
            fee_table[vip_type]['name'], used_days, bought_days, price_format(used_cost), price_format(int(float((paid_cost - used_cost)))))

        destination_post_package = tracker.get_slot('destination_post_package')
        buy_new_vip_duration = tracker.get_slot('buy_new_vip_duration')

        vip_type_new = convert_post_package(destination_post_package)
        _, _, _, bought_days_new = convert_duration(buy_new_vip_duration)
        
        if vip_type_new is None:
            return [FollowupAction('utter_ask_destination_post_package')]

        paid_cost_new = fee_table[vip_type_new]['fee'][bought_days_new]
        discount = discounts[bought_days_new]
        result = int(float((paid_cost - used_cost - paid_cost_new)))
        
        if result > 0:
            message2 = 'Khi đổi sang gói {} với thời gian {} ngày có đơn giá {}đ - đã được khuyến mãi {}"%" bạn sẽ được hoàn lại {}đ vào Tài khoản khuyến mại.'.format(
                fee_table[vip_type_new]['name'], bought_days_new,price_format(paid_cost_new),int(discount)*100,price_format(float(result)))
        elif result < 0:
            message2 = 'Khi đổi sang gói {} với thời gian {} ngày có đơn giá {}đ - đã được khuyến mãi {}"%" bạn sẽ cần thanh toán thêm {}đ.'.format(
                fee_table[vip_type_new]['name'], bought_days_new,price_format(paid_cost_new),int(discount)*100,price_format(float(result) * -1))
        elif result == 0:
            message2 = 'Khi đổi sang gói {} với thời gian {} ngày có đơn giá {}đ - đã được khuyến mãi {}"%" bạn sẽ không cần thanh toán thêm chi phí gì cả.'.format(
                fee_table[vip_type_new]['name'], bought_days_new,int(discount)*100,price_format(paid_cost_new))        
        dispatcher.utter_message(message1)
        dispatcher.utter_message(message2)
        return [SlotSet("source_post_package", None),SlotSet("buy_vip_duration", None),SlotSet("used_vip_duration", None),SlotSet("destination_post_package", None),SlotSet("buy_new_vip_duration", None)]

class ActionCalculateChangePost(Action):
    def name(self) -> Text:
        return "action_change_post_package"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        source_post_package = tracker.get_slot('source_post_package')
        buy_vip_duration = tracker.get_slot('buy_vip_duration')
        used_vip_duration = tracker.get_slot('used_vip_duration')

        vip_type = convert_post_package(source_post_package)
        _, _, _, bought_days = convert_duration(buy_vip_duration)
        _, _, _, used_days = convert_duration(used_vip_duration)

        if vip_type is None:
            return [FollowupAction('utter_ask_source_post_package')]

        discount = 0
        for i in discounts.keys():
            if used_days >= i:
                discount = discounts[i]

        used_cost = fee_table[vip_type]['fee'][1] * used_days * (1 - discount)
        paid_cost = fee_table[vip_type]['fee'][bought_days]

        message1 = 'Bạn đã dùng gói {} được {} ngày trên tổng số {} ngày. Vậy số tiền bạn đã dùng là {}đ.'.format(
            fee_table[vip_type]['name'], used_days, bought_days, price_format(used_cost))

        destination_post_package = tracker.get_slot('destination_post_package')
        buy_new_vip_duration = tracker.get_slot('buy_new_vip_duration')

        vip_type_new = convert_post_package(destination_post_package)
        _, _, _, bought_days_new = convert_duration(buy_new_vip_duration)

        if vip_type_new is None:
            return [FollowupAction('utter_ask_destination_post_package')]

        paid_cost_new = fee_table[vip_type_new]['fee'][bought_days_new]

        result = int(float((paid_cost - used_cost - paid_cost_new)))

        if result > 0:
            message2 = 'Khi đổi sang gói {} với thời gian {} ngày bạn sẽ được hoàn lại {}đ vào Tài khoản khuyến mại.'.format(
                fee_table[vip_type_new]['name'], bought_days_new, price_format(float(result)))
        else:
            message2 = 'Khi đổi sang gói {} với thời gian {} ngày bạn sẽ cần thanh toán thêm {}đ.'.format(
                fee_table[vip_type_new]['name'], bought_days_new, price_format(float(result) * -1))
        dispatcher.utter_message(message1)
        dispatcher.utter_message(message2)
        return [AllSlotsReset()]


class ActionCheckEmailAndPhone(Action):
    def __init__(self):
        pass

    def check_phone_number(self, phone_number):
        prefix1 = ['09', '03', '07', '08', '05']
        prefix2 = ['849', '843', '847', '848', '845']
        rmchar = ['+', '-', '_', '.', ',']
        for ch in rmchar:
            phone_number = phone_number.replace(ch, '')
        if not phone_number.isdigit():
            return False
        if phone_number[:2] in prefix1 and len(phone_number) == 10:
            return True
        if phone_number[:3] in prefix2 and len(phone_number) == 11:
            return True
        return False

    def name(self) -> Text:
        return "action_check_email_n_phone"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # check email status
        email = tracker.get_slot('email')
        if email is not None:
            from validate_email import validate_email
            if not validate_email(email_address=email, check_regex=True, check_mx=False):
                dispatcher.utter_template('utter_request_valid_email', tracker)
                return [SlotSet("email", None), FollowupAction('action_listen')]
            elif not validate_email(email_address=email, check_regex=False, check_mx=True, smtp_timeout=5, dns_timeout=5):
                dispatcher.utter_template('utter_request_exist_email', tracker)
                return [SlotSet("email", None), FollowupAction('action_listen')]
            else:
                return []

        # check phone number
        phone_number = tracker.get_slot('phone_number')
        if phone_number is not None:
            if not self.check_phone_number(phone_number):
                dispatcher.utter_template('utter_request_valid_phone_number', tracker)
                return [SlotSet("phone_number", None), FollowupAction('action_listen')]
        return []


class ActionForwardCustomerService(Action):
    def __init__(self):
        pass

    def name(self) -> Text:
        return "action_forward_customer_service"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        email = tracker.get_slot('email')
        phone_number = tracker.get_slot('phone_number')
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
