from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    '''
    Represents a product category.
    '''

    category_name = models.CharField(
        max_length=25,
        unique=True,
        verbose_name=_("category name"),
    )

    description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name=_("description"),
        help_text=_("an optional description for the category"),
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")


class Customer(models.Model):
    '''
    Represents an individual customer or business entity.
    '''

    customer_name = models.CharField(
        max_length=50,
        verbose_name=_("customer name"),
    )

    contact_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("contact person"),
    )

    address = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("address"),
    )

    city = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("city"),
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_("postal code"),
    )

    country = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("country"),
    )

    def __str__(self):
        return self.customer_name

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")


class Employee(models.Model):
    '''
    Represents an employee of Northwind Traders.
    '''

    last_name = models.CharField(
        max_length=15,
        verbose_name=_("last name"),
    )

    first_name = models.CharField(
        max_length=15,
        verbose_name=_("first name"),
    )

    birth_date = models.DateField(
        verbose_name=_("birth date"),
    )

    photo = models.ImageField(
        upload_to="images/employee_photo/",
        blank=True,
        null=True,
        verbose_name=_("photo"),
    )

    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("notes"),
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = _("employee")
        verbose_name_plural = _("employees")


class Supplier(models.Model):
    '''
    Represents an external supplier.
    '''

    supplier_name = models.CharField(
        max_length=50,
        verbose_name=_("supplier name"),
    )

    contact_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("contact person"),
    )

    address = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=_("address"),
    )

    city = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name=_("city"),
    )

    postal_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=_("postal code"),
    )

    country = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("country"),
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("phone number"),
    )

    def __str__(self):
        return self.supplier_name

    class Meta:
        verbose_name = _("supplier")
        verbose_name_plural = _("suppliers")


class Product(models.Model):
    '''
    Represents a product offered by Northwind Traders.
    '''

    product_name = models.CharField(
        max_length=50,
        verbose_name=_("product name"),
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("supplier"),
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name=_("category"),
    )

    unit = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name=_("unit"),
    )

    price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.0,
        verbose_name=_("price"),
    )

    def __str__(self):
        return self.product_name

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(price__gte="0"),
                name="product_price_must_not_be_negative",
            ),
        ]
        verbose_name = _("product")
        verbose_name_plural = _("products")


class Shipper(models.Model):
    '''
    Represents a shipping partner of Northwind Traders.
    '''

    shipper_name = models.CharField(
        max_length=25,
        verbose_name=_("shipper name"),
    )

    phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name=_("phone number"),
    )

    def __str__(self):
        return self.shipper_name

    class Meta:
        verbose_name = _("shipper")
        verbose_name_plural = _("shippers")


class Order(models.Model):
    '''
    Represents an individual customer order.
    '''

    customer = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("customer"),
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("employee"),
    )

    order_date = models.DateField(
        auto_now_add=True,
        verbose_name=_("order date"),
    )

    shipper = models.ForeignKey(
        Shipper,
        on_delete=models.PROTECT,
        related_name="orders",
        verbose_name=_("shipper"),
    )

    def __str__(self):
        return "#{:06d}".format(self.id)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")


class OrderDetail(models.Model):
    '''
    Represents an item in a customer order.
    '''

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name=_("order"),
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="details",
        verbose_name=_("product"),
    )

    quantity = models.PositiveIntegerField(
        verbose_name=_("quantity"),
    )

    def __str__(self):
        return f'{_("order")} {self.order}, {_("product")} {self.product}, {_("quantity")} {self.quantity}'

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt="0"),
                name="order_detail_quantity_must_be_positive",
            ),
        ]
        verbose_name = _("order detail")
        verbose_name_plural = _("order details")
