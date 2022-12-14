from job import Job 

class Solution:
    last_ID = -1

    def __init__(self, jobs: int, machines: int) -> None:
        Solution.last_ID += 1
        self.id = Solution.last_ID
        self.num_jobs = jobs
        self.num_machines = machines
        self.jobs = []
        self.makespan = 0.0

    def calculate_makespan(self):
        
        times = [[0 for _ in range(self.num_machines)] for _ in range(self.num_jobs) ]
        
        for machine_idx in range(self.num_machines):
            for job_idx in range(self.num_jobs):
                job:Job = self.jobs[job_idx]
                is_first_machine = machine_idx == 0
                is_first_job = job_idx == 0

                if is_first_machine and is_first_job:
                     times[job_idx][machine_idx] = job.processing_times[machine_idx]
                elif is_first_machine:
                    times[job_idx][machine_idx] = times[job_idx-1][machine_idx] + job.processing_times[machine_idx]
                elif is_first_job:
                    times[job_idx][machine_idx] = times[job_idx][machine_idx-1] + job.processing_times[machine_idx]
                else:
                    max_time = max( times[job_idx-1][machine_idx], times[job_idx][machine_idx-1])
                    times[job_idx][machine_idx] = max_time + job.processing_times[machine_idx]
        return times[self.num_jobs-1][self.num_machines-1]

    def add_job(self, job:Job):
        self.jobs.append(job)
    
    def shift_jobs(self, from_position, to_position):
        current_job = self.jobs[from_position]
        for i in range(from_position, to_position, -1):
            self.jobs[i] = self.jobs[i-1]
        self.jobs[to_position] = current_job

    def __str__(self) -> str:
        permutation = "("
        job: Job
        for job in self.jobs:
            permutation += str(job.id) + " "
        permutation = permutation.strip()
        permutation += ")"
        return permutation
