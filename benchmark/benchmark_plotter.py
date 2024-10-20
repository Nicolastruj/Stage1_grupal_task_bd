import csv
import json

import matplotlib.pyplot as plt
import pandas as pd


def load_json_data(filepath):
    """Load data from a JSON file."""
    with open(filepath, 'r') as file:
        return json.load(file)


def write_csv_data(filepath, benchmarks):
    """Write benchmarks data to a CSV file."""
    fields_names = ['name', 'mean_time', 'rounds', 'iterations', 'warmup']

    with open(filepath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fields_names)
        writer.writeheader()
        for benchmark in benchmarks:
            writer.writerow(convert_benchmark_to_dict(benchmark))


def convert_benchmark_to_dict(benchmark):
    """Converts a JSON object to a dictionary."""
    return {
        'name': benchmark['name'],
        'mean_time': benchmark['stats']['mean'],
        'rounds': benchmark['stats']['rounds'],
        'iterations': benchmark['stats']['iterations'],
        'warmup': benchmark['options']['warmup']
    }


def load_data(filename):
    """Load data from a CSV file."""
    df = pd.read_csv(filename)
    return df


def process_numeric_data(df, colname):
    """Process the data to ensure the mean times are numeric."""
    df[colname] = pd.to_numeric(df[colname], errors='coerce')
    return df


def plot_benchmark_data(df):
    """Plot a bar chart comparing mean times for each benchmark."""
    mean_times = df.groupby('name')['mean_time'].mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(mean_times['name'], mean_times['mean_time'], color='skyblue')

    plt.title('Average Mean Time for Each Benchmark')
    plt.xlabel('Benchmark Name')
    plt.ylabel('Mean Time (ms)')
    plt.xticks(rotation=45)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


def main():
    json_filepath = '0001_indexer_benchmark.json'
    csv_filepath = '0001_indexer_benchmark.csv'

    data = load_json_data(json_filepath)
    benchmarks = data['benchmarks']

    write_csv_data(csv_filepath, benchmarks)

    df_benchmark = load_data(csv_filepath)
    df_benchmark = process_numeric_data(df_benchmark, "mean_time")
    plot_benchmark_data(df_benchmark)


if __name__ == "__main__":
    main()
