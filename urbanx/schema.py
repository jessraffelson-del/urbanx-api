import graphene
from graphene_django import DjangoObjectType
from decimal import Decimal
from city.models import CityService
from marketplace.models import Product, Order


class DecimalType(graphene.Scalar):
    @staticmethod
    def serialize(value):
        return float(value)

    @staticmethod
    def parse_value(value):
        return Decimal(str(value))

    @staticmethod
    def parse_literal(ast):
        return Decimal(str(ast.value))


class CityServiceType(DjangoObjectType):
    class Meta:
        model = CityService
        fields = '__all__'


class ProductType(DjangoObjectType):
    price = DecimalType()

    class Meta:
        model = Product
        fields = '__all__'


class OrderType(DjangoObjectType):
    total_price = DecimalType()

    class Meta:
        model = Order
        fields = '__all__'

class Query(graphene.ObjectType):
    all_services = graphene.List(CityServiceType)
    all_products = graphene.List(ProductType)
    all_orders = graphene.List(OrderType)
    service = graphene.Field(CityServiceType, id=graphene.Int())
    product = graphene.Field(ProductType, id=graphene.Int())
    order = graphene.Field(OrderType, id=graphene.Int())
    products_by_category = graphene.List(
        ProductType,
        category=graphene.String(required=True)
    )
    available_products = graphene.List(ProductType)

    def resolve_all_services(root, info):
        return CityService.objects.all()

    def resolve_all_products(root, info):
        return Product.objects.all()

    def resolve_all_orders(root, info):
        return Order.objects.all()

    def resolve_service(root, info, id):
        return CityService.objects.get(pk=id)

    def resolve_product(root, info, id):
        return Product.objects.get(pk=id)

    def resolve_order(root, info, id):
        return Order.objects.get(pk=id)

    def resolve_products_by_category(root, info, category):
        return Product.objects.filter(category=category)

    def resolve_available_products(root, info):
        return Product.objects.filter(is_available=True, stock__gt=0)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        category = graphene.String(required=True)
        description = graphene.String(required=True)
        price = graphene.Float(required=True)
        stock = graphene.Int(required=True)

    product = graphene.Field(ProductType)

    def mutate(root, info, name, category, description, price, stock):
        product = Product(
            name=name,
            category=category,
            description=description,
            price=price,
            stock=stock
        )
        product.save()
        return CreateProduct(product=product)


class Mutation(graphene.ObjectType):
    create_product = CreateProduct.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)