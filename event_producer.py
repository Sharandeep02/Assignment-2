import random
import requests
import concurrent.futures
from datetime import datetime
import logging

logging.basicConfig(filename='event_producer.log', level=logging.DEBUG)
log = logging.getLogger(f'event_producer_agent:')


class EventProducer:

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.event_list = ["access_app", "click_banner", "view_products", "select_product", "add_to_cart",
                           "place_order"]

    def generate_event(self, user_id: str) -> dict:
        """
        this method takes user_id as an input, generates an event and returns it.
        :param user_id:
        :return event:
        """
        event_type = random.choice(self.event_list)
        timestamp = datetime.now()
        event = {"user_id": user_id,
                 "event_type": event_type,
                 "timestamp": f'{timestamp}',
                 }
        log.info(f"\tgenerated event {event}")
        return event

    def send_event(self, event):
        response = requests.post(self.webhook_url, json=event)
        log.info(response.status_code)
        return response


def generate_and_send_event(event_producer, user_id):
    """

    :param event_producer:
    :param user_id:
    :return:
    """
    try:
        event = event_producer.generate_event(user_id)
        response = event_producer.send_event(event)
        log.info(response)
        message = f"{'-' * 5} successfully generated and posted the event for user {'-' * 5}"
        log.info(message)
        return message
    except Exception as e:
        message = f'event_producer_thread failed with error, {e}'
        log.error(message)
        return message


if __name__ == "__main__":
    event_producer_obj = EventProducer("http://localhost:8888/webhook")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        user_range = range(10)
        results = [executor.submit(generate_and_send_event, event_producer_obj, user) for user in user_range]
        for f in concurrent.futures.as_completed(results):
            log.info(f.result())
