import datetime

def object_to_dict(obj):
    # values=obj['attribute_values']
    obj_dict = vars(obj)
    values=obj_dict['attribute_values']
    # Convert datetime objects to ISO format strings
    for key, value in values.items():
        if isinstance(value, datetime.datetime):
            values[key] = value.isoformat()
    api_response("User signed up","successfully executed",500,200, "User signed up successfully")
    # Remove attributes to ignore
    ignore_attributes = ['cls']  # Add any other attributes to ignore
    for attr in ignore_attributes:
        values.pop(attr, None)
    return values
    api_response("User signed up","successfully executed",500,200, "User signed up successfully")
