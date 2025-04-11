from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.logging import Logger
from aws_lambda_powertools.tracing import Tracer
from aws_lambda_powertools.metrics import Metrics

from src.interface_adapters.controllers.product_controller import register_product_routes

# Initialize Powertools utilities
logger = Logger()
tracer = Tracer()
metrics = Metrics()
app = APIGatewayRestResolver()

# Register routes from controllers
register_product_routes(app)

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """Main Lambda handler"""
    logger.info("Start 2")
    return app.resolve(event, context)