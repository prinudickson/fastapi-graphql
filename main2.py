from graphene import Schema, ObjectType, Field, String, Int

class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()

class Query(ObjectType):
    user = Field(UserType, user_id=Int(default_value=1))

    users = [
        {"id":1, "name":"Jane", "age": 10},
        {"id":2, "name":"Doe", "age": 19},
        {"id":3, "name":"Rahul", "age": 23},
        {"id":4, "name":"Kapoor", "age": 48}
    ]

    def resolve_user(self, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None

schema = Schema(query=Query)

gql = '''
query {
    user(userId: 4){
        id
        name
        age
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql)
    print(result)
