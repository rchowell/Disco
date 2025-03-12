from disco.object import Validator


def test_json_schema_validator():
    schema = """
    {
        "$id": "https://example.com/person.schema.json",
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "title": "Person",
        "type": "object",
        "properties": {
            "firstName": {
                "type": "string",
                "description": "The person's first name."
            },
            "lastName": {
                "type": "string",
                "description": "The person's last name."
            },
            "age": {
                "description": "Age in years which must be equal to or greater than zero.",
                "type": "integer",
                "minimum": 0
            }
        }
    }
    """

    validator = Validator.from_json_schema(schema)

    data_ok = """
    {
        "firstName": "John",
        "lastName": "Doe",
        "age": 21
    }
    """
    assert validator.validate(data_ok)

    data_bad = """
    {
        "firstName": "John",
        "lastName": "Doe",
        "age": -1
    }
    """
    assert not validator.validate(data_bad)
