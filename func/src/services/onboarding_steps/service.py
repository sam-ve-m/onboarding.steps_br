from decouple import config

from src.domain.enums.file.selfie_file import UserSelfie
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps_builder.service import OnboardingStepBuilder


class OnboardingSteps:
    bucket_name = config("AWS_BUCKET_USERS_FILES")
    user_repository = UserRepository
    file_repository = FileRepository
    steps_builder = OnboardingStepBuilder

    @classmethod
    async def onboarding_user_current_step_br(
        cls,
        payload: dict,
    ) -> dict:

        user_unique_id = payload["user"]["unique_id"]

        user_selfie_exists = await cls.file_repository.user_file_exists(
            file_type=UserSelfie.SELFIE,
            unique_id=user_unique_id,
            bucket_name=cls.bucket_name,
        )

        user = await cls.user_repository.find_user({"unique_id": user_unique_id})
        onboarding_step_builder = cls.steps_builder(user)

        onboarding_steps = await onboarding_step_builder.build(
            selfie_exists=user_selfie_exists
        )

        return onboarding_steps
