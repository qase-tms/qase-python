import json

from typing import Optional, List

from .basemodel import BaseModel


class RunExecution(BaseModel):
    def __init__(self,
                 start_time: float,
                 end_time: float,
                 cumulative_duration: int = 0,
                 ) -> None:
        self.start_time = start_time
        self.end_time = end_time
        self.duration = int((end_time - start_time) * 1000)
        self.cumulative_duration = cumulative_duration

    def track(self, result: dict):
        self.cumulative_duration += result["execution"]["duration"]


class RunStats(BaseModel):
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0
        self.skipped = 0
        self.broken = 0
        self.muted = 0
        self.total = 0

    def track(self, result: dict):
        status = result["execution"]["status"]
        if status == "passed":
            self.passed += 1
        elif status == "failed":
            self.failed += 1
        elif status == "skipped":
            self.skipped += 1
        elif status == "broken":
            self.broken += 1
        self.total += 1
        if result.get('muted', False):
            self.muted += 1


class Run(BaseModel):
    def __init__(self,
                 title: str,
                 start_time: float,
                 end_time: float,
                 results: List[str] = [],
                 threads: List[str] = [],
                 suites: List[str] = [],
                 environment: Optional[str] = None
                 ):
        self.host_data = None
        self.title = title
        self.execution = RunExecution(start_time=start_time, end_time=end_time)
        self.stats = RunStats()
        self.results = results
        self.threads = threads
        self.suites = suites
        self.environment = environment

    def add_result(self, result: dict):
        compact_result = {
            "id": result["id"],
            "title": result["title"],
            "status": result["execution"]["status"],
            "duration": result["execution"]["duration"],
            "thread": result["execution"]["thread"]
        }
        self.results.append(compact_result)
        self.execution.track(result)
        self.stats.track(result)
        if result["execution"]["thread"] not in self.threads:
            self.threads.append(result["execution"]["thread"])

    def add_host_data(self, host_data: dict):
        self.host_data = host_data
