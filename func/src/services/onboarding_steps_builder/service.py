from src.domain.enums.fraud.onboarding_steps import OnboardingFraudEnum
from src.domain.enums.fraud.status.base.enum import OnboardingFraudStatusEnum
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
            4: OnboardingStepsEnum.DATA_VALIDATION,
            5: OnboardingStepsEnum.ELECTRONIC_SIGNATURE,
            6: OnboardingStepsEnum.FINISHED,
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

    def onboarding_is_finished(self) -> bool:
        is_finished = self.is_current_step(OnboardingStepsEnum.FINISHED)
        return is_finished

    def get_bureaux_status(self) -> OnboardingFraudStatusEnum:
        return max(
            self.__user.cpf_validation_status,
            self.__user.score_validation_status,
        )

    def get_blocklist_status(self) -> OnboardingFraudStatusEnum:
        return self.__user.blocklist_validation_status

    def get_is_approved(self) -> OnboardingFraudStatusEnum:
        status = OnboardingFraudStatusEnum.APPROVED
        anti_fraud_validations = [self.get_bureaux_status(), self.get_blocklist_status()]
        for fraud_status in anti_fraud_validations:
            if fraud_status == OnboardingFraudStatusEnum.REPROVED:
                return OnboardingFraudStatusEnum.REPROVED
            status = max(status, fraud_status)
        return status

    async def build(self, selfie_exists: bool) -> dict:
        onboarding_steps = {
            OnboardingStepsEnum.SUITABILITY.value: self.user_suitability_step(),
            OnboardingStepsEnum.IDENTIFIER_DATA.value: self.user_identifier_step(),
            OnboardingStepsEnum.SELFIE.value: self.user_selfie_step(selfie_exists),
            OnboardingStepsEnum.COMPLEMENTARY_DATA.value: self.user_complementary_step(),
            OnboardingStepsEnum.DATA_VALIDATION.value: self.user_data_validation_step(),
            OnboardingStepsEnum.ELECTRONIC_SIGNATURE.value: self.user_electronic_signature_step(),
            OnboardingStepsEnum.FINISHED.value: self.onboarding_is_finished(),
            OnboardingStepsEnum.CURRENT.value: self.get_current_step().value,
            OnboardingFraudEnum.OBJECT_WRAP_NAME.value: self.get_is_approved().value,
        }
        return onboarding_steps
