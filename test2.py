import time
import random
from swizzle import swizzledtuple, LookupMode

fields = ['x', 'y', 'z']
arrange = ['x', 'y', 'z', 'z']
args = (1, 2, 3)

# Build swizzledtuple classes
VecDynamic = swizzledtuple('VecDynamic', fields, arrange_names=arrange, mode=LookupMode.DYNAMIC)
VecDiscovery = swizzledtuple('VecDiscovery', fields, arrange_names=arrange, mode=LookupMode.DISCOVERY)

# Create instances
vd = VecDynamic(*args)
vs = VecDiscovery(*args)

# Generate many random swizzle strings
components = 'xyz'
max_len = 4
num_swizzles = 100_000

swizzles = [
    ''.join(random.choices(components, k=random.randint(1, max_len)))
    for _ in range(num_swizzles)
]

print(f"Running {num_swizzles} random swizzle lookups for each mode...\n")

# Benchmark DYNAMIC
start_dyn = time.perf_counter()
for s in swizzles:
    try:
        _ = getattr(vd, s)
    except AttributeError:
        pass
end_dyn = time.perf_counter()
dyn_time = end_dyn - start_dyn

# Benchmark DISCOVERY
start_dis = time.perf_counter()
for s in swizzles:
    try:
        _ = getattr(vs, s)
    except AttributeError:
        pass
end_dis = time.perf_counter()
dis_time = end_dis - start_dis

# Print results
print("=== BENCHMARK RESULTS ===")
print(f"Dynamic mode   : {dyn_time:.4f} seconds")
print(f"Discovery mode : {dis_time:.4f} seconds")

if dis_time != 0:
    print(f"Speed ratio (dynamic/discovery): {dyn_time / dis_time:.2f}x")
else:
    print("Discovery mode ran too fast to measure reliably.")

