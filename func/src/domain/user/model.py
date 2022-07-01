from src.domain.enums.caf.status import CAFStatus


class User:
    def __init__(self, user_document: dict):
        self.__suitability_profile = user_document.get("suitability")
        self.__terms = user_document.get("terms", {})
        self.__signed_refusal_term = self.__terms.get("term_refusal")
        self.__cpf = user_document.get("identifier_document", {}).get("cpf")
        self.__cel_phone = user_document.get("phone")
        self.__marital_status = user_document.get("marital")
        self.__bureau_status = user_document.get("bureau_status")
        self.__bureau_status_validated = user_document.get("is_bureau_data_validated")
        self.__electronic_signature = user_document.get("electronic_signature")

    def get_bureau_status(self):
        return self.__bureau_status

    def has_suitability(self) -> bool:
        suitability = bool(self.__suitability_profile)
        signed_refusal_term = bool(self.__terms.get("term_refusal"))
        has_suitability = suitability or signed_refusal_term
        return has_suitability

    def has_identifier_data(self) -> bool:
        cpf = bool(self.__cpf)
        cell_phone = bool(self.__cel_phone)
        has_identifier_data = cpf and cell_phone
        return has_identifier_data

    def has_complementary_data(self) -> bool:
        marital = bool(self.__marital_status)
        has_complementary_data = marital
        return has_complementary_data

    def has_document_validated(self) -> bool:
        bureau_status = bool(self.__bureau_status)
        bureau_status_is_different_from_document = (
            self.__bureau_status != CAFStatus.DOCUMENT.value
        )
        has_document_validated = (
            bureau_status and bureau_status_is_different_from_document
        )
        return has_document_validated

    def has_validated_data(self) -> bool:
        has_validated_data = bool(self.__bureau_status_validated)
        return has_validated_data

    def has_eletronic_signature(self) -> bool:
        has_electronic_signature = bool(self.__electronic_signature)
        return has_electronic_signature
