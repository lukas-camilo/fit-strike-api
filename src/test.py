from aws_lambda_powertools.event_handler import APIGatewayRestResolver

from interface_adapters.controllers.product_controller import register_product_routes

app = APIGatewayRestResolver()

a = register_product_routes(app).list_products_handler()
print(f"Aqui => {a}")