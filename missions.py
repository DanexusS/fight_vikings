class AbstractObjective:
    def __init__(self, description):
        self.description = description
        self.is_completed = False
        self.parent = None

    def complete(self):
        self.is_completed = True
        self.parent.obj_completed()

    def __repr__(self):
        return self.description


#   Примеры заданий
class KillObjective(AbstractObjective):
    def __init__(self, description, enemy_type, amount):
        super().__init__(description)

        self.enemy_type = enemy_type
        self.amount = amount

    def check(self, enemy_type):
        if self.enemy_type == enemy_type:
            self.complete()


class DiscoverObjective(AbstractObjective):
    def __init__(self, description, location_type):
        super().__init__(description)

        self.location_type = location_type


class MissionObject:
    def __init__(self, title, description, reward, objectives):
        self.objectives = objectives
        for obj in self.objectives:
            obj.parent = self

        self.title = title
        self.rewards = reward
        self.description = description
        self.is_completed = False
        self.current_objective = self.objectives[0]

    def obj_completed(self):
        next_obj_id = self.objectives.index(self.current_objective) + 1

        if next_obj_id < len(self.objectives):
            self.current_objective = self.objectives[next_obj_id]
        else:
            self.current_objective = None
            self.complete()

    def complete(self):
        pass

    def add(self, other):
        other.parent = self
        self.objectives.append(other)

    def __repr__(self):
        return self.title


class PlayerMissionLogic:
    def __init__(self, mission: MissionObject):
        self.mission = mission
