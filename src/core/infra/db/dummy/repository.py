from typing import Any, List, Optional
from collections import defaultdict


class DummyMongoDBRepository:
    def __init__(self):
        self._collections = defaultdict(list)
        self._initialized = False

    async def initialize(self):
        if not self._initialized:
            self._initialized = True

    async def insert_one(self, collection_name: str, document: dict) -> None:
        await self.initialize()
        if collection_name not in self._collections:
            self._collections[collection_name] = []

        # Asegurarse de que el documento sea una copia para evitar modificaciones externas
        doc_copy = document.copy()
        self._collections[collection_name].append(doc_copy)

    async def find_one(self, collection_name: str, query: dict) -> Optional[dict]:
        collection = self._collections[collection_name]
        for doc in collection:
            matches = True
            for key, value in query.items():
                if key == '_id':
                    # Convertir tanto el valor buscado como el almacenado a string para comparar
                    doc_value = str(doc.get(key))
                    query_value = str(value)
                    if doc_value != query_value:
                        matches = False
                        break
                elif doc.get(key) != value:
                    matches = False
                    break
            if matches:
                return doc
        return None

    async def find_many(self, collection_name: str, query: dict = None) -> List[dict]:
        await self.initialize()
        if collection_name not in self._collections:
            return []

        if not query:
            return [doc.copy() for doc in self._collections[collection_name]]

        results = []
        for doc in self._collections[collection_name]:
            matches = True
            for key, value in query.items():
                if key == "_id" and isinstance(value, str):
                    value = ObjectId(value)
                if key not in doc or doc[key] != value:
                    matches = False
                    break
            if matches:
                results.append(doc.copy())
        return results

    async def update_one(self, collection_name: str, query: dict, update: dict) -> Any:
        await self.initialize()
        if collection_name not in self._collections:

            class DummyResult:
                modified_count = 0

            return DummyResult()

        for doc in self._collections[collection_name]:
            matches = True
            for key, value in query.items():
                if key == "_id" and isinstance(value, str):
                    value = ObjectId(value)
                if key not in doc or doc[key] != value:
                    matches = False
                    break
            if matches:
                doc.update(update)

                class DummyResult:
                    modified_count = 1

                return DummyResult()

        class DummyResult:
            modified_count = 0

        return DummyResult()

    async def update_many(self, collection_name: str, query: dict, update: dict) -> Any:
        await self.initialize()
        if collection_name not in self._collections:

            class DummyResult:
                modified_count = 0

            return DummyResult()

        modified = 0
        for doc in self._collections[collection_name]:
            matches = True
            for key, value in query.items():
                if key == "_id" and isinstance(value, str):
                    value = ObjectId(value)
                if key not in doc or doc[key] != value:
                    matches = False
                    break
            if matches:
                doc.update(update)
                modified += 1

        class DummyResult:
            modified_count = modified

        return DummyResult()

    async def delete_one(self, collection_name: str, query: dict) -> Any:
        await self.initialize()
        if collection_name not in self._collections:

            class DummyResult:
                deleted_count = 0

            return DummyResult()

        for i, doc in enumerate(self._collections[collection_name]):
            matches = True
            for key, value in query.items():
                if key == "_id" and isinstance(value, str):
                    value = ObjectId(value)
                if key not in doc or doc[key] != value:
                    matches = False
                    break
            if matches:
                self._collections[collection_name].pop(i)

                class DummyResult:
                    deleted_count = 1

                return DummyResult()

        class DummyResult:
            deleted_count = 0

        return DummyResult()

    async def delete_many(self, collection_name: str, query: dict) -> Any:
        await self.initialize()
        if collection_name not in self._collections:

            class DummyResult:
                deleted_count = 0

            return DummyResult()

        original_length = len(self._collections[collection_name])
        self._collections[collection_name] = [
            doc
            for doc in self._collections[collection_name]
            if not all(
                doc.get(key)
                == (
                    ObjectId(value)
                    if key == "_id" and isinstance(value, str)
                    else value
                )
                for key, value in query.items()
            )
        ]
        deleted = original_length - len(self._collections[collection_name])

        class DummyResult:
            deleted_count = deleted

        return DummyResult()
