from django.contrib.auth.tokens import default_token_generator
from djoser import utils
from djoser.compat import get_user_email
from djoser.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users import services, serializers, permissions, email, exceptions, models


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    token_generator = default_token_generator
    user_service = services.UserService()
    permission_classes = [IsAuthenticated]

    def permission_denied(self, request, **kwargs):
        if (
                settings.HIDE_USERS
                and request.user.is_authenticated
                and self.action in ["update", "partial_update", "list", "retrieve"]
        ):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = self.user_service.get_list()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "activate":
            self.permission_classes = [IsAuthenticated, permissions.IsManager]
        elif self.action == "resend_activation":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "list":
            self.permission_classes = settings.PERMISSIONS.user_list
        elif self.action == "reset_password":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "reset_password_confirm":
            self.permission_classes = settings.PERMISSIONS.password_reset_confirm
        elif self.action == "set_password":
            self.permission_classes = settings.PERMISSIONS.set_password
        elif self.action == "set_username":
            self.permission_classes = settings.PERMISSIONS.set_username
        elif self.action == "reset_username":
            self.permission_classes = settings.PERMISSIONS.username_reset
        elif self.action == "reset_username_confirm":
            self.permission_classes = settings.PERMISSIONS.username_reset_confirm
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.UserCreateSerializer
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return settings.SERIALIZERS.activation
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class

    def get_instance(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.user_service.create(serializer.validated_data)
        serializer = serializers.UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        super().perform_update(serializer)
        user = serializer.instance
        # should we send activation email after update?
        if settings.SEND_ACTIVATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.activation(self.request, context).send(to)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        if instance == request.user:
            utils.logout_user(self.request)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["get", "put", "patch", "delete"], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == "GET":
            return self.retrieve(request, *args, **kwargs)
        elif request.method == "PUT":
            return self.update(request, *args, **kwargs)
        elif request.method == "PATCH":
            return self.partial_update(request, *args, **kwargs)
        elif request.method == "DELETE":
            return self.destroy(request, *args, **kwargs)

    # @action(["post"], detail=False)
    # def resend_activation(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.get_user(is_active=False)
    #
    #     if not settings.SEND_ACTIVATION_EMAIL or not user:
    #         return Response(status=status.HTTP_400_BAD_REQUEST)
    #
    #     context = {"user": user}
    #     to = [get_user_email(user)]
    #     settings.EMAIL.activation(self.request, context).send(to)
    #
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(["post"], detail=False)
    # def set_password(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     self.request.user.set_password(serializer.data["new_password"])
    #     self.request.user.save()
    #
    #     if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
    #         context = {"user": self.request.user}
    #         to = [get_user_email(self.request.user)]
    #         settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
    #
    #     if settings.LOGOUT_ON_PASSWORD_CHANGE:
    #         utils.logout_user(self.request)
    #     elif settings.CREATE_SESSION_ON_LOGIN:
    #         update_session_auth_hash(self.request, self.request.user)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(["post"], detail=False)
    # def reset_password(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.get_user()
    #
    #     if user:
    #         context = {"user": user}
    #         to = [get_user_email(user)]
    #         settings.EMAIL.password_reset(self.request, context).send(to)
    #
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(["post"], detail=False)
    # def reset_password_confirm(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     serializer.user.set_password(serializer.data["new_password"])
    #     if hasattr(serializer.user, "last_login"):
    #         serializer.user.last_login = now()
    #     serializer.user.save()
    #
    #     if settings.PASSWORD_CHANGED_EMAIL_CONFIRMATION:
    #         context = {"user": serializer.user}
    #         to = [get_user_email(serializer.user)]
    #         settings.EMAIL.password_changed_confirmation(self.request, context).send(to)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(["post"], detail=False, url_path="set_{}".format(User.USERNAME_FIELD))
    # def set_username(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = self.request.user
    #     new_username = serializer.data["new_" + User.USERNAME_FIELD]
    #
    #     setattr(user, User.USERNAME_FIELD, new_username)
    #     user.save()
    #     if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
    #         context = {"user": user}
    #         to = [get_user_email(user)]
    #         settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(["post"], detail=False, url_path="reset_{}".format(User.USERNAME_FIELD))
    # def reset_username(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.get_user()
    #
    #     if user:
    #         context = {"user": user}
    #         to = [get_user_email(user)]
    #         settings.EMAIL.username_reset(self.request, context).send(to)
    #
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # @action(
    #     ["post"], detail=False, url_path="reset_{}_confirm".format(User.USERNAME_FIELD)
    # )
    # def reset_username_confirm(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     new_username = serializer.data["new_" + User.USERNAME_FIELD]
    #
    #     setattr(serializer.user, User.USERNAME_FIELD, new_username)
    #     if hasattr(serializer.user, "last_login"):
    #         serializer.user.last_login = now()
    #     serializer.user.save()
    #
    #     if settings.USERNAME_CHANGED_EMAIL_CONFIRMATION:
    #         context = {"user": serializer.user}
    #         to = [get_user_email(serializer.user)]
    #         settings.EMAIL.username_changed_confirmation(self.request, context).send(to)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @action(['head'], detail=False, url_path=r'exists/(?P<user_email>[^/]+)')
    def exists(self, request, user_email):
        try:
            print(user_email)
            models.User.objects.get(email=user_email)
            return Response(status=status.HTTP_200_OK)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(['get'], detail=True)
    def activate(self, request, pk, *args, **kwargs):
        try:
            user = self.user_service.get(pk)
        except exceptions.UserDoesNotExist as e:
            return Response(data={'detail': str(e)}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            data = {'detail': 'User already active.'}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        password = self.user_service.set_password(user)
        self.user_service.activate(user)

        context = {'user': user, 'password': password}
        to = [get_user_email(user)]

        email.ActivationEmail(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)


class RolesViewSet(viewsets.ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [IsAuthenticated]


class CitiesViewSet(viewsets.ModelViewSet):
    queryset = models.City.objects.all()
    serializer_class = serializers.CitySerializer
    permission_classes = [IsAuthenticated]
