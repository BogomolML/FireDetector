ROWS, COLS = 6, 6

def check_point(coord: tuple, img_h: int, img_w: int) -> int:
    if coord is None:
        return 0
    cell_w = img_w // COLS
    cell_h = img_h // ROWS

    col_index = coord[0] // cell_w
    row_index = coord[1] // cell_h

    cell_number = row_index * COLS + col_index + 1
    return cell_number

def get_grid_size() -> tuple:
    return ROWS, COLS
