import uuid

from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.validation import validate

from src.application.use_cases.add_user import AddUserUseCase
from src.infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository

# Initialize Powertools utilities
logger = Logger()
tracer = Tracer()
metrics = Metrics()

# Initialize repository
user_repository = DynamoDBUserRepository()

# Initialize use case
add_user_use_case = AddUserUseCase(user_repository)

# JSON schema for input validation
create_user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
    },
    "required": ["name"]
}

def register_user_routes(app: APIGatewayRestResolver):
    @tracer.capture_method
    @app.post("/user")
    def create_user():
        event: APIGatewayProxyEvent = app.current_event
        data = event.json_body
        validate(event_body=data, schema=create_user_schema)

        add_user_use_case.execute(str(uuid.uuid4()), data['name'])

        metrics.add_metric(name="UserCreated", unit=MetricUnit.Count, value=1)
        return Response(
            status_code=201,
            content_type="application/json",
            body={
                "message": "User created successfully"
            }
        )