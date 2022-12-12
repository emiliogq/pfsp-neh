from job import Job
from solution import Solution
import time
from operator import attrgetter
import logging

def read_instance_file(filename: str):
    with open(filename) as file:
        lines = file.readlines()
        num_machines = int(lines[1].split(" ")[1])
        job_times_line = lines[3:]
        i = 0
        jobs = []
        for job_times in job_times_line:
            job_processing_times = [ float(time) for time in job_times.split("\t")]
            job = Job(i, job_processing_times)
            jobs.append(job)
            i += 1
    return jobs, num_machines

def init_matrix(row_size, column_size):
    return [ [ 0 for j in range(column_size)] for i in range(row_size)]

def calculate_e_matrix(solution:Solution, current_job_position:int, machines: int):

    e = init_matrix(current_job_position, machines)
    
    for job_idx in range(current_job_position):
        job : Job = solution.jobs[job_idx]
        is_first_job = job_idx == 0
        for machine_idx in range(machines):
            is_first_machine = machine_idx == 0
            if is_first_job and is_first_machine:
                extra_time = 0
            elif is_first_machine:
                extra_time = e[job_idx-1][machine_idx]
            elif is_first_job:
                extra_time = e[job_idx][machine_idx-1]
            else:
                extra_time = max(e[job_idx-1][machine_idx], e[job_idx][machine_idx-1])
            e[job_idx][machine_idx] = extra_time + job.processing_times[machine_idx]
    return e

def calculate_q_matrix(solution:Solution, current_job_position:int , machines: int):
    q = init_matrix(current_job_position+1, machines)
    for job_idx in range(current_job_position, -1, -1):
        job: Job = solution.jobs[job_idx]
        is_current_job = job_idx == current_job_position
        is_previous_job = job_idx == current_job_position - 1
        for machine_idx in range(machines-1, -1, -1):
            is_last_machine = machine_idx == machines - 1
            processing_time = 0 if is_current_job else job.processing_times[machine_idx]
            if is_current_job:
                extra_time = 0
            elif is_previous_job and is_last_machine:
                extra_time = 0    
            elif is_last_machine:
                extra_time = q[job_idx+1][machine_idx]            
            elif is_previous_job:
                extra_time = q[job_idx][machine_idx+1]
            else:
                extra_time = max(q[job_idx + 1][machine_idx], q[job_idx][machine_idx + 1])
            q[job_idx][machine_idx] = extra_time + processing_time
    return q

def calculate_f_matrix(solution:Solution, current_job_position:int, e_matrix, machines: int):
    next_job_position = current_job_position + 1
    current_job: Job = solution.jobs[current_job_position]
    f = init_matrix(next_job_position, machines)
    for job_idx in range(next_job_position):
        is_first_job = job_idx == 0
        for machine_idx in range(machines):
            is_first_machine = machine_idx == 0   
            if is_first_job and is_first_machine:
                extra_time = 0
            elif is_first_machine:
                extra_time = e_matrix[job_idx-1][machine_idx]
            elif is_first_job:
                extra_time = f[job_idx][machine_idx-1]
            else:
                extra_time = max(e_matrix[job_idx-1][machine_idx], f[job_idx][machine_idx-1])
            f[job_idx][machine_idx] = extra_time + current_job.processing_times[machine_idx]
    return f

def compute_best_position(current_job_position: int, machines: int, q_matrix, f_matrix):
    best_position = current_job_position
    minimal_makespan = float('inf')
    for job_idx in range(current_job_position, -1, -1):
        max_sum = 0.0
        for machine_idx in range(machines):
            sum = f_matrix[job_idx][machine_idx] + q_matrix[job_idx][machine_idx]
            max_sum = sum if sum > max_sum else max_sum
        makespan = max_sum
        if makespan <= minimal_makespan:
            minimal_makespan = makespan
            best_position = job_idx
    return best_position, minimal_makespan

"""
Compute the best position for a job and returns the makespan. It uses Taillard's accelerations
"""
def shift_job_to_left(solution : Solution, current_job_position : int):
    is_last_job = current_job_position == solution.num_jobs - 1
    e_matrix = calculate_e_matrix(solution, current_job_position, solution.num_machines)
    q_matrix = calculate_q_matrix(solution, current_job_position, solution.num_machines)
    f_matrix = calculate_f_matrix(solution, current_job_position, e_matrix, solution.num_machines)
    best_job_position, minimal_makespan = compute_best_position(current_job_position, solution.num_machines, q_matrix, f_matrix)
    if (best_job_position < current_job_position):
        solution.shift_jobs(current_job_position, best_job_position)
    if is_last_job:
        solution.makespan = minimal_makespan
    return solution

def neh(jobs, machines: int):
    start_time = time.time()
    jobs.sort(key = attrgetter("total_processing_time"), reverse = True)
    solution = Solution(len(jobs), machines)
    i = 0
    for job in jobs:
        solution.add_job(job)
        shift_job_to_left(solution, i)
        i += 1
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    logging.info(f"NEH Makespan with Taillard acceleration = {solution.makespan:2f}")
    logging.info(f"Elapsed time = {elapsed_time:2f} sec")
    
    return solution, elapsed_time 