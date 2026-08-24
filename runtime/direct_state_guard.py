class DirectStateGuard:
    @staticmethod
    def attempt(obs, target):
        try:
            obs.transition(target, "direct manipulation", "UNTRUSTED")
        except ValueError:
            return False
        return True
