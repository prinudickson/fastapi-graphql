from graphene import Schema, ObjectType, Field, String, Int, List, Mutation

class UserType(ObjectType):
    """
    _summary_

    Parameters
    ----------
    ObjectType : _type_
        _description_
    """
    id = Int()
    name = String()
    age = Int()

class CreateUser(Mutation):
    """
    _summary_

    Parameters
    ----------
    Mutation : _type_
        _description_

    Returns
    -------
    _type_
        _description_
    """
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, name, age):
        user = {"id": len(Query.users)+1, "name": name, "age": age }
        Query.users.append(user)
        return CreateUser(user=user)
    
class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break

        if not user:
            return None
        
        if name is not None:
            user["name"] = name

        if age is not None:
            user["age"] = age

        return UpdateUser(user=user)

class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    def mutate(self, info, user_id):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                Query.users.remove(u)
                user = u
                break
        
        return DeleteUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int(default_value=1))
    user_min_age = List(UserType, min_age=Int())

    users = [
        {"id":1, "name":"Jane", "age": 10},
        {"id":2, "name":"Doe", "age": 19},
        {"id":3, "name":"Rahul", "age": 23},
        {"id":4, "name":"Kapoor", "age": 48}
    ]

    def resolve_user(self, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]
        return matched_users[0] if matched_users else None
    
    def resolve_user_min_age(self, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]

class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()

schema = Schema(query=Query, mutation=Mutation)

gql_create = '''
mutation {
    createUser(name: "Jimmy", age: 45){
        user{
            id
            name
            age
        }
    }
}
'''

gql_query1 = '''
query {
    user(userId: 4){
        id
        name
        age
    }
}
'''

gql_query2 = '''
query {
    userMinAge(minAge: 20){
        id
        name
        age
    }
}
'''

gql_update = '''
mutation {
    updateUser(userId: 4, name: "Kapoor_updated", age: 4545){
        user{
            id
            name
            age
        }
    }
}
'''

gql_delete = '''
mutation {
    eleteUser(userId: 4){
        user{
            id
            name
            age
        }
    }
}
'''

if __name__ == "__main__":
    result = schema.execute(gql_create)
    print(result)

    result = schema.execute(gql_query1)
    print(result)

    result = schema.execute(gql_query2)
    print(result)

    result = schema.execute(gql_update)
    print(result)

    result = schema.execute(gql_query2)
    print(result)

    result = schema.execute(gql_delete)
    print(result)

    result = schema.execute(gql_query2)
    print(result)

