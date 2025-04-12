from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver

# Initialize Powertools utilities
logger = Logger()
tracer = Tracer()
metrics = Metrics()

def register_friends_routes(app: APIGatewayRestResolver):

    @tracer.capture_method
    @app.get("/friends")
    def get_all_friends():
        pass