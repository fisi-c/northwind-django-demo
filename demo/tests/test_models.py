import datetime

from django.test import TestCase
from django.db import IntegrityError

from demo import models


class ModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = models.Category.objects.create()
        cls.customer = models.Customer.objects.create()
        cls.employee = models.Employee.objects.create(
            birth_date=datetime.date(2000, 1, 1),
        )
        cls.supplier = models.Supplier.objects.create()
        cls.product = models.Product.objects.create(
            category=cls.category,
            supplier=cls.supplier,
        )
        cls.shipper = models.Shipper.objects.create()
        cls.order = models.Order.objects.create(
            customer=cls.customer,
            employee=cls.employee,
            shipper=cls.shipper,
        )
        cls.order_detail = models.OrderDetail.objects.create(
            quantity=1,
            order=cls.order,
            product=cls.product,
        )


class ProductTest(ModelTestCase):
    def test_negative_price_raises_integrity_error(self):
        self.product.price = -1.0
        with self.assertRaisesMessage(IntegrityError, "product_price_must_not_be_negative"):
            self.product.save()


class OrderDetailTest(ModelTestCase):
    def test_zero_quantity_raises_integrity_error(self):
        self.order_detail.quantity = 0
        with self.assertRaisesMessage(IntegrityError, "order_detail_quantity_must_be_positive"):
            self.order_detail.save()
