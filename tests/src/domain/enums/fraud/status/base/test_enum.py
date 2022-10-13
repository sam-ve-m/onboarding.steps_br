from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum


def test_relation_with_approved_and_reproved():
    assert OnboardingFraudStatusEnum.REPROVED > OnboardingFraudStatusEnum.APPROVED
    assert (OnboardingFraudStatusEnum.REPROVED < OnboardingFraudStatusEnum.APPROVED) is False


def test_relation_with_approved_and_pending():
    assert OnboardingFraudStatusEnum.PENDING > OnboardingFraudStatusEnum.APPROVED
    assert (OnboardingFraudStatusEnum.PENDING < OnboardingFraudStatusEnum.APPROVED) is False


def test_relation_with_reproved_and_pending():
    assert OnboardingFraudStatusEnum.REPROVED > OnboardingFraudStatusEnum.PENDING
    assert (OnboardingFraudStatusEnum.REPROVED < OnboardingFraudStatusEnum.PENDING) is False


def test_relation_with_equals():
    assert (OnboardingFraudStatusEnum.REPROVED < OnboardingFraudStatusEnum.REPROVED) is False
    assert (OnboardingFraudStatusEnum.REPROVED > OnboardingFraudStatusEnum.REPROVED) is False

    assert (OnboardingFraudStatusEnum.APPROVED < OnboardingFraudStatusEnum.APPROVED) is False
    assert (OnboardingFraudStatusEnum.APPROVED > OnboardingFraudStatusEnum.APPROVED) is False

    assert (OnboardingFraudStatusEnum.PENDING < OnboardingFraudStatusEnum.PENDING) is False
    assert (OnboardingFraudStatusEnum.PENDING > OnboardingFraudStatusEnum.PENDING) is False
