from app.general.service import GeneralService
from app.accounts.services import UserService
from app.project.services import ProjectService


class SERVICE_NAMES:
    GeneralService = "general_service"
    UserService = "user_service"
    ProjectService = "project_service"


class ServiceLocator:
    service = {}

    general_service: GeneralService
    user_service: UserService
    project_service: ProjectService

    def __init__(self):
        self._services = {}

    def register(self, name, service):
        self._services[name] = service

    def get(self, name):
        return self._services[name]

    def __getitem__(self, name):
        return self.get(name)

    def __getattr__(self, name):
        return self.get(name)


#  register services


service_locator = ServiceLocator()

service_locator.register(SERVICE_NAMES.GeneralService, GeneralService())
service_locator.register(SERVICE_NAMES.UserService, UserService())
service_locator.register(SERVICE_NAMES.ProjectService, ProjectService())
