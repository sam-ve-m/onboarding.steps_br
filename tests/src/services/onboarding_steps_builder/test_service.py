from unittest.mock import MagicMock, patch

from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
from src.domain.user.model import User
from src.services.onboarding_steps_builder.service import OnboardingStepBuilder


@patch.object(OnboardingFraudStatusEnum, "__gt__", return_value=False)
def test_get_is_approved_when_reproved_and_approved(mock_comparison):
    user = User(user_document={
        "bureau_validations": {
        "cpf": "REPROVADO",
        "score": "APROVADO",
        "blocklist": "APPROVED"}
    })
    builder = OnboardingStepBuilder(user)
    result = builder.get_is_approved()
    mock_comparison.assert_called_once_with(
        OnboardingFraudStatusEnum.REPROVED
    )
    assert result == OnboardingFraudStatusEnum.REPROVED


def test_get_is_approved_when_pending_and_reproved():
    user = User(user_document={
        "bureau_validations": {
        "cpf": None,
        "score": None,
        "blocklist": "REPROVED"}
    })
    builder = OnboardingStepBuilder(user)
    result = builder.get_is_approved()
    assert result == OnboardingFraudStatusEnum.REPROVED


def test_get_is_approved_when_pending():
    user = User(user_document={
        "bureau_validations": {
            "cpf": None,
            "score": "APROVADO",
            "blocklist": "APPROVED"}
    })
    builder = OnboardingStepBuilder(user)
    result = builder.get_is_approved()
    assert result == OnboardingFraudStatusEnum.PENDING


def test_get_is_approved():
    user = User(user_document={
        "bureau_validations": {
            "cpf": "APROVADO",
            "score": "APROVADO",
            "blocklist": "APPROVED"}
    })
    builder = OnboardingStepBuilder(user)
    result = builder.get_is_approved()
    assert result == OnboardingFraudStatusEnum.APPROVED
