from typing import Optional

from decouple import config
from etria_logger import Gladsheim

from src.domain.model_decorator.generate_id import hash_field
from src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure
from src.repositories.cache.repository import RepositoryRedis


class OnboardingStepsRepository:

    infra = MongoDBInfrastructure
    cache = RepositoryRedis
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def find_one(
        cls, query: dict, ttl: int = None, project: dict = None
    ) -> Optional[dict]:
        if ttl is None:
            ttl = 0
        try:
            collection = await cls.__get_collection()
            data = None

            has_ttl = ttl > 0
            if has_ttl:
                data = await cls._get_from_cache(query=query)

            if not data:
                data = await collection.find_one(query, project)

            if has_ttl and data is not None:
                await cls._save_cache(query=query, ttl=ttl, data=data)

            return data

        except Exception as e:
            Gladsheim.error(error=e)
            raise Exception("internal_error")

    @classmethod
    async def _get_from_cache(cls, query: dict):
        if query is None:
            return None
        query_hash = await hash_field(payload=query)
        base_identifier = cls.get_base_identifier()
        cache_value = await cls.cache.get(key=f"{base_identifier}:{query_hash}")
        if cache_value:
            return cache_value
        return None

    @classmethod
    async def _save_cache(cls, data: dict, query: dict, ttl: int = 0):

        ttl = 60 if ttl == 0 else ttl

        query_hash = await hash_field(payload=query)
        base_identifier = cls.get_base_identifier()
        await cls.cache.set(
            key=f"{base_identifier}:{query_hash}",
            value=data,
            ttl=ttl,
        )

    @classmethod
    def get_base_identifier(cls):
        if not (cls.database and cls.collection):
            raise Exception(
                "The gods think you are a foolish guy because you don't know what you want. Try again!"
            )
        return f"{cls.database}:{cls.collection}"

    @classmethod
    async def is_user_using_suitability_or_refuse_term(cls, unique_id: str) -> str:
        collection = await cls.__get_collection()
        user = await collection.find_one({"unique_id": unique_id})
        suitability = user.get("suitability")
        term_refusal = user["terms"].get("term_refusal")

        has_suitability = suitability is not None
        has_term_refusal = term_refusal is not None

        suitability_and_refusal_term = (True, True)
        only_suitability = (True, False)
        only_refusal_term = (False, True)
        nothing = (False, False)

        user_trade_match = {
            suitability_and_refusal_term: cls.suitability_and_refusal_term_callback,
            only_suitability: lambda _suitability, _term_refusal: "suitability",
            only_refusal_term: lambda _suitability, _term_refusal: "term_refusal",
            nothing: lambda _suitability, _term_refusal: None,
        }

        user_trade_profile_callback = user_trade_match.get(
            (has_suitability, has_term_refusal)
        )
        user_trade_profile = user_trade_profile_callback(suitability, term_refusal)

        return user_trade_profile

    @staticmethod
    def suitability_and_refusal_term_callback(_suitability, _term_refusal):
        last_trade_profile_signed = (
            _suitability["submission_date"] > _term_refusal["date"]
        )
        return "suitability" if last_trade_profile_signed else "term_refusal"
