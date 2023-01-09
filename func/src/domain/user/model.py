from func.src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
from func.src.domain.enums.fraud.status.bureau.enum import BureauStatus


class User:
    def __init__(self, user_document: dict):
        self.__suitability_profile = user_document.get("suitability")
        self.__terms = user_document.get("terms")
        self.__signed_refusal_term = user_document.get("terms", {}).get("term_refusal")
        self.__cpf = user_document.get("identifier_document", {}).get("cpf")
        self.__cel_phone = user_document.get("phone")
        self.__marital_status = user_document.get("marital")
        self.__bureau_status = user_document.get("bureau_status")
        self.__origin = user_document.get("origin")
        self.__bureau_status_validated = user_document.get("is_bureau_data_validated")
        self.__electronic_signature = user_document.get("electronic_signature")
        bureau_validations = user_document.get("bureau_validations", {})
        self.__fraud_validation_cpf = bureau_validations.get("cpf")
        self.__fraud_validation_score = bureau_validations.get("score")
        self.__fraud_validation_blocklist = bureau_validations.get("blocklist")

    def get_bureau_status(self):
        return self.__bureau_status

    def get_origin(self):
        return self.__origin

    def has_suitability(self) -> bool:
        suitability = self.__suitability_profile is not None
        signed_refusal_term = self.__signed_refusal_term is not None
        has_suitability = suitability or signed_refusal_term
        return has_suitability

    def has_identifier_data(self) -> bool:
        cpf = self.__cpf is not None
        cell_phone = self.__cel_phone is not None
        has_identifier_data = cpf and cell_phone
        return has_identifier_data

    def has_complementary_data(self) -> bool:
        marital = self.__marital_status is not None
        has_complementary_data = marital
        return has_complementary_data

    def has_validated_data(self) -> bool:
        has_validated_data = self.__bureau_status_validated is not None
        return has_validated_data

    def has_eletronic_signature(self) -> bool:
        has_electronic_signature = self.__electronic_signature is not None
        return has_electronic_signature

    @property
    def cpf_validation_status(self) -> OnboardingFraudStatusEnum:
        if not self.__fraud_validation_cpf:
            return OnboardingFraudStatusEnum.PENDING
        bureau_status = BureauStatus[self.__fraud_validation_cpf]
        return OnboardingFraudStatusEnum[bureau_status.value]

    @property
    def score_validation_status(self) -> OnboardingFraudStatusEnum:
        if not self.__fraud_validation_score:
            return OnboardingFraudStatusEnum.PENDING
        bureau_status = BureauStatus[self.__fraud_validation_score]
        return OnboardingFraudStatusEnum[bureau_status.value]
