import boto3

from src.application.repository.user_repository import UserRepository
from src.domain.entities.user import User


class DynamoDBUserRepository(UserRepository):
    def __init__(self):
        self.table_name = "users"
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)

    def add_user(self, user: User) -> None:
        self.table.put_item(
            Item={
                'id': user.user_id,
                'name': user.name
            }
        )