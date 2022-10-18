from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum


def test_relation_with_approved_and_reproved():
    assert OnboardingFraudStatusEnum.REPROVED > OnboardingFraudStatusEnum.APPROVED
    assert OnboardingFraudStatusEnum.APPROVED < OnboardingFraudStatusEnum.REPROVED
    assert (OnboardingFraudStatusEnum.APPROVED > OnboardingFraudStatusEnum.REPROVED) is False
    assert (OnboardingFraudStatusEnum.REPROVED < OnboardingFraudStatusEnum.APPROVED) is False


def test_relation_with_approved_and_pending():
    assert OnboardingFraudStatusEnum.PENDING > OnboardingFraudStatusEnum.APPROVED
    assert OnboardingFraudStatusEnum.APPROVED < OnboardingFraudStatusEnum.PENDING
    assert (OnboardingFraudStatusEnum.APPROVED > OnboardingFraudStatusEnum.PENDING) is False
    assert (OnboardingFraudStatusEnum.PENDING < OnboardingFraudStatusEnum.APPROVED) is False


def test_relation_with_reproved_and_pending():
    assert OnboardingFraudStatusEnum.REPROVED > OnboardingFraudStatusEnum.PENDING
    assert OnboardingFraudStatusEnum.PENDING < OnboardingFraudStatusEnum.REPROVED
    assert (OnboardingFraudStatusEnum.PENDING > OnboardingFraudStatusEnum.REPROVED) is False
    assert (OnboardingFraudStatusEnum.REPROVED < OnboardingFraudStatusEnum.PENDING) is False


def test_relation_with_equals():
    assert (OnboardingFraudStatusEnum.REPROVED < OnboardingFraudStatusEnum.REPROVED) is False
    assert (OnboardingFraudStatusEnum.REPROVED > OnboardingFraudStatusEnum.REPROVED) is False

    assert (OnboardingFraudStatusEnum.APPROVED < OnboardingFraudStatusEnum.APPROVED) is False
    assert (OnboardingFraudStatusEnum.APPROVED > OnboardingFraudStatusEnum.APPROVED) is False

    assert (OnboardingFraudStatusEnum.PENDING < OnboardingFraudStatusEnum.PENDING) is False
    assert (OnboardingFraudStatusEnum.PENDING > OnboardingFraudStatusEnum.PENDING) is False
