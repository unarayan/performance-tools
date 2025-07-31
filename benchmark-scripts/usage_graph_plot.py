import csv
import json
import matplotlib.pyplot as plt
import os
import subprocess
import argparse
import glob

MAX_POINTS = 180

def downsample(x, y, max_points=MAX_POINTS):
    step = max(1, len(x) // max_points)
    return x[::step], y[::step]

def plot_cpu_usage(ax, filepath):
    cpu_usage = []
    time_seconds = []

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 8 and parts[1] == 'all':
                try:
                    idle = float(parts[7])
                    usage = 100 - idle
                    cpu_usage.append(usage)
                    time_seconds.append(len(cpu_usage) - 1)
                except ValueError:
                    continue

    if cpu_usage:
        time_ds, usage_ds = downsample(time_seconds, cpu_usage)
        ax.plot(time_ds, usage_ds, marker='o', color='blue', label='CPU Usage %')
        ax.set_title('CPU Usage Over Time')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Usage (%)')
        y_max = max(usage_ds or [0]) * 1.1
        ax.set_ylim(bottom=0, top=y_max)
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No CPU data", ha='center', va='center')
        ax.axis('off')

def plot_npu_usage(ax, filepath):
    usage_values = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                usage = float(row['percent_usage'])
                usage_values.append(usage)
            except ValueError:
                continue

    time_intervals = list(range(len(usage_values)))
    if usage_values:
        time_ds, usage_ds = downsample(time_intervals, usage_values)
        ax.plot(time_ds, usage_ds, color='darkorange', marker='o', linestyle='-', linewidth=2, label='NPU Usage (%)')
        ax.set_title('NPU Usage Over Time')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Usage (%)')
        y_max = max(usage_ds or [0]) * 1.1 
        ax.set_ylim(bottom=0, top=y_max)
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No NPU data", ha='center', va='center')
        ax.axis('off')

def plot_memory_usage(ax, filepath):
    used_mem = []
    time = 0
    with open(filepath, 'r') as file:
        for line in file:
            if line.startswith('Mem:'):
                parts = line.split()
                if len(parts) >= 3:
                    try:
                        used = int(parts[2]) / (1024 * 1024)  # Convert to GB
                        used_mem.append(used)
                    except ValueError:
                        continue
    if used_mem:
        time_series = list(range(len(used_mem)))
        time_ds, mem_ds = downsample(time_series, used_mem)
        ax.plot(time_ds, mem_ds, marker='o', color='green', label='Memory Used (GB)')
        ax.set_title('Memory Usage Over Time')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Memory Used (GB)')
        y_max = max(mem_ds or [0]) * 1.1  # or mem_ds / val list etc.
        ax.set_ylim(bottom=0, top=y_max)
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No Memory data", ha='center', va='center')
        ax.axis('off')

def plot_gpu_metrics(ax, filepath):
    desc_map = {
        'CCS %': 'Compute[CCS]',
        'RCS %': 'Render/3D[RCS]',
        'VCS %': 'Video[VCS]',
        'VECS %': 'VideoEnhance[VECS]',
        'Power W pkg': 'Power (W)',
        'RC6 %': 'Idle (RC6 %)'
    }

    metric_series = {metric: [] for metric in desc_map}
    time_series = []

    if os.path.isfile(filepath) and os.path.getsize(filepath) > 0:
        with open(filepath, 'r') as f:
            data = json.load(f)

        for i, entry in enumerate(data):
            time_series.append(i)
            for metric in desc_map:
                try:
                    val = float(str(entry.get(metric, '0')).replace('%', '').strip())
                except ValueError:
                    val = 0.0
                metric_series[metric].append(val)

        step = max(1, len(time_series) // MAX_POINTS)
        time_series_ds = time_series[::step]

        styles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1)), (0, (5, 10))]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c','#d62728', '#9467bd', '#8c564b']
        markers = ['o', 's', '^', 'x', 'D', '*']

        for idx, (metric, values) in enumerate(metric_series.items()):
            values_ds = values[::step]
            ax.plot(
                time_series_ds, values_ds,
                label=desc_map[metric],
                linestyle=styles[idx % len(styles)],
                color=colors[idx % len(colors)],
                marker=markers[idx % len(markers)],
                markersize=3,
                linewidth=1.5
            )

        basename = os.path.basename(filepath)
        device_part = basename.split('-')[-1].split('.')[0] if '-' in basename else "unknown"
        ax.set_title(f'GPU Usage Over Time (device={device_part})')
        ax.set_xlabel('Time (seconds)')
        ax.set_ylabel('Usage (%)')
        y_max = max([max(metric_series[m][::step] or [0]) for m in desc_map])
        ax.set_ylim(bottom=0, top=y_max + 2)
        ax.grid(True)
        ax.legend()
    else:
        ax.text(0.5, 0.5, "No GPU data", ha='center', va='center')
        ax.axis('off')

def main():
    parser = argparse.ArgumentParser(description="Generate single consolidated plot for CPU, NPU, GPU, and Memory usage.")
    parser.add_argument('--dir', type=str, default='.', help='Root directory containing logs')
    args = parser.parse_args()

    root = os.path.abspath(args.dir)
    cpu_log = os.path.join(root, 'cpu_usage.log')
    npu_csv = os.path.join(root, 'npu_usage.csv')
    mem_log = os.path.join(root, 'memory_usage.log')
    gpu_files = sorted(glob.glob(os.path.join(root, 'igt*.json')))

    total_plots = 3  # CPU + NPU + Memory
    if gpu_files:
        total_plots += len(gpu_files)

    fig, axs = plt.subplots(total_plots, 1, figsize=(20, total_plots * 4))  # Wide + Tall

    print("📊 Generating single consolidated graph...")
    plot_cpu_usage(axs[0], cpu_log)
    plot_npu_usage(axs[1], npu_csv)
    plot_memory_usage(axs[2], mem_log)

    if gpu_files:
        for idx, gpu_file in enumerate(gpu_files):
            plot_gpu_metrics(axs[3 + idx], gpu_file)
    else:
        print("⚠️ No GPU metric files found (igt*.json). Skipping GPU plots.")

    plt.tight_layout()
    output_image = os.path.join(root, 'plot_metrics.png')
    plt.savefig(output_image, dpi=300)
    plt.close()

    try:
        subprocess.run(["xdg-open", output_image])
    except:
        pass

    print(f"✅ Saved: {output_image}")

if __name__ == '__main__':
    main()
