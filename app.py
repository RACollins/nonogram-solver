# --------------------------------------------------------------------------------------------------
# Nonogram solver app
# Author: Richard Collins
# --------------------------------------------------------------------------------------------------


###############
### Imports ###
###############


import streamlit as st
import numpy as np
from picross_solver import picross_solver
from PIL import Image, ImageDraw, ImageFont

###################
### Page Config ###
###################


st.set_page_config(
    page_title="Nonogram Solver",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="auto",
)


#################
### Constants ###
#################

#################
### Functions ###
#################


def main():
    st.title("Nonogram Solver")
    st.subheader("Solve nonograms by entering the rows and columns constraints")

    ### Side bar
    with st.sidebar:
        st.header("Information")
        st.markdown(
            """
            Nonograms are logic puzzles that can be solved by filling in cells in a grid.
            The constraints are given as a list of numbers, which represent the length of the
            filled segments in the row or column.
        """
        )

    ### Number of rows and columns
    row_input_col, col_input_col, unused_cols = st.columns([1, 1, 8])
    with row_input_col:
        n_rows = st.number_input(
            "Number of rows", min_value=1, max_value=25, value=5, step=1
        )
    with col_input_col:
        n_cols = st.number_input(
            "Number of columns", min_value=1, max_value=25, value=5, step=1
        )

    ### Row and column constraints
    row_constraints_col, col_constraints_col, unused_cols = st.columns([1, 1, 3])
    row_constraints_dict, col_constraints_dict = {}, {}
    with row_constraints_col:
        for r in range(n_rows):
            row_constraints_dict[r] = st.text_input(
                f"Row {r} constraints", value="", key=f"row_{r}_constraints"
            )
    with col_constraints_col:
        for c in range(n_cols):
            col_constraints_dict[c] = st.text_input(
                f"Column {c} constraints", value="", key=f"col_{c}_constraints"
            )

    ### Convert constraints to list of lists
    row_constraints = [
        [int(x) for x in row.split(",") if x.strip()] if row.strip() else []
        for row in row_constraints_dict.values()
    ]
    col_constraints = [
        [int(x) for x in col.split(",") if x.strip()] if col.strip() else []
        for col in col_constraints_dict.values()
    ]

    ### Initialise grid
    grid = np.full((n_rows, n_cols), -1, dtype=int)

    with st.form(key="nonogram_input"):
        show_numbers = st.toggle("Show grid numbers", value=False)
        solved_grid = picross_solver.solve(row_constraints, col_constraints, grid)
        solve_button = st.form_submit_button(label="Solve!")

    if solve_button:
        st.write(solved_grid)
        if solved_grid is not None:
            try:
                # Convert to binary and map to gray values
                binary_grid = np.where(grid > 0, 64, 192).astype(np.uint8)

                if binary_grid.ndim == 1:
                    binary_grid = binary_grid.reshape(-1, 1)

                # Create PIL Image
                img = Image.fromarray(binary_grid, mode="L")

                # Calculate scaling factor
                scale = min(500 // img.width, 500 // img.height)
                new_size = (img.width * scale, img.height * scale)

                # Resize image
                img_resized = img.resize(new_size, Image.Resampling.NEAREST)

                # If show_numbers is enabled, add numbers to the image
                if show_numbers:
                    draw = ImageDraw.Draw(img_resized)
                    # Try to create a font size that fits well within the cells
                    font_size = max(scale // 2, 10)  # Minimum size of 10
                    try:
                        font = ImageFont.truetype("Arial", font_size)
                    except:
                        font = ImageFont.load_default()

                    # Add numbers to each cell
                    for i in range(grid.shape[0]):
                        for j in range(grid.shape[1]):
                            # Calculate position for text
                            x = j * scale + scale // 4
                            y = i * scale + scale // 4
                            # Draw the number
                            value = str(int(grid[i, j] > 0))
                            draw.text((x, y), value, fill=128, font=font)

                # Display the image
                st.image(img_resized, caption="Solved Nonogram")
            except Exception as e:
                st.error(f"Error creating image: {str(e)}")

    return None


if __name__ == "__main__":
    main()
