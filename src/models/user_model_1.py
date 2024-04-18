from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute,UTCDateTimeAttribute,MapAttribute,DiscriminatorAttribute,ListAttribute

# from pynamodb_config import AWS_ACCESS_KEY_ID, AWS_REGION, AWS_SECRET_ACCESS_KEY, HOST

class Entity(Model):
  class Meta:
    table_name = "entity"
    region = "us-east-2"
    write_capacity_units = 5  # Specify the write capacity units
    read_capacity_units = 5  
    billing_mode = 'PAY_PER_REQUEST'
    
  id = UnicodeAttribute(hash_key=True)
  cls = DiscriminatorAttribute()
  name = UnicodeAttribute()
  description = UnicodeAttribute()
  email = UnicodeAttribute()
  phone = UnicodeAttribute()
  im = UnicodeAttribute(null=True)
  modified_date = UTCDateTimeAttribute(null=True)
  registration_date = UTCDateTimeAttribute()
  status=UnicodeAttribute()
  modified_by = UnicodeAttribute(null=True)
# Create table if not exists
if not Entity.exists():
    Entity.create_table(wait=True)
  
class OrganizationChild(MapAttribute):
  id = UnicodeAttribute(hash_key=True)
#   cls = DiscriminatorAttribute()
  name = UnicodeAttribute()
  description = UnicodeAttribute()
  email = UnicodeAttribute()
  phone = UnicodeAttribute()
  im = UnicodeAttribute(null=True)
  modified_date = UTCDateTimeAttribute(null=True)
  registration_date = UTCDateTimeAttribute()
  status=UnicodeAttribute()
  modified_by = UnicodeAttribute(null=True)

class Organization(Entity, discriminator='organization'):
  child_entity_list = ListAttribute(null=True,of=OrganizationChild)
  

class TestOrganization(Entity, discriminator='test_organization'):
  child_entity_list = ListAttribute(null=True)
    
class User(Entity, discriminator='user'):
    first_name=UnicodeAttribute()
    last_name=UnicodeAttribute()
    cell_phone=UnicodeAttribute()