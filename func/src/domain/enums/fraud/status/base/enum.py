from enum import Enum


class OnboardingFraudStatusEnum(Enum):
    APPROVED = "approved"
    REPROVED = "reproved"
    PENDING = "pending"

    def __gt__(self, other):
        if (
            self != OnboardingFraudStatusEnum.REPROVED and
            other == OnboardingFraudStatusEnum.REPROVED
        ) or (
            self == OnboardingFraudStatusEnum.APPROVED and
            other != OnboardingFraudStatusEnum.APPROVED
        ) or (self == other):
            return False
        return True

    def __lt__(self, other):
        if (
            self == OnboardingFraudStatusEnum.REPROVED and
            other != OnboardingFraudStatusEnum.REPROVED
        ) or (
            self != OnboardingFraudStatusEnum.APPROVED and
            other == OnboardingFraudStatusEnum.APPROVED
        ) or (self == other):
            return False
        return True
