from enum import Enum


class OnboardingStepsEnum(Enum):
    CURRENT = "current_step"
    SUITABILITY = "suitability"
    IDENTIFIER_DATA = "identifier_data"
    SELFIE = "selfie"
    COMPLEMENTARY_DATA = "complementary_data"
    DOCUMENT_VALIDATOR = "document_validator"
    DATA_VALIDATION = "data_validation"
    ELECTRONIC_SIGNATURE = "electronic_signature"
    FINISHED = "finished"
