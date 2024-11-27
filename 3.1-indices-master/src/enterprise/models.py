
from tortoise import fields, models


class Company(models.Model):
    class Meta:
        table = "users_company"

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)
    address = fields.CharField(max_length=200)

    def __str__(self) -> str:
        return f"<{self.id}: {self.title}>"


class Job(models.Model):
    class Meta:
        table = "users_job"

    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=200)

    def __str__(self) -> str:
        return f"<{self.id}: {self.title}>"


class User(models.Model):
    class Meta:
        table = "users_user"

    id = fields.IntField(pk=True)
    first_name = fields.CharField(max_length=200)
    second_name = fields.CharField(max_length=200)
    last_name = fields.CharField(max_length=200)
    email = fields.CharField(max_length=200)
    address = fields.CharField(max_length=300)
    phone_number = fields.CharField(max_length=40)
    company = fields.ForeignKeyField(
        "models.Company",
        on_delete=fields.RESTRICT,
        related_name="users",
    )
    job = fields.ForeignKeyField(
        "models.Job",
        on_delete=fields.RESTRICT,
        related_name="+",
    )

    def __str__(self) -> str:
        return f"<{self.id}: {self.last_name} {self.first_name} {self.second_name}>"


class TimestampMixin():
    created_at = fields.DatetimeField(null=True, auto_now_add=True)
    updated_at = fields.DatetimeField(null=True, auto_now=True)


class Customer(TimestampMixin, models.Model):
    class Meta:
        table = "customers"

    customer_id = fields.IntField(pk=True, allows_generated=True)
    first_name = fields.CharField(max_length=50, null=False)
    last_name = fields.CharField(max_length=50, null=False)
    email = fields.CharField(max_length=100, null=False, unique=True)
    phone = fields.CharField(max_length=20)
    address = fields.CharField(max_length=255)
    city = fields.CharField(max_length=100)
    state = fields.CharField(max_length=100)
    zip_code = fields.CharField(max_length=20)

    def __str__(self) -> str:
        return f"<{self.customer_id}: {self.last_name} {self.first_name}>"

class Order(TimestampMixin, models.Model):
    class Meta:
        table = "orders"

    order_id = fields.IntField(pk=True, allows_generated=True)
    customer = fields.ForeignKeyField(
        "models.Customer",
        on_delete=fields.RESTRICT,
    )
    order_date = fields.DateField(null=True)
    total_amount = fields.DecimalField(max_digits=10, decimal_places=2)
    status = fields.CharField(max_length=50)
    shipping_address = fields.CharField(max_length=255)
    billing_address = fields.CharField(max_length=255)

    def __str__(self) -> str:
        return f"<{self.order_id}: Customer <{self.customer_id}>>"


class OrderProduct(models.Model):
    class Meta:
        table = 'orders_products'

    order_product_id = fields.IntField(pk=True, allows_generated=True)
    order = fields.ForeignKeyField(
        "models.Order",
        on_delete=fields.RESTRICT,
    )
    product = fields.ForeignKeyField(
        "models.Product",
        on_delete=fields.RESTRICT,
    )
    quantity = fields.IntField(null=False)


class Product(models.Model):
    class Meta:
        table = 'products'

    product_id = fields.IntField(pk=True, allows_generated=True)
    name = fields.CharField(100, null=False)
    description = fields.TextField()
    image_url = fields.CharField(255)


class Seller(TimestampMixin, models.Model):
    class Meta:
        table =  'sellers'

    seller_id = fields.IntField(pk=True, allows_generated=True)
    name = fields.CharField(100, null=False)
    email = fields.CharField(100, null=False, unique=True)
    phone = fields.CharField(20)
    address = fields.CharField(255)
    city = fields.CharField(100)
    state = fields.CharField(100)
    zip_code = fields.CharField(20)
    latitude = fields.DecimalField(max_digits=9, decimal_places=6)
    longitude = fields.DecimalField(max_digits=9, decimal_places=6)


class SellerPrice(TimestampMixin, models.Model):
    class Meta:
        table = 'seller_prices'

    seller_price_id = fields.IntField(pk=True, allows_generated=True)
    seller = fields.ForeignKeyField(
        "models.Seller",
        on_delete=fields.RESTRICT,
    )
    product = fields.ForeignKeyField(
        "models.Product",
        on_delete=fields.RESTRICT,
    )
    price = fields.DecimalField(max_digits=10, decimal_places=2)


class SellerStock(TimestampMixin, models.Model):
    class Meta:
        table = 'seller_stock'

    seller_stock_id = fields.IntField(pk=True, allows_generated=True)
    seller = fields.ForeignKeyField(
        "models.Seller",
        on_delete=fields.RESTRICT,
    )
    product = fields.ForeignKeyField(
        "models.Product",
        on_delete=fields.RESTRICT,
    )
    stock = fields.IntField()
