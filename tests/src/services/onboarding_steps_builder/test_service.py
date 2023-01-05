from unittest.mock import patch
from decouple import AutoConfig

from func.src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
from func.src.domain.user.model import User
from func.src.services.onboarding_steps_builder.service import OnboardingStepBuilder


@patch.object(AutoConfig, "__call__", return_value="picpay")
@patch.object(OnboardingFraudStatusEnum, "__gt__", return_value=False)
def test_get_is_approved_when_reproved_first(mock_comparison, mock_config):
    result = OnboardingStepBuilder(User({})).get_is_approved(
        OnboardingFraudStatusEnum.REPROVED, OnboardingFraudStatusEnum.APPROVED
    )
    mock_comparison.assert_not_called()
    assert result == OnboardingFraudStatusEnum.REPROVED


@patch.object(AutoConfig, "__call__", return_value="picpay")
@patch.object(OnboardingFraudStatusEnum, "__gt__", return_value=False)
def test_get_is_approved_when_approved_first(mock_comparison, mock_config):
    result = OnboardingStepBuilder(User({})).get_is_approved(
        OnboardingFraudStatusEnum.APPROVED, OnboardingFraudStatusEnum.REPROVED
    )
    mock_comparison.assert_called_once_with(OnboardingFraudStatusEnum.APPROVED)
    assert result == OnboardingFraudStatusEnum.REPROVED
