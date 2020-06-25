# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.forms import FormAction
from rasa_sdk.events import FollowupAction
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCost(Action):

    def name(self) -> Text:
        return "action_get_cost"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        estate_type = tracker.get_slot('estate_type')
        address = tracker.get_slot('address')
        area = tracker.get_slot('area')
        dispatcher.utter_message(text="Giá {} tại {} diện tích {} m2 có giá khoảng 2 tỷ đồng ạ.".format(estate_type, address, area))

        return []


class GetCostForm(FormAction):

    def name(self) -> Text:
        return "get_cost_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["estate_type", "address", "area"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        pass
        estate_type = tracker.get_slot('estate_type')
        address = tracker.get_slot('address')
        area = tracker.get_slot('area')
        dispatcher.utter_message(
            text="Giá {} tại {} với diện tích {} m2 có giá khoảng 2 tỷ đồng ạ.".format(estate_type, address, area))
        return []


class RenHouseForm(FormAction):

    def name(self) -> Text:
        return "ren_house_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["estate_type", "address", "cost"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        pass
        estate_type = tracker.get_slot('estate_type')
        address = tracker.get_slot('address')
        cost = tracker.get_slot('cost')
        dispatcher.utter_message(
            text="Gửi bạn một số {} đang cho thuê tại {} với giá khoảng {}:".format(estate_type, address, cost))
        return []


class BuyHouseForm(FormAction):

    def name(self) -> Text:
        return "buy_house_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["estate_type", "address", "cost"]

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        pass
        estate_type = tracker.get_slot('estate_type')
        address = tracker.get_slot('address')
        cost = tracker.get_slot('cost')
        dispatcher.utter_message(
            text="Gửi bạn một số {} đang được bán tại {} với giá khoảng {}:".format(estate_type, address, cost))
        return []