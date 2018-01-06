import timeit

iterations = 500000
methods = [('uuid0.generate()', 'import uuid0'),
           ('uuid.uuid1()', 'import uuid'),
           ('uuid.uuid4()', 'import uuid')]
results = []
max_its = 0

print("Testing {} methods with {} iterations\n".format(len(methods), iterations))
for method, setup in methods:
    seconds = timeit.timeit(method, setup, number=iterations)
    it_s = iterations / seconds
    us_it = seconds * 1000000 / iterations
    results.append((method, it_s, us_it))

    if it_s > max_its:
        max_its = it_s

results.sort(key=lambda x: x[1], reverse=True)

col_fmt = "{:<20} {:<10} {:<10} {:<8}"
print(col_fmt.format("method", "it/s", "μs/it", "% slower"))
for res in results:
    print(col_fmt.format(res[0],
                         round(res[1]),
                         round(res[2], 3),
                         str(round((1 - res[1] / max_its) * 100, 2)) + '%'
                        ))
