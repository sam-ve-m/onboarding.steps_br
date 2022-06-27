from unittest.mock import patch

from pytest import mark, raises

from src.domain.exceptions.model import BadRequestError
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import OnboardingSteps

payload_dummy = {"user": {"unique_id": "test"}}
find_user_return_dummy = {"current_user": payload_dummy}


class OnboardingStepBuilderBRStub:
    def __init__(self):
        self.__onboarding_steps: dict = {
            "current_onboarding_step": "suitability_step",
            "suitability_step": False,
            "user_identifier_data_step": False,
            "user_selfie_step": False,
            "user_complementary_step": False,
            "user_document_validator": False,
            "user_data_validation": False,
            "user_electronic_signature": False,
            "finished": False,
        }
        self.__steps: list = [
            "suitability_step",
            "user_identifier_data_step",
            "user_selfie_step",
            "user_complementary_step",
            "user_document_validator",
            "user_data_validation",
            "user_electronic_signature",
        ]
        self.bureau_status = None

    def user_suitability_step(self, current_user):
        self.__onboarding_steps["suitability_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "user_identifier_data_step"
        return self

    def user_identifier_step(self, current_user: dict):
        self.__onboarding_steps["user_identifier_data_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "user_selfie_step"
        return self

    def user_selfie_step(self, user_file_exists: bool):
        self.__onboarding_steps["user_selfie_step"] = user_file_exists
        self.__onboarding_steps["current_onboarding_step"] = "user_complementary_step"
        return self

    def user_complementary_step(self, current_user):
        self.__onboarding_steps["user_complementary_step"] = True
        self.__onboarding_steps["current_onboarding_step"] = "user_document_validator"
        return self

    def user_document_validator_step(self, current_user, document_exists: bool):
        self.__onboarding_steps["user_document_validator"] = True
        self.__onboarding_steps["current_onboarding_step"] = "user_data_validation"
        return self

    def user_data_validation_step(self, current_user):
        self.__onboarding_steps["user_data_validation"] = True
        self.__onboarding_steps["current_onboarding_step"] = "user_electronic_signature"
        return self

    def user_electronic_signature_step(self, current_user):
        self.__onboarding_steps["user_electronic_signature"] = True
        return self

    def is_finished(self):
        self.__onboarding_steps["current_onboarding_step"] = "finished"
        self.__onboarding_steps["finished"] = True

    async def build(self) -> dict:
        self.is_finished()
        onboarding_steps = self.__onboarding_steps
        return onboarding_steps


fake_builder = OnboardingStepBuilderBRStub()


@mark.asyncio
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=find_user_return_dummy
)
async def test_onboarding_user_current_step_br(
    find_user_mock, file_exists_mock, monkeypatch
):
    monkeypatch.setattr(
        target=OnboardingSteps, name="steps_builder", value=OnboardingStepBuilderBRStub
    )
    result = await OnboardingSteps.onboarding_user_current_step_br(payload_dummy)
    expected_result = {
        "current_onboarding_step": "finished",
        "suitability_step": True,
        "user_identifier_data_step": True,
        "user_selfie_step": True,
        "user_complementary_step": True,
        "user_document_validator": True,
        "user_data_validation": True,
        "user_electronic_signature": True,
        "finished": True,
    }
    assert result == expected_result


@mark.asyncio
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=None
)
async def test_onboarding_user_current_step_br_when_user_is_none(
    find_user_mock, file_exists_mock, monkeypatch
):
    monkeypatch.setattr(
        target=OnboardingSteps, name="steps_builder", value=OnboardingStepBuilderBRStub
    )
    with raises(BadRequestError):
        result = await OnboardingSteps.onboarding_user_current_step_br(payload_dummy)
