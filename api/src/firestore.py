from fastapi import HTTPException
from firebase_admin import firestore_async
from google.cloud.firestore_v1.async_document import AsyncDocumentReference
from typing import Dict, Any, List
import firebase_admin


class Firestore:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cred = firebase_admin.credentials.Certificate("firebase-secrets.json")
            firebase_admin.initialize_app(cred)
            cls.firestore = firestore_async.client()  # type: ignore
            cls.instance = super(Firestore, cls).__new__(cls)
        return cls.instance

    async def create(self, collection: str, data: Dict[str, Any]) -> Dict[str, Any]:
        ref = self.__get_ref(data["id"], collection)
        await ref.set(data)
        return await self.__get_doc_safely(ref)

    async def get_by_id(self, id: str, collection: str) -> Dict[str, Any]:
        ref = self.__get_ref(id, collection)
        return await self.__get_doc_safely(ref)

    async def get_all(self, collection: str) -> List[Dict[str, Any]]:
        docs = self.firestore.collection(collection).stream()  # type: ignore
        docs_dicts = []
        async for doc in docs:
            dict = doc.to_dict()
            docs_dicts.append(dict)
        return docs_dicts

    async def update(
        self, id: str, collection: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        ref = self.__get_ref(id, collection)
        await self.__get_doc_safely(ref)
        await ref.update(data)
        return await self.__get_doc_safely(ref)

    async def __get_doc_safely(self, ref: AsyncDocumentReference) -> Dict[str, Any]:
        doc = await ref.get()
        if not doc.exists:
            raise HTTPException(status_code=404, detail=f"Item doesn't exists")
        return doc.to_dict()  # type: ignore

    def __get_ref(self, id: str, collection: str) -> AsyncDocumentReference:
        ref = self.firestore.collection(collection).document(id)
        return ref


firestore = Firestore()
