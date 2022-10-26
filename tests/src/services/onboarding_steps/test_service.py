from unittest.mock import patch

from decouple import AutoConfig
from pytest import mark

from src.domain.user.model import User
from src.repositories.file.repository import FileRepository
from src.repositories.user.repository import UserRepository
from src.services.onboarding_steps.service import OnboardingSteps

payload_dummy = {"user": {"unique_id": "test"}}
user_document_dummy = {
    "suitability": "data",
    "terms": {"term_refusal": "data"},
    "term_refusal": "data",
    "identifier_document": {"cpf": "data"},
    "phone": "data",
    "marital": "data",
    "bureau_status": "data",
    "is_bureau_data_validated": "data",
    "electronic_signature": "data",
    "origin": "picpay",
}

find_user_return_dummy_with_all_data = User(user_document_dummy)
find_user_return_dummy_with_no_data = User({})

build_return_dummy_all_true = {
    "suitability": True,
    "identifier_data": True,
    "selfie": True,
    "complementary_data": True,
    "data_validation": True,
    "electronic_signature": True,
    "finished": True,
    "current_step": "finished",
    "anti_fraud": "pending",
}
build_return_dummy_all_true_and_anti_fraud_bypass = {
    "suitability": True,
    "identifier_data": True,
    "selfie": True,
    "complementary_data": True,
    "data_validation": True,
    "electronic_signature": True,
    "finished": True,
    "current_step": "finished",
    "anti_fraud": "approved",
}
build_return_dummy_all_false = {
    "suitability": False,
    "identifier_data": False,
    "selfie": False,
    "complementary_data": False,
    "data_validation": False,
    "electronic_signature": False,
    "finished": False,
    "current_step": "suitability",
    "anti_fraud": "pending",
}


@mark.asyncio
@patch.object(AutoConfig, "__call__", return_value="")
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=find_user_return_dummy_with_all_data
)
async def test_onboarding_user_current_step_br(
    find_user_mock, file_exists_mock, config_mock
):
    result = await OnboardingSteps.onboarding_user_current_step_br(payload_dummy)
    expected_result = build_return_dummy_all_true
    assert result == expected_result


@mark.asyncio
@patch.object(AutoConfig, "__call__", return_value="picpay")
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=find_user_return_dummy_with_all_data
)
async def test_onboarding_user_current_step_br_with_anti_fraud_bypass(
    find_user_mock, file_exists_mock, config_mock
):
    result = await OnboardingSteps.onboarding_user_current_step_br(payload_dummy)
    expected_result = build_return_dummy_all_true_and_anti_fraud_bypass
    assert result == expected_result


@mark.asyncio
@patch.object(AutoConfig, "__call__", return_value="picpay")
@patch.object(FileRepository, "user_file_exists", return_value=True)
@patch.object(
    UserRepository, "find_user", return_value=find_user_return_dummy_with_no_data
)
async def test_onboarding_user_current_step_br_when_user_is_none(
    find_user_mock, file_exists_mock, config_mock
):
    result = await OnboardingSteps.onboarding_user_current_step_br(payload_dummy)
    expected_result = build_return_dummy_all_false
    assert result == expected_result
