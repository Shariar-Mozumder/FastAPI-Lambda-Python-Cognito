from src.utils.response import api_response
def get_details(name,role,age):
    try:
        
        payload={
            "Name":name,
            "Role":role,
            "Age": str(age)
        }
        return api_response(200,"get details sucessfully",payload)
    except Exception as e:
        return {"error msg: "+str(e)}