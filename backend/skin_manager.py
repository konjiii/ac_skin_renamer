

class SkinManager:
    """
    Handles backend logic
    """
    def __init__(self, ac_path):
        if not ac_path:
            raise ValueError("AC path must be provided")
        self.ac_path = ac_path