from queryEngine import query_engine, query_engine_dict

def test_query_engine(benchmark):
    benchmark.extra_info['unit'] = 'ms'

    #comment the algorithm you don't want to analyse:
    benchmark(lambda: query_engine.query_engine("wife")) #lambda to encapsulate the result and receive the benchmark information
    #benchmark(lambda: query_engine_dict.query_engine("wife"))

#to execute=> pytest benchmark.py
#to execute memory usage => in query engine module, I added @profile, then execute in there, first uncomment the profile and function call at the enc:
# python -m memory_profiler query_engine.py
#all of these test, from inside the package