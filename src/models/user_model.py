from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,NumberAttribute

# Define PynamoDB model for User
class User(Model):
    class Meta:
        table_name = "users"
        region = "us-east-2"
        write_capacity_units = 5  # Specify the write capacity units
        read_capacity_units = 5   # Specify the read capacity units

    user_id = UnicodeAttribute(hash_key=True)
    full_name = UnicodeAttribute()
    email = UnicodeAttribute()
    age = NumberAttribute()
    phone = UnicodeAttribute()
    password=UnicodeAttribute()
    token=UnicodeAttribute()

# Create table if not exists
if not User.exists():
    User.create_table(wait=True)