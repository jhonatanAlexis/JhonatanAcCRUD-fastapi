from typing import List
from fastapi import HTTPException, APIRouter
from db.db import collection
from modelo.libro import Libro

router = APIRouter()

@router.post("/", response_description="Crear nuevo libro", response_model=Libro)
async def create_libro(libro: Libro):
    existing_user = await collection.find_one({"isbn": libro.isbn})
    if existing_user != None:
        raise HTTPException(status_code=404, detail="El isbn ya existe")
    result = await collection.insert_one(libro.dict())
    libro._id = str(result.inserted_id)
    return libro

@router.get("/", response_description="Ver todos los libros", response_model=List[Libro])
async def read_books():
    libros = await collection.find().to_list(100)
    for libro in libros:
        libro["_id"] = str(libro["_id"])
        print(libro)
    return libros

@router.get("/{isbn}", response_description="Buscar libro por isbn", response_model=Libro)
async def read_by_isbn(isbn: str):
    libro = await collection.find_one({"isbn": isbn})
    if libro:
        return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.put("/{isbn}", response_description="Actualizar libro", response_model=Libro)
async def modify(isbn: str, libro: Libro):
    uptaded_book = await collection.find_one_and_update({"isbn": isbn}, {"$set": libro.dict()})
    if uptaded_book:
        return uptaded_book
    raise HTTPException(status_code=404, detail="Libro no encontrado")

@router.delete("/{isbn}", response_description="Borrar libro", response_model=Libro)
async def delete(isbn: str):
    deleted_book = await collection.find_one_and_delete({"isbn": isbn})
    if deleted_book:
        return deleted_book
    raise HTTPException(status_code=404, detail="Libro no encontrado")