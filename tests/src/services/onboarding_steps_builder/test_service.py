from unittest.mock import patch

from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
from src.services.onboarding_steps_builder.service import OnboardingStepBuilder


@patch.object(OnboardingFraudStatusEnum, "__gt__", return_value=False)
def test_get_is_approved_when_reproved_first(mock_comparison):
    result = OnboardingStepBuilder.get_is_approved(
        OnboardingFraudStatusEnum.REPROVED,
        OnboardingFraudStatusEnum.APPROVED
    )
    mock_comparison.assert_not_called()
    assert result == OnboardingFraudStatusEnum.REPROVED


@patch.object(OnboardingFraudStatusEnum, "__gt__", return_value=False)
def test_get_is_approved_when_approved_first(mock_comparison):
    result = OnboardingStepBuilder.get_is_approved(
        OnboardingFraudStatusEnum.APPROVED,
        OnboardingFraudStatusEnum.REPROVED
    )
    mock_comparison.assert_called_once_with(
        OnboardingFraudStatusEnum.APPROVED
    )
    assert result == OnboardingFraudStatusEnum.REPROVED
