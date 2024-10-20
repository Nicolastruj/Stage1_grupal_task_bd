from queryEngine import query_engine, query_engine_dict
import pytest


def test_query_engine(benchmark):
    benchmark.extra_info['unit'] = 'ms'

    benchmark.pedantic(
        target=query_engine.query_engine,
        args=("wife",),
        iterations=100,
        rounds=10,
        warmup_rounds=5
    )


def test_query_engine_dict(benchmark):
    benchmark.extra_info['unit'] = 'ms'

    indexer_folder = "../Words_Datamart"
    metadata_datamart_folder = "../Books_Metadata"
    book_datamart_folder = "../Books_Datamart"

    benchmark.pedantic(
        target=query_engine_dict.query_engine,
        args=("wife", indexer_folder, metadata_datamart_folder, book_datamart_folder),
        iterations=100,
        rounds=10,
        warmup_rounds=5
    )

# to execute => pytest benchmark.py --benchmark-group-by=func
# to save results => pytest benchmark.py --benchmark-save indexer_benchmarks
# to execute memory usage => in query engine module, I added @profile, then execute in there, first uncomment the profile and function call at the enc:
# python -m memory_profiler query_engine.py
# all of these test, from inside the package
