from neh import read_instance_file, neh
from solution import Solution

def test_neh():

    jobs, machines = read_instance_file("data/tai117_500_20_inputs.txt")
    solution:Solution
    solution, elapsed_time = neh(jobs, machines)
    assert solution.makespan == solution.calculate_makespan()
