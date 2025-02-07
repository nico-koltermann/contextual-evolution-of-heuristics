import json
import os
import plotly.graph_objects as go
from datetime import datetime
import re
import itertools

def plot_evaluation_time(folder_path, local=True, save_file=True):
    data_folder_path = os.path.join(folder_path, "all_programs")
    data_save_path = os.path.join(folder_path, "visualization")

    if save_file:
        os.makedirs(data_save_path, exist_ok=True)

    created_at_values = []
    evaluation_times = []
    total_durations = []
    offspring_ids = []
    objectives = []
    populations = []
    exception_timestamps = []

    for filename in os.listdir(data_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(data_folder_path, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                    if local:
                        created_at_str = data.get("full_request", {}).get("created_at", "")
                    else:
                        created_at_str = data.get("full_request", {}).get("created", "")

                    evaluation_time_ns = data.get("offspring", {}).get("evaluation_time", None)
                    total_duration_ns = data.get("full_request", {}).get("total_duration", -1)
                    offspring_id = data.get("offspring", {}).get("offspring_id", "")
                    objective = data.get("offspring", {}).get("objective", None)
                    exception = data.get("exception", None)
                    population_match = re.search(r"pop_(\d+)", offspring_id)
                    population = population_match.group(1) if population_match else "Unknown"

                    if created_at_str and evaluation_time_ns is not None and total_duration_ns is not None:
                        if local:
                            created_at = datetime.fromisoformat(created_at_str[:26].replace("Z", "+00:00"))
                            total_duration_s = total_duration_ns / 1_000_000_000
                        else:
                            created_at  =  datetime.fromtimestamp(int(created_at_str))
                            total_duration_s = total_duration_ns

                        evaluation_time_s = evaluation_time_ns / 1_000_000_000

                        created_at_values.append(created_at)
                        evaluation_times.append(evaluation_time_s)
                        total_durations.append(total_duration_s)
                        offspring_ids.append(offspring_id)
                        objectives.append(objective)
                        populations.append(population)

                    elif exception and exception.strip():
                        exception_timestamps.append(created_at)

            except json.JSONDecodeError:
                print(f"Warning: '{filename}' is not a valid JSON file and will be skipped.")
            except ValueError as e:
                print(f"An error occurred while processing '{filename}': {e}")
            except Exception as e:
                print(f"An unexpected error occurred while processing '{filename}': {e}")

    if not created_at_values:
        print("No valid data found in JSON files.")
        return

    # Compute cumulative exception count
    cumulative_exceptions = []
    for timestamp in sorted(created_at_values):
        exception_count = sum(1 for t in exception_timestamps if t <= timestamp)
        cumulative_exceptions.append(exception_count)

    unique_populations = list(map(str, sorted(set(map(int, populations)))))
    symbols = ['circle', 'diamond', 'square', 'triangle-up', 'triangle-down', 'cross', 'x']
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink']
    symbol_color_combinations = list(itertools.product(symbols, colors))

    fig = go.Figure()
    population_boundaries = {}

    for i, population in enumerate(unique_populations):
        pop_indices = [j for j, p in enumerate(populations) if p == population]
        symbol, color = symbol_color_combinations[i % len(symbol_color_combinations)]

        fig.add_trace(go.Scatter(
            x=[created_at_values[j] for j in pop_indices],
            y=[evaluation_times[j] for j in pop_indices],
            mode="markers",
            marker=dict(
                size=10,
                color=[total_durations[j] for j in pop_indices],
                colorscale="Viridis",
                coloraxis="coloraxis",
                symbol=symbol,
                line=dict(color=color, width=1),
            ),
            name=f"Population {population}",
            text=[offspring_ids[j] for j in pop_indices],
            hovertemplate="<b>Offspring ID:</b> %{text}<br>" +
                          "<b>Created At:</b> %{x}<br>" +
                          "<b>Heuristics Evaluation Time (s):</b> %{y}<br>" +
                          "<b>Total Prompting Duration (s):</b> %{marker.color}<br>" +
                          "<b>Objective:</b> %{customdata[0]}<extra></extra>",
            customdata=[[objectives[j]] for j in pop_indices],
        ))

        population_boundaries[population] = max([created_at_values[j] for j in pop_indices])

    for population, boundary in population_boundaries.items():
        fig.add_shape(
            type="line",
            x0=boundary, y0=min(evaluation_times),
            x1=boundary, y1=max(evaluation_times),
            line=dict(color="black", width=2, dash="dash"),
            xref="x", yref="y"
        )

    # Add cumulative exceptions on a secondary y-axis
    fig.add_trace(go.Scatter(
        x=sorted(created_at_values),
        y=cumulative_exceptions,
        mode="lines",
        line=dict(color="red", width=2, dash="dot"),
        name="Cumulative Exceptions",
        hovertemplate="<b>Time:</b> %{x}<br><b>Cumulative Exceptions:</b> %{y}<extra></extra>",
        yaxis="y2"  # Use secondary y-axis
    ))

    # Update layout with secondary y-axis
    fig.update_layout(
        title="Heuristics Evaluation Time with Total Duration as Color and Cumulative Exceptions",
        xaxis_title="Created At",
        yaxis_title="Heuristics Evaluation Time (s)",
        xaxis=dict(tickformat="%Y-%m-%d %H:%M:%S"),
        yaxis=dict(exponentformat='E'),
        yaxis2=dict(
            title="Cumulative Exceptions",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            title="Populations",
            x=1.12,
            y=1.0,
            tracegroupgap=5
        ),
        coloraxis=dict(
            colorbar=dict(
                title="Total Duration (s)",
                x=1.02,
                len=0.75,
                yanchor="middle",
                y=0.63
            ),
            colorscale="Viridis"
        ),
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=1.0,
                y=1.08,
                showactive=True,
                buttons=[
                    dict(
                        label="Show All",
                        method="update",
                        args=[{"visible": [True] * len(unique_populations)}]
                    ),
                    dict(
                        label="Hide All",
                        method="update",
                        args=[{"visible": ["legendonly"] * len(unique_populations)}]
                    )
                ]
            )
        ]
    )


    if save_file:
        html_path = os.path.join(data_save_path, "evaluation_time_plot.html")

        fig.write_html(html_path)
        print(f"Plot saved as '{html_path}'")

    return fig

if __name__ == "__main__":

    folder_path = (r'/home/nico/LFO/eoh_results/results_20241216_074843_multibay_reshuffle_gpt4o_ueTrue')

    local = False
    if any(llm in folder_path for llm in ['gemma', 'llama', 'nemotron']):
        local = True

    plot_evaluation_time(folder_path, local)
