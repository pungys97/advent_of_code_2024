from itertools import zip_longest
import random
from numpy.linalg import norm
from tqdm import tqdm

program = [2,4,1,5,7,5,0,3,1,6,4,3,5,5,3,0]

instruction_pointer = 0

A = 0
B = 0
C = 0

out = []

def interpret_operand(operand):
    if operand <= 3:
        return operand
    elif operand == 4:
        return A
    elif operand == 5:
        return B
    elif operand == 6:
        return C
    raise Exception("Invalid operand")

def op_adv(op):
    global A
    A = int(A / (2 ** interpret_operand(op)))

def op_bxl(op):
    # bitwise XOR between B and op
    global B
    B = B ^ op

def op_bxc(op):
    global B
    B = B ^ C

def op_bdv(op):
    global B
    B = int(A / (2 ** interpret_operand(op)))

def op_cdv(op):
    global C
    C = int(A / (2 ** interpret_operand(op)))

def op_bst(op):
    global B
    B = interpret_operand(op) % 8

def op_jnz(op):
    global instruction_pointer
    if A == 0:
        return
    instruction_pointer = op

def op_out(op):
    global out
    out.append(interpret_operand(op) % 8)

operations = [
    op_adv,
    op_bxl,
    op_bst,
    op_jnz,
    op_bxc,
    op_out,
    op_bdv,
    op_cdv
]

def run_once(a):
    global instruction_pointer, out, A, B, C
    A = a
    B = C = 0
    instruction_pointer = 0
    out = []
    while True:
        if instruction_pointer >= len(program):
            break
        original_ip = instruction_pointer
        op = program[instruction_pointer]
        operations[op](program[instruction_pointer + 1])
        if original_ip != instruction_pointer:  # jump was executed already
            continue
        instruction_pointer += 2
        # if current output is not beginning of the program, break
        if program[:len(out)] != out:
            break
    return out


if __name__ == "__main__":
    for i in range(100_000_000):
        out = run_once(i)
        if len(out) > 3:
            print(i, out)

import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
from itertools import zip_longest
from tqdm import tqdm
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import multiprocessing


@dataclass
class GeneticConfig:
    population_size: int = 15_000
    generations: int = 1000
    mutation_rate: float = 0.15
    elite_size: int = 100  # Number of best individuals to preserve
    tournament_size: int = 5
    num_workers: int = multiprocessing.cpu_count()
    n_bits: int = 46
    lower_bound: int = 30_000_000_000_000
    upper_bound: int = 40_000_000_000_000


