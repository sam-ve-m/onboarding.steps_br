from unittest.mock import MagicMock

from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
from src.services.onboarding_steps_builder.service import OnboardingStepBuilder
from pytest_steps import test_steps


@test_steps('reproved_and_aprovved', 'reproved_and_pending')
def test_get_is_approved_when_reproved(monkeypatch):
    monkeypatch.setattr(
        OnboardingFraudStatusEnum, "__gt__",
        MagicMock(return_value=False)
    )
    dummy_anti_fraud = {
        0: OnboardingFraudStatusEnum.APPROVED,
        1: OnboardingFraudStatusEnum.REPROVED,
        2: OnboardingFraudStatusEnum.APPROVED,
    }
    result = OnboardingStepBuilder.get_is_approved(dummy_anti_fraud)
    assert result == OnboardingFraudStatusEnum.REPROVED
    yield
    dummy_anti_fraud = {
        0: OnboardingFraudStatusEnum.PENDING,
        1: OnboardingFraudStatusEnum.REPROVED,
        2: OnboardingFraudStatusEnum.APPROVED,
    }
    result = OnboardingStepBuilder.get_is_approved(dummy_anti_fraud)
    assert result == OnboardingFraudStatusEnum.REPROVED
    yield


def test_get_is_approved_when_pending():
    dummy_anti_fraud = {
        0: OnboardingFraudStatusEnum.APPROVED,
        1: OnboardingFraudStatusEnum.PENDING,
        2: OnboardingFraudStatusEnum.APPROVED,
    }
    result = OnboardingStepBuilder.get_is_approved(dummy_anti_fraud)
    assert result == OnboardingFraudStatusEnum.PENDING


def test_get_is_approved():
    dummy_anti_fraud = {
        0: OnboardingFraudStatusEnum.APPROVED,
        1: OnboardingFraudStatusEnum.APPROVED,
        2: OnboardingFraudStatusEnum.APPROVED,
    }
    result = OnboardingStepBuilder.get_is_approved(dummy_anti_fraud)
    assert result == OnboardingFraudStatusEnum.APPROVED
