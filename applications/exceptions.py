from users.exceptions import UserDoesNotExist


class ApplicationException(BaseException):
    pass


class OwnerDoesNotExist(ApplicationException, UserDoesNotExist):
    pass


class ManagerDoesNotExist(ApplicationException, UserDoesNotExist):
    pass


class NotClientOrCompany(ApplicationException):
    pass


class NotManager(ApplicationException):
    pass


class NoServices(ApplicationException):
    pass
