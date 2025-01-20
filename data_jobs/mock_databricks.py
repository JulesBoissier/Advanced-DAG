import random
from datetime import datetime, timedelta

import numpy as np


class MockDatabricksJobs:
    @staticmethod
    def fetch_plane_events(
        years=5, points_per_year=4000, amplitude=1, frequency=1, noise_level=0.1
    ):
        total_points = years * points_per_year
        start_date = datetime.today()
        time_intervals = [
            start_date + timedelta(days=i * (365 / points_per_year))
            for i in range(total_points)
        ]

        sine_wave = amplitude * np.sin(
            2 * np.pi * frequency * np.linspace(0, years, total_points)
        )
        noise = np.random.normal(0, noise_level, total_points)

        data = {time_intervals[i]: sine_wave[i] + noise[i] for i in range(total_points)}

        relevant_events = random.sample(time_intervals, random.randint(1, 5))
        non_relevant_events = random.sample(time_intervals, random.randint(1, 5))

        return data, relevant_events, non_relevant_events

    @staticmethod
    def run_threshold_job():
        pass
