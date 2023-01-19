class PartnerServiceException(BaseException):
    pass


class UserIsNotPartner(PartnerServiceException):
    pass
