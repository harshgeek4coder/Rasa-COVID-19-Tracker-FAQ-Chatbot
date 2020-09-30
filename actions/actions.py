# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests


# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


class ActionHelloLoc(Action):

    def name(self) -> Text:
        return "action_get_loc"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        slot_name = tracker.get_slot("state")

        print("slotname", slot_name)

        dispatcher.utter_message(
            text="So You Live In " + slot_name.title() + " , Here Are Your Location's Corona Stats: \n")

        return []

class Actioncoronastats(Action):

    def name(self) -> Text:
        return "actions_corona_state_stat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        responses = requests.get("https://api.covid19india.org/data.json").json()

        entities = tracker.latest_message['entities']
        print("Now Showing Data For:", entities)
        state = None

        for i in entities:
            if i["entity"] == "state":
                state = i["value"]

        message = "Please Enter Correct State Name !"

        if state == "india":
            state = "Total"
        for data in responses["statewise"]:
            if data["state"] == state.title():
                print(data)
                message = "Now Showing Cases For --> " + state.title() + " Since Last 24 Hours : "+ "\n" + "Active: " + data[
                    "active"] + " \n" + "Confirmed: " + data["confirmed"] + " \n" + "Recovered: " + data[
                              "recovered"] + " \n" + "Deaths: " + data["deaths"] + " \n" + "As Per Data On: " + data[
                              "lastupdatedtime"]

        print(message)
        dispatcher.utter_message(message)

        return []





