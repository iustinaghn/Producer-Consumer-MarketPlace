"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
import threading
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.products = products
        self.marketplace = marketplace
        self.id_producer = self.marketplace.register_producer()
        self.republish_wait_time = republish_wait_time
        self.event = threading.Event()

    def run(self):
        while True:
            for p in self.products:
                ack_publish = False
                while ack_publish is not True:
                    ack_publish = self.marketplace.publish(self.id_producer, p[0])
                    self.event.wait(p[2]) if ack_publish is False else self.event.wait(self.republish_wait_time)
