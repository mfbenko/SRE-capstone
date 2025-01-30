import pymongo
import json

def validate_document(document, schema):
    """Validates a document against a JSON schema."""
    try:
        jsonschema.validate(document, schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)

def main():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["your_database"]
    collection = db["your_collection"]

    # Pulled from Kaggle
    schema = {
        "type": "object",
        "properties": {
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
        #Still gotta fill this out
        "required": ["name", "age"]
    }

 # Iterate over documents in the collection
    for document in collection.find():
        is_valid, error_message = validate_document(document, schema)
        if not is_valid:
            print(f"Document {document['_id']} failed validation: {error_message}")

if __name__ == "__main__":
    main()
   
