"""
This module offers the available Products.

Computer Systems Architecture Course
Assignment 1
March 2020
"""

from dataclasses import dataclass


@dataclass(init=True, repr=True, order=False, frozen=True)
class Product:
    """
    Class that represents a product.
    """
    name: str
    price: str


@dataclass(init=True, repr=True, order=False, frozen=True)
class Tea(Product):
    """
    Tea products
    """
    type: str


@dataclass(init=True, repr=True, order=False, frozen=True)
class Coffee(Product):
    """
    Coffee products
    """
    acidity: str
    roast_level: str