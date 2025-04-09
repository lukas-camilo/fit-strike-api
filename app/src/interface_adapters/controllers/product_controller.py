from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.validation import validate
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.metrics import Metrics, MetricUnit
from domain.entities.product import Product
from application.use_cases.create_product import create_product
from application.use_cases.get_product import get_product
from application.use_cases.update_product import update_product
from application.use_cases.delete_product import delete_product
from application.use_cases.list_products import list_products
from infrastructure.repositories.product_repository import ProductRepository

# Initialize Powertools utilities
logger = Logger()
tracer = Tracer()
metrics = Metrics()

# Inicialize o repositório
repository = ProductRepository()

# JSON schema for input validation
create_product_schema = {
    "type": "object",
    "properties": {
        "product_id": {"type": "string"},
        "name": {"type": "string"},
        "price": {"type": "number"},
        "stock": {"type": "integer"}
    },
    "required": ["product_id", "name", "price", "stock"]
}

def register_product_routes(app: APIGatewayRestResolver):

    @tracer.capture_method
    @app.post("/products")
    def create_product_handler():
        event: APIGatewayProxyEvent = app.current_event
        data = event.json_body
        validate(event_body=data, schema=create_product_schema)  # Validate input

        product = Product(data['product_id'], data['name'], data['price'], data['stock'])
        create_product(repository, product)

        metrics.add_metric(name="ProductCreated", unit=MetricUnit.Count, value=1)
        return Response(
            status_code=201,
            content_type="application/json",
            body={"message": "Product created successfully"}
        )

    @tracer.capture_method
    @app.get("/products")
    def list_products_handler():
        products = list_products(repository)
        return Response(
            status_code=200,
            content_type="application/json",
            body=[vars(p) for p in products]
        )

    @tracer.capture_method
    @app.get("/products/<product_id>")
    def get_product_handler(product_id: str):
        product = get_product(repository, product_id)
        if product:
            return Response(
                status_code=200,
                content_type="application/json",
                body=vars(product)
            )
        return Response(
            status_code=404,
            content_type="application/json",
            body={"message": "Product not found"}
        )

    @tracer.capture_method
    @app.put("/products/<product_id>")
    def update_product_handler(product_id: str):
        event: APIGatewayProxyEvent = app.current_event
        data = event.json_body
        validate(event_body=data, schema=create_product_schema)  # Validate input

        updated_product = Product(product_id, data['name'], data['price'], data['stock'])
        update_product(repository, product_id, updated_product)

        return Response(
            status_code=200,
            content_type="application/json",
            body={"message": "Product updated successfully"}
        )

    @tracer.capture_method
    @app.delete("/products/<product_id>")
    def delete_product_handler(product_id: str):
        delete_product(repository, product_id)
        metrics.add_metric(name="ProductDeleted", unit=MetricUnit.Count, value=1)
        return Response(
            status_code=204,
            content_type="application/json",
            body=""
        )