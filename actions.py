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
        dispatcher.utter_message(text="Giá {} tại {} với diện tích {} m2 có giá khoảng 2 tỷ đồng ạ.".format(estate_type, address, area))

        return []


class FormGetInfor(FormAction):

    def name(self) -> Text:
        return "form_get_infor"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        return ["estate_type", "address", "area"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:
        return {
            "estate_type": [self.from_entity(entity="estate_type", intent=["inform"]), self.from_text()],
            "address": [self.from_entity(entity="address", intent=["inform"]), self.from_text()],
            "area": [self.from_entity(entity="area", intent=["inform"]), self.from_text()],
        }

    def submit(
            self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any],
    ) -> List[Dict]:
        pass
        # estate_type = tracker.get_slot('estate_type')
        # address = tracker.get_slot('address')
        # area = tracker.get_slot('area')