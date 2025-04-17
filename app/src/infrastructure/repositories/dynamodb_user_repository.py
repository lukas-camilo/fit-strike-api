import boto3

from src.application.repository.user_repository import UserRepository
from src.domain.entities.user import User
from typing import Tuple, List, Optional

class DynamoDBUserRepository(UserRepository):

    def __init__(self):
        self.table_name = "users"
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)

    def add_user(self, user: User) -> None:
        self.table.put_item(
            Item={
                'id': user.user_id,
                'name': user.name,
                'email': user.email
            }
        )

    def get_users(self, limit: int, last_evaluated_key=None) -> Tuple[List[User], Optional[dict]]:
        scan_kwargs = {
            'Limit': limit
        }

        if last_evaluated_key:
            scan_kwargs['ExclusiveStartKey'] = last_evaluated_key

        response = self.table.scan(**scan_kwargs)
        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey', None)

        users = [User(user_id=item['id'], name=item['name'], email=item['email']) for item in items]

        return users, last_evaluated_key