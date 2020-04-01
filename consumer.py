"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
import threading
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.name = kwargs["name"]
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.event = threading.Event()

    def run(self):
        for cart in self.carts:
            id_c = self.marketplace.new_cart()
            i = 0
            while i < len(cart):
                q = 0
                while q < cart[i]["quantity"]:
                    if cart[i]["type"] == "add":
                        bol = False
                        while bol is False:
                            bol = self.marketplace.add_to_cart(id_c, cart[i]["product"])
                            self.event.wait(self.retry_wait_time) if bol is False else self.event.set()
                    self.marketplace.remove_from_cart(id_c, cart[i]["product"]) if cart[i]["type"] == "remove" else None
                    q += 1
                i += 1

            [print("%s bought %s" % (self.name, str(product))) for product in self.marketplace.place_order(id_c)]
