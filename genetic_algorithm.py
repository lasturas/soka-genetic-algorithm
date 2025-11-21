import random
import time
import math

# -------------------------------------------------------
#           PARAMETER KONFIGURASI GA
# -------------------------------------------------------
POPULATION_SIZE = 150
MAX_GENERATIONS = 300
MUTATION_RATE = 0.10
CROSSOVER_RATE = 0.8
TOURNAMENT_SIZE = 3
ELITISM_COUNT = 2


# =======================================================
#                     CHROMOSOME
# =======================================================
class Chromosome:
    def __init__(self, gene):
        self.gene = gene            # daftar VM index per task
        self.fitness = float('inf') # makin kecil makin bagus


# =======================================================
#                    MAIN GA
# =======================================================
def schedule(tasks, vms, iterations=1):
    num_tasks = len(tasks)
    num_vms = len(vms)

    print("Memulai Algoritma Genetika...")
    start_time = time.time()

    # 1) POPULASI AWAL
    population = initialize_population(num_tasks, num_vms)

    best_overall = None
    best_fitness = float('inf')

    # ---------------------------------------------------
    #                 LOOP EVOLUSI
    # ---------------------------------------------------
    for gen in range(MAX_GENERATIONS):

        # Evaluasi setiap anggota
        evaluate_population(population, tasks, vms)

        # Ambil terbaik generasi ini
        current_best = min(population, key=lambda c: c.fitness)

        if current_best.fitness < best_fitness:
            best_fitness = current_best.fitness
            best_overall = current_best

        if gen % 20 == 0:
            print(f"Gen-{gen} | Best Fitness : {best_fitness:.6f}")

        # ---------------------------------------------------
        #             SELEKSI GENERASI BARU
        # ---------------------------------------------------
        population.sort(key=lambda c: c.fitness)
        new_population = population[:ELITISM_COUNT]   # elitism

        while len(new_population) < POPULATION_SIZE:

            # Tournament selection
            p1 = tournament_selection(population)
            p2 = tournament_selection(population)

            # Crossover
            if random.random() < CROSSOVER_RATE:
                c1, c2 = load_aware_crossover(p1.gene, p2.gene, tasks)
            else:
                c1, c2 = p1.gene, p2.gene

            # Mutasi
            new_population.append(Chromosome(mutate(c1, num_vms)))
            if len(new_population) < POPULATION_SIZE:
                new_population.append(Chromosome(mutate(c2, num_vms)))

        population = new_population

    # ---------------------------------------------------
    #               GA SELESAI
    # ---------------------------------------------------
    end_time = time.time()
    print(f"GA selesai dalam {end_time - start_time:.4f} detik.")

    # Konversi hasil penjadwalan ke dictionary
    final_result = {}
    for i, task in enumerate(tasks):
        vm_choice = best_overall.gene[i]
        final_result[task.id] = vms[vm_choice].name

    return final_result



# =======================================================
#                 POPULASI AWAL
# =======================================================
def initialize_population(num_tasks, num_vms):
    population = []

    # 1) Round-robin solution → agar mulai dari posisi cukup seimbang
    rr = [(i % num_vms) for i in range(num_tasks)]
    population.append(Chromosome(rr))

    # 2) Sisanya random
    for _ in range(POPULATION_SIZE - 1):
        gene = [random.randint(0, num_vms - 1) for _ in range(num_tasks)]
        population.append(Chromosome(gene))

    return population



# =======================================================
#                EVALUASI POPULASI
# =======================================================
def evaluate_population(population, tasks, vms):
    for chrom in population:
        chrom.fitness = evaluate_solution(chrom.gene, tasks, vms)



# =======================================================
#         FITNESS FUNCTION (versi stabil)
# =======================================================
def evaluate_solution(gene, tasks, vms):
    vm_loads = [0.0] * len(vms)

    # Tambahkan beban tiap tugas ke VM tujuan
    for i, task in enumerate(tasks):
        vm_loads[gene[i]] += task.cpu_load

    # Execution time = total load / core VM
    exec_times = [
        vm_loads[i] / vms[i].cpu_cores for i in range(len(vms))
    ]

    makespan = max(exec_times)

    # IMBALANCE = standard deviation
    mean_exec = sum(exec_times) / len(exec_times)
    variance = sum((t - mean_exec) ** 2 for t in exec_times) / len(exec_times)
    imbalance = math.sqrt(variance)

    # ---------------------------------------------------
    #    NORMALISASI otomatis berdasar dataset
    # ---------------------------------------------------
    total_load = sum(task.cpu_load for task in tasks)

    norm_makespan = makespan / 250.0
    norm_imbalance = imbalance / 2.0

    # ---------------------------------------------------
    #          MULTI-OBJECTIVE BALANCING
    # ---------------------------------------------------
    W_MAKE = 0.30
    W_IMBA = 0.70

    fitness = W_MAKE * norm_makespan + W_IMBA * norm_imbalance
    return fitness



# =======================================================
#               TOURNAMENT SELECTION
# =======================================================
def tournament_selection(population):
    contestants = random.sample(population, TOURNAMENT_SIZE)
    return min(contestants, key=lambda c: c.fitness)



# =======================================================
#           LOAD-AWARE CROSSOVER
# =======================================================
def load_aware_crossover(p1, p2, tasks):
    size = len(p1)
    if size <= 1:
        return p1, p2

    # Cari 20% tugas paling berat → jangan tukar
    sorted_tasks = sorted(
        enumerate(tasks),
        key=lambda x: x[1].cpu_load,
        reverse=True
    )
    heavy_count = max(1, size // 5)
    heavy_indices = [idx for idx, _ in sorted_tasks[:heavy_count]]

    c1 = p1[:]
    c2 = p2[:]

    for i in range(size):
        if i in heavy_indices:
            continue
        if random.random() < 0.5:
            c1[i], c2[i] = c2[i], c1[i]

    return c1, c2



# =======================================================
#                     MUTATION
# =======================================================
def mutate(gene, num_vms):
    g = gene[:]
    for i in range(len(g)):
        if random.random() < MUTATION_RATE:
            g[i] = random.randint(0, num_vms - 1)
    return g
