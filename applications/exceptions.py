from users.exceptions import UserDoesNotExist


class OwnerDoesNotExist(UserDoesNotExist):
    pass


class ManagerDoesNotExist(UserDoesNotExist):
    pass


class NotClientOrCompany(BaseException):
    pass


class NotManager(BaseException):
    pass
