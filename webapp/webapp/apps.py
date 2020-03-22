from planner.apps import PlannerConfig
from users.apps import UsersConfig

class PlannerWrapperConfig(PlannerConfig):
    verbose_name = "plan it"


class UsersWrapperConfig(UsersConfig):
    verbose_name = "users"
