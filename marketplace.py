"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2020
"""
from threading import RLock


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer
        self.all_prod = {}
        self.all_cart = []
        self.nr_cart = 0
        self.nr_prod = 0
        self.rlock = RLock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        self.rlock.acquire()
        self.nr_prod = self.nr_prod + 1
        self.all_prod["prod%s" % str(self.nr_prod)] = []
        self.rlock.acquire()
        return "prod%s" % str(self.nr_prod)

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.all_prod[producer_id]) < self.queue_size_per_producer:
            self.all_prod[producer_id].append(product)
            return True

        else:
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.nr_cart = self.nr_cart + 1
        self.all_cart.insert(self.nr_cart - 1, [])
        return self.nr_cart - 1

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        ack_cart = False
        i = 0
        while i < len(self.all_prod):
            for p in self.all_prod["prod%s" % str(i + 1)]:
                if p == product:
                    self.all_cart[cart_id].append(product)
                    ack_cart = True
                    break
            if ack_cart is True:
                break
            i += 1
        self.all_prod["prod%s" % str(i + 1)].remove(product) if ack_cart is True else None

        return ack_cart

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        self.all_cart[cart_id].remove(product)
        self.all_prod["prod%s" % str(self.nr_prod)].append(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        current_cart = []
        current_cart, self.all_cart[cart_id] = self.all_cart[cart_id], current_cart

        return current_cart
