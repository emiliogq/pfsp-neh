class Job:
    def __init__(self, id, processing_times : list) -> None:
        self.id = id
        self.processing_times = processing_times
        self.total_processing_time = sum(self.processing_times)
