all: lazy_primes split_join indexed_iteration moving_average pipeline_as_value

lazy_primes:
	 g++ -std=c++20 -O2 01_lazy_primes.cpp -o lazy_primes
	 ./lazy_primes

split_join:
	 g++ -std=c++23 -O2 02_split_join.cpp -o split_join
	 ./split_join

indexed_iteration:
	 g++ -std=c++23 -O2 03_indexed_iteration.cpp -o indexed_iteration
	 ./indexed_iteration


moving_average:
	g++ -std=c++23 -O2 04_moving_average.cpp -o moving_average
	./moving_average

pipeline_as_value:
	g++ -std=c++23 -O2 05_pipeline_as_value.cpp -o pipeline_as_value
	./pipeline_as_value

clean:
	rm -f lazy_primes split_join indexed_iteration moving_average pipeline_as_value *.exe