class GeneticOptimizer:
    def __init__(self, config: GeneticConfig):
        self.config = config
        self.best_fitness = float('inf')
        self.best_solution = None
        self.generation = 0
        self.population = self._initialize_population()

    def _initialize_population(self):
        """Initialize population with random numbers in the specified range."""
        return [random.randint(self.config.lower_bound, self.config.upper_bound)
                for _ in range(self.config.population_size)]


    def perturbate_number(self, number: int, prob: float = 0.1) -> int:
        """Mutate number by flipping bits with given probability."""
        new_number = number
        # Use numpy for faster random number generation
        mutations = np.random.random(self.config.n_bits) < prob
        for i, should_mutate in enumerate(mutations):
            if should_mutate:
                new_number ^= (1 << i)
        return new_number

    def crossover(self, a: int, b: int) -> Tuple[int, int]:
        """Perform two-point crossover between parents."""
        # Two-point crossover is often more effective than single-point
        point1 = random.randint(0, self.config.n_bits - 1)
        point2 = random.randint(point1 + 1, self.config.n_bits)

        mask1 = ((1 << point1) - 1)
        mask2 = ((1 << point2) - 1) ^ mask1
        mask3 = ((1 << self.config.n_bits) - 1) ^ mask2 ^ mask1

        new_a = (a & mask1) | (b & mask2) | (a & mask3)
        new_b = (b & mask1) | (a & mask2) | (b & mask3)

        return new_a, new_b

    def edit_distance(self, arr2):
        arr1 = program
        m, n = len(arr1), len(arr2)
        dp = np.zeros((m + 1, n + 1), dtype=int)

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dp[i][j] = j
                elif j == 0:
                    dp[i][j] = i
                elif arr1[i - 1] == arr2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[m][n]

    def cosine_similarity(self, array2):
        array1 = program

        # Calculate length penalty (1.0 if same length, decreases as difference increases)
        length_penalty = min(len(array1), len(array2)) / max(len(array1), len(array2))

        # Truncate to shorter length for cosine calculation
        min_len = min(len(array1), len(array2))
        array1, array2 = array1[:min_len], array2[:min_len]

        # Calculate cosine similarity and apply length penalty
        cosine_sim = np.dot(array1, array2) / (norm(array1) * norm(array2))
        return cosine_sim * length_penalty

    def pad_and_mse(self, array1):
        if array1 == program:
            return 0.0
        max_len = max(len(array1), len(program))
        arr1_padded = np.pad(array1, (0, max_len - len(array1)), 'constant')
        arr2_padded = np.pad(program, (0, max_len - len(program)), 'constant')
        return np.mean((arr1_padded - arr2_padded) ** 2)

    def _evaluate_individual(self, individual: int) -> float:
        """Evaluate fitness of a single individual."""
        try:
            out_ = run_once(individual)  # Assuming run_once is defined elsewhere
            return self.edit_distance(out_) + self.pad_and_mse(out_)
        except Exception as e:
            print(f"Error evaluating individual: {e}")
            return 0.0

    def tournament_select(self, fitness_values: List[float]) -> int:
        """Select parent using tournament selection."""
        tournament = random.sample(range(len(self.population)), self.config.tournament_size)
        return min(tournament, key=lambda i: fitness_values[i])


    def evaluate_population(self) -> List[float]:
        """Evaluate entire population in parallel."""
        with ProcessPoolExecutor(max_workers=self.config.num_workers) as executor:
            fitness_values = list(executor.map(self._evaluate_individual, self.population))

        # Update best solution
        best_fitness = min(fitness_values)
        print(f"Best fitness: {best_fitness}")
        if best_fitness < self.best_fitness:
            self.best_fitness = best_fitness
            self.best_solution = self.population[fitness_values.index(best_fitness)]
            print(f"New best fitness: {self.best_fitness}")
            print(f"Best solution: {self.best_solution}")
            if best_fitness == 0:
                print(f"Found optimal solution: {self.best_solution}")

        return fitness_values

    def evolve(self) -> Optional[int]:
        """Run the genetic algorithm."""
        pbar = tqdm(range(self.config.generations))
        for generation in pbar:
            self.generation = generation

            # Evaluate population
            fitness_values = self.evaluate_population()

            # Early stopping if solution found
            if self.best_fitness == 0:
                print(f"Solution found in generation {generation}")
                return self.best_solution

            # Update progress bar
            pbar.set_description(f"Gen {generation}, Best: {self.best_fitness:.4f}")

            # Create new population
            new_population = []

            # Elitism: preserve best individuals
            sorted_indices = sorted(range(len(fitness_values)), key=lambda i: fitness_values[i])
            new_population.extend(self.population[i] for i in sorted_indices[:self.config.elite_size])

            # Fill rest of population with offspring
            while len(new_population) < self.config.population_size:
                parent1_idx = self.tournament_select(fitness_values)
                parent2_idx = self.tournament_select(fitness_values)

                offspring1, offspring2 = self.crossover(
                    self.population[parent1_idx],
                    self.population[parent2_idx]
                )

                # Mutate offspring
                if random.random() < self.config.mutation_rate:
                    offspring1 = self.perturbate_number(offspring1)
                if random.random() < self.config.mutation_rate:
                    offspring2 = self.perturbate_number(offspring2)

                new_population.append(offspring1)
                if len(new_population) < self.config.population_size:
                    new_population.append(offspring2)

            self.population = new_population

        return self.best_solution

