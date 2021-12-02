class AbstractObjective:
    def __init__(self, description):
        self.description = description
        self.is_completed = False
        self.parent = None

    def complete(self):
        self.is_completed = True
        self.parent.current_objective_id += 1
        if self.parent.current_objective_id > len(self.parent.objectives):
            self.parent.complete()

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
    def __init__(self, title, description, reward, objectives):
        self.objectives = objectives
        for obj in self.objectives:
            obj.parent = self

        self.title = title
        self.rewards = reward
        self.description = description
        self.is_completed = False
        self.current_objective_id = 0

    def complete(self):
        pass

    def current_objective(self):
        return self.objectives[self.current_objective_id]

    def add(self, other):
        other.parent = self
        self.objectives.append(other)

    def __repr__(self):
        return self.title


# тестовые возможности

test_mission = MissionObject("test", "idk", 100, [KillObjective("test obj", "guardian", 10),
                                                  KillObjective("test obj 2", "guardians", 110)])

print(test_mission.current_objective())

test_mission.current_objective().complete()

print(test_mission.current_objective())
