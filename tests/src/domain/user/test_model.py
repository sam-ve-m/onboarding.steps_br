from unittest.mock import MagicMock

from pytest_steps import test_steps

from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
from src.domain.enums.fraud.status.bureau.enum import BureauStatus
from src.domain.user.model import User

fake_instance = MagicMock()


@test_steps("missing_refusal", "missing_profile", "missing_none")
def test_has_suitability_true():
    fake_instance._User__suitability_profile = True
    fake_instance._User__signed_refusal_term = None
    assert User.has_suitability(fake_instance) is True
    yield

    fake_instance._User__suitability_profile = None
    fake_instance._User__signed_refusal_term = True
    assert User.has_suitability(fake_instance) is True
    yield

    fake_instance._User__suitability_profile = True
    fake_instance._User__signed_refusal_term = True
    assert User.has_suitability(fake_instance) is True
    yield


def test_has_suitability_false():
    fake_instance._User__suitability_profile = None
    fake_instance._User__signed_refusal_term = None
    assert User.has_suitability(fake_instance) is False


@test_steps("missing_cpf", "missing_phone", "missing_cpf_and_phone")
def test_has_identifier_data_false():
    fake_instance._User__cpf = None
    fake_instance._User__cel_phone = True
    assert User.has_identifier_data(fake_instance) is False
    yield

    fake_instance._User__cpf = True
    fake_instance._User__cel_phone = None
    assert User.has_identifier_data(fake_instance) is False
    yield

    fake_instance._User__cpf = None
    fake_instance._User__cel_phone = None
    assert User.has_identifier_data(fake_instance) is False
    yield


def test_has_identifier_data_true():
    fake_instance._User__cpf = True
    fake_instance._User__cel_phone = True
    assert User.has_identifier_data(fake_instance) is True


def test_has_complementary_data_true():
    fake_instance._User__marital_status = True
    assert User.has_complementary_data(fake_instance) is True


def test_has_complementary_data_false():
    fake_instance._User__marital_status = None
    assert User.has_complementary_data(fake_instance) is False


def test_has_validated_data_true():
    fake_instance._User__bureau_status_validated = True
    assert User.has_validated_data(fake_instance) is True


def test_has_validated_data_false():
    fake_instance._User__bureau_status_validated = None
    assert User.has_validated_data(fake_instance) is False


def test_has_eletronic_signature_true():
    fake_instance._User__electronic_signature = True
    assert User.has_eletronic_signature(fake_instance) is True


def test_has_eletronic_signature_false():
    fake_instance._User__electronic_signature = None
    assert User.has_eletronic_signature(fake_instance) is False


def test_cpf_validation_status(monkeypatch):
    mocked_fraud_enum = MagicMock()
    mocked_status_enum = MagicMock()
    monkeypatch.setattr(BureauStatus, "_member_map_", mocked_status_enum)
    monkeypatch.setattr(OnboardingFraudStatusEnum, "_member_map_", mocked_fraud_enum)
    fake_instance._User__fraud_validation_cpf = True
    result = User.cpf_validation_status.fget(fake_instance)
    assert result == mocked_fraud_enum[mocked_status_enum[fake_instance._User__fraud_validation_cpf].value]


def test_cpf_validation_status_none():
    fake_instance._User__fraud_validation_cpf = None
    result = User.cpf_validation_status.fget(fake_instance)
    assert result == OnboardingFraudStatusEnum.PENDING


def test_score_validation_status(monkeypatch):
    mocked_fraud_enum = MagicMock()
    mocked_status_enum = MagicMock()
    monkeypatch.setattr(BureauStatus, "_member_map_", mocked_status_enum)
    monkeypatch.setattr(OnboardingFraudStatusEnum, "_member_map_", mocked_fraud_enum)
    fake_instance._User__fraud_validation_score = True
    result = User.score_validation_status.fget(fake_instance)
    assert result == mocked_fraud_enum[mocked_status_enum[fake_instance._User__fraud_validation_score].value]


def test_score_validation_status_none():
    fake_instance._User__fraud_validation_score = None
    result = User.score_validation_status.fget(fake_instance)
    assert result == OnboardingFraudStatusEnum.PENDING
