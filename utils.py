def generate_config(input_file: str) -> dict:
    """
    Parse a nonogram puzzle text file and convert it to a dictionary format.

    Args:
        input_file (str): Path to the input text file

    Returns:
        dict: Puzzle configuration in dictionary format
    """
    config = {"size": 0, "n_rows": 0, "n_cols": 0, "clues": {"rows": [], "cols": []}}

    current_section = None

    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("rows:"):
                current_section = "rows"
                continue
            elif line.startswith("cols:"):
                current_section = "cols"
                continue

            if current_section:
                # Convert space-separated numbers to list of integers
                clue = [int(x) for x in line.split()]
                config["clues"][current_section].append(clue)

    # Set dimensions based on clues
    config["n_rows"] = len(config["clues"]["rows"])
    config["n_cols"] = len(config["clues"]["cols"])
    config["size"] = config["n_rows"] * config["n_cols"]

    return config
