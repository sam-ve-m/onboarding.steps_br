import asyncio

from decouple import config

from src.domain.enums.file.user_file import UserFileType
from src.domain.exceptions.model import BadRequestError
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps_builder.service import OnboardingStepBuilderBR


class OnboardingSteps:
    bucket_name = config("AWS_BUCKET_USERS_FILES")
    user_repository = UserRepository
    file_repository = FileRepository
    steps_builder = OnboardingStepBuilderBR

    @classmethod
    async def onboarding_user_current_step_br(
        cls,
        payload: dict,
    ) -> dict:

        onboarding_step_builder = cls.steps_builder()
        user_unique_id = payload["user"]["unique_id"]

        user_file_exists = await cls.file_repository.user_file_exists(
            file_type=UserFileType.SELFIE,
            unique_id=user_unique_id,
            bucket_name=cls.bucket_name,
        )
        user_document_front_exists = cls.file_repository.user_file_exists(
            file_type=UserFileType.DOCUMENT_FRONT,
            unique_id=user_unique_id,
            bucket_name=cls.bucket_name,
        )
        user_document_back_exists = cls.file_repository.user_file_exists(
            file_type=UserFileType.DOCUMENT_BACK,
            unique_id=user_unique_id,
            bucket_name=cls.bucket_name,
        )
        user_document_exists = all(
            await asyncio.gather(user_document_front_exists, user_document_back_exists)
        )

        current_user = await cls.user_repository.find_user(
            {"unique_id": user_unique_id}
        )
        if current_user is None:
            raise BadRequestError("common.register_not_exists")

        onboarding_steps = await (
            onboarding_step_builder.user_suitability_step(current_user=current_user)
            .user_identifier_step(current_user=current_user)
            .user_selfie_step(user_file_exists=user_file_exists)
            .user_complementary_step(current_user=current_user)
            .user_document_validator_step(
                current_user=current_user, document_exists=user_document_exists
            )
            .user_data_validation_step(current_user=current_user)
            .user_electronic_signature_step(current_user=current_user)
            .build()
        )

        return onboarding_steps
