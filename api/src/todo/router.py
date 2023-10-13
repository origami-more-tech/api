from fastapi import APIRouter
from firestore import firestore
from todo.model import Todo, CreateTodoDTO, PatchTodoDTO
from contstants import Collection
from typing import List


router = APIRouter()
router.tags = [Collection.todo]


@router.get("/{id}")
async def get_todo(id: str) -> Todo:
    todo_dict = await firestore.get_by_id(collection=Collection.todo, id=id)
    return Todo(**todo_dict)


@router.get("/")
async def get_all_todos() -> List[Todo]:
    todo_dicts = await firestore.get_all(collection=Collection.todo)
    return [Todo(**todo_dict) for todo_dict in todo_dicts]


@router.post("/")
async def create_todo(create_todo_dto: CreateTodoDTO) -> Todo:
    todo = Todo(**create_todo_dto.model_dump())
    todo_dict = await firestore.create(
        collection=Collection.todo, data=todo.model_dump()
    )
    return Todo(**todo_dict)


@router.patch("/{id}")
async def patch_todo(id: str, patch_todo_dto: PatchTodoDTO) -> Todo:
    todo_dict = await firestore.update(
        collection=Collection.todo, id=id, data=patch_todo_dto.model_dump()
    )
    return Todo(**todo_dict)


@router.delete("/{id}")
async def delete_todo(id: str):
    return f"You wanna get todo with {id}"
