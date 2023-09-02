from graphene import Schema, ObjectType, String

class Query(ObjectType):
    xy = String(name=String(default_value="John"))

    def resolve_xy(self, info, name):
        return f'hey {name }' 

schema = Schema(query=Query)

gql = '''
{
    xy(name: "graphql")
}
'''

if __name__ =="__main__": 
    result = schema.execute(gql)
    print(result )