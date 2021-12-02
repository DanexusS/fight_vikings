class AbstractObjective:
    def __init__(self, description):
        self.description = description
        self.is_completed = False
        self.parent = None

    def __repr__(self):
        return self.description


#   Примеры заданий
class KillObjective(AbstractObjective):
    def __init__(self, description, enemy_type, amount):
        super().__init__(description)

        self.enemy_type = enemy_type
        self.amount = amount


class DiscoverObjective(AbstractObjective):
    def __init__(self, description, location_type):
        super().__init__(description)

        self.location_type = location_type


class MissionObject:
    def __init__(self, title, description, rewards, *objectives):
        self.objectives = list(*objectives)
        for obj in self.objectives:
            obj.parent = self

        self.title = title
        self.rewards = rewards
        self.description = description
        self.is_completed = False
        self.current_objective = self.objectives[0]

    def add(self, other):
        other.parent = self
        self.objectives.append(other)
