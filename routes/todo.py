from typing import List
from beanie import PydanticObjectId
from database.connection import Database
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Path, HTTPException, status, Request, Depends
from models.todo import Todo, TodoUpdate



todo_router = APIRouter(tags=["Todos"])
todo_database = Database(Todo)
templates = Jinja2Templates(directory="templates/")


@todo_router.post("/")
async def add_todo(request: Request, todo: Todo = Depends(Todo.as_form)):   
        await todo_database.save(todo)
        todo = await todo_database.get_all()
        return templates.TemplateResponse("todos.html", 
            {
            "request": request,
            "todos": todo
            })



@todo_router.get("/", response_model=List[Todo])
async def retrieve_all_todos(request: Request) -> List[Todo]:
    todos = await todo_database.get_all()
    return templates.TemplateResponse("todos.html", 
    {
        "request": request,
        "todos": todos
    })


@todo_router.get("/{id}", response_model=Todo)
async def retrieve_event(id: PydanticObjectId,request: Request) -> Todo:
    todo = await todo_database.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tod with supplied ID does not exist"
        )
    return templates.TemplateResponse("todo.html", 
    {
        "request": request,
        "todo": todo
    })


@todo_router.put("/{id}", response_model=Todo)
async def update_todo(id: PydanticObjectId, body: TodoUpdate,) -> Todo:
    updated_todo = await todo_database.update(id, body)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID does not exist"
        )
    return updated_todo





@todo_router.delete("/{id}")
async def delete_todo(id: PydanticObjectId) -> dict:
    todo = await todo_database.get(id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo with supplied ID does not exist"
        )

    return {
        "message": "Todo deleted successfully."
    }