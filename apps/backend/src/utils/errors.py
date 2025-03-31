class SearchLimitError(Exception):
    def __init__(self, input_range):
        super().__init__(f"Maxium range breached: Input max_distance {input_range}")
