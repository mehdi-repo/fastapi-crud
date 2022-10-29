from beanie import Document
from fastapi import Form
from pydantic import BaseModel

class Todo(Document):
    user:str
    title:str
    description:str
    
    class Config:
        schema_extra={
            "example":{
                "user":"Mehdi",
                "title":"Move",
                "description":"watch a classic move"
            }
        }
    
    @classmethod
    def as_form(cls,user:str=Form(...),title:str=Form(...),description:str=Form(...)):
        return cls(user=user,title=title,description=description)
            
 

class TodoUpdate(BaseModel):
    user:str
    title:str
    description:str
    
    class Config:
        schema_extra={
            "example":{
                "user":"",
                "title":"",
                "description":""
            }
        }             