from pymongo import MongoClient


def create_collection(coll_name):
    client = MongoClient('mongodb://localhost:27017/')
    db = client.test
    result = db.create_collection(coll_name, validator={
        '$jsonSchema': {
            'bsonType': 'object',
            'additionalProperties': True,
            'required': ['component', 'path'],
            'properties': {
                'component': {
            "Normal_Anolmalous": {"type": "string"},
            "Get_Post": {"type": "string"},
            "User-Agent": {"type": "string"},
            "Pragma": {"type": "string"},
            "Cache-Control": {"type": "string"},
            "Accept": {"type": "string"},
            "Accept-Encoding": {"type": "string"},
            "Accept-charset": {"type": "string"},
            "Language": {"type": "string"},
            "Host": {"type": "string"}
                },
                'path': {
                    'bsonType': 'string',
                    'description': 'Set to default value'
                }
            }
        }
    })

    print(result)


if __name__ == '__main__':
    create_collection('my_coll')
