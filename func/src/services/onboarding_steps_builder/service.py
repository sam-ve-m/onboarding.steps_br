from src.domain.enums.caf.status import CAFStatus
from src.domain.enums.onboarding_steps.onboarding_steps import OnboardingStepsEnum
from src.domain.user.model import User


class OnboardingStepBuilder:
    def __init__(self, user: User):
        self.__user = user
        self.__step = 0
        self.__onboarding_steps = {
            0: OnboardingStepsEnum.SUITABILITY,
            1: OnboardingStepsEnum.IDENTIFIER_DATA,
            2: OnboardingStepsEnum.SELFIE,
            3: OnboardingStepsEnum.COMPLEMENTARY_DATA,
            4: OnboardingStepsEnum.DOCUMENT_VALIDATOR,
            5: OnboardingStepsEnum.DATA_VALIDATION,
            6: OnboardingStepsEnum.ELECTRONIC_SIGNATURE,
            7: OnboardingStepsEnum.FINISHED,
        }

    def get_current_step(self):
        step = self.__onboarding_steps.get(self.__step)
        return step

    def is_current_step(self, step: OnboardingStepsEnum) -> bool:
        current_step = self.get_current_step()
        is_current_step = step == current_step
        return is_current_step

    def user_suitability_step(self) -> bool:
        suitability = self.__user.has_suitability()
        is_current_step = self.is_current_step(OnboardingStepsEnum.SUITABILITY)
        suitability_step = suitability and is_current_step
        if suitability_step:
            self.__step += 1
        return suitability_step

    def user_identifier_step(self) -> bool:
        identifier = self.__user.has_identifier_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.IDENTIFIER_DATA)
        identifier_step = identifier and is_current_step
        if identifier_step:
            self.__step += 1
        return identifier_step

    def user_selfie_step(self, user_selfie_exists: bool) -> bool:
        selfie = user_selfie_exists
        is_current_step = self.is_current_step(OnboardingStepsEnum.SELFIE)
        selfie_step = selfie and is_current_step
        if selfie_step:
            self.__step += 1
        return selfie_step

    def user_complementary_step(self) -> bool:
        complementary = self.__user.has_complementary_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.COMPLEMENTARY_DATA)
        complementary_step = complementary and is_current_step
        if complementary_step:
            self.__step += 1
        return complementary_step

    def user_document_validator_step(self, document_exists: bool) -> bool:
        document_validator = self.__user.has_document_validated()
        is_current_step = self.is_current_step(OnboardingStepsEnum.DOCUMENT_VALIDATOR)
        document_validator_step = (
            document_validator or document_exists
        ) and is_current_step
        if document_validator_step:
            self.__step += 1
        return document_validator_step

    def user_data_validation_step(self) -> bool:
        validation_data = self.__user.has_validated_data()
        is_current_step = self.is_current_step(OnboardingStepsEnum.DATA_VALIDATION)
        validation_data_step = validation_data and is_current_step
        if validation_data_step:
            self.__step += 1
        return validation_data_step

    def user_electronic_signature_step(self) -> bool:
        eletronic_signature = self.__user.has_eletronic_signature()
        is_current_step = self.is_current_step(OnboardingStepsEnum.ELECTRONIC_SIGNATURE)
        eletronic_signature_step = eletronic_signature and is_current_step
        if eletronic_signature_step:
            self.__step += 1
        return eletronic_signature_step

    async def build(self, selfie_exists: bool, document_exists: bool) -> dict:
        onboarding_steps = {
            OnboardingStepsEnum.SUITABILITY.value: self.user_suitability_step(),
            OnboardingStepsEnum.IDENTIFIER_DATA.value: self.user_identifier_step(),
            OnboardingStepsEnum.SELFIE.value: self.user_selfie_step(selfie_exists),
            OnboardingStepsEnum.COMPLEMENTARY_DATA.value: self.user_complementary_step(),
            OnboardingStepsEnum.DOCUMENT_VALIDATOR.value: self.user_document_validator_step(
                document_exists
            ),
            OnboardingStepsEnum.DATA_VALIDATION.value: self.user_data_validation_step(),
            OnboardingStepsEnum.ELECTRONIC_SIGNATURE.value: self.user_electronic_signature_step(),
            OnboardingStepsEnum.CURRENT.value: self.get_current_step().value,
        }

        bureau_status = self.__user.get_bureau_status()
        if bureau_status == CAFStatus.REFUSED.value:
            onboarding_steps[OnboardingStepsEnum.CURRENT.value] = bureau_status

        return onboarding_steps