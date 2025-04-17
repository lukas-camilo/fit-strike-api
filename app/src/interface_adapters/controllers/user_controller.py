import uuid

from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, Response
from aws_lambda_powertools.metrics import MetricUnit
from aws_lambda_powertools.utilities.data_classes import APIGatewayProxyEvent
from aws_lambda_powertools.utilities.validation import validate, SchemaValidationError

from src.application.use_cases.user.add_user import AddUserUseCase
from src.application.use_cases.user.get_users import GetUsersUseCase
from src.infrastructure.repositories.dynamodb_user_repository import DynamoDBUserRepository

# Initialize Powertools utilities
logger = Logger()
tracer = Tracer()
metrics = Metrics()

# Initialize repository
user_repository = DynamoDBUserRepository()

# Initialize use case
add_user_use_case = AddUserUseCase(user_repository)
get_users_use_case = GetUsersUseCase(user_repository)

# JSON schema for input validation
create_user_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "email": {"type": "string"}
    },
    "required": ["name", "email"]
}


def register_user_routes(app: APIGatewayRestResolver):
    @tracer.capture_method
    @app.post("/users")
    def create_user():
        try:
            event: APIGatewayProxyEvent = app.current_event
            data = event.json_body
            validate(event=data, schema=create_user_schema)

            add_user_use_case.execute(str(uuid.uuid4()), data['name'], data['email'])

            metrics.add_metric(name="UserCreated", unit=MetricUnit.Count, value=1)
            
            return Response(
                status_code=201,
                content_type="application/json",
                body={
                    "message": "User created successfully"
                }
            )
        except SchemaValidationError as e:
            missing_fields = [error.path for error in e.context]
            return Response(
                status_code=400,
                content_type="application/json",
                body={
                    "message": "Invalid input data",
                    "missing_fields": missing_fields,
                    "error": str(e)
                }
            )

    @tracer.capture_method
    @app.get("/users")
    def get_users():
        event: APIGatewayProxyEvent = app.current_event
        limit = int(event.headers.get("X-Limit", 10))
        last_evaluated_key = event.headers.get("X-Last-Evaluated-Key", None)

        users, last_evaluated_key = get_users_use_case.execute(limit, last_evaluated_key)

        return Response(
            status_code=200,
            content_type="application/json",
            body=[user.to_dict() for user in users]
        )