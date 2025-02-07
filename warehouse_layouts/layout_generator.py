import csv

def generate_layout(bays, lanes, path_width):

    row_number = 2 + bays * lanes + (bays - 1) * path_width
    col_number = 2 + bays * lanes + (bays - 1) * path_width

    row_kind = []
    row_kind.append(-5)
    for b in range(bays):
        for l in range(lanes):
            row_kind.append(1)
        if b != bays-1:
            for p in range(path_width):
                row_kind.append(-5)
    row_kind.append(-5)

    layout_list = []
    for r in row_kind:
        row_list = []
        if r == -5:
            for x in range(col_number):
                row_list.append(-5)
            layout_list.append(row_list)
        elif r == 1:
            row_list = row_kind
            layout_list.append(row_list)

    return layout_list


def add_sink(layout, path_width):
    new_layout = []
    # Add columns: 
    for i in range(len(layout)): 
        row = layout[i] + [-5 for i in range(path_width)]
        new_layout.append(row)

    # Add last rows: 
    for _ in range(path_width):
        new_layout.append([-5 for i in range(len(new_layout[0]))])

    # Add sink at bottom right corner: 
    new_layout[-1][-1] = 2

    # Add a further row and column to have paths to the sink from all directions
    for i in range(len(new_layout)):
        new_layout[i].append(-5)
    new_layout.append([-5 for i in range(len(new_layout[0]))])  

    return new_layout

def add_source(layout, path_width):
    new_layout = []
    # Add columns: 
    for i in range(len(layout)): 
        row = [-5 for i in range(path_width+1)] + layout[i]
        new_layout.append(row)
    
    # Add source at bottom right corner: 
    new_layout[-2][1] = 3

    return new_layout


def generate(bay_max, lane_max, path_width, name_addition):

    for b in range(1, bay_max+1):
        for l in range(3, lane_max+1):
            layout = generate_layout(b, l, path_width)
            if name_addition == '_sink':
                layout = add_sink(layout, path_width) 
            if name_addition == '_sink_source':
                layout = add_sink(layout, path_width) 
                layout = add_source(layout, path_width)

            csv_file = f"Size_{l}x{l}_Layout_{b}x{b}{name_addition}.csv"

            # Write the custom array to the CSV file
            with open(csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(layout)


def generate_wide():
    generate(10, 10, 2, '')

def generate_standard_layout():
    generate(10, 10, 3, '_wide')

def generate_sink():
    generate(10, 10, 2, '_sink')

def generate_sink_source():
    generate(10, 10, 2, '_sink_source')

if __name__ == '__main__':
    generate_standard_layout()
    generate_wide()
    generate_sink()
    generate_sink_source()
