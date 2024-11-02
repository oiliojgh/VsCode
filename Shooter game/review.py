total-area= 0
def calculate_triangle_area(base, heigh):
    global total_area
    area = (base * heigh) / 2
    total_area += area
    return area

triangle1_area = calculate_triangle_area(10, 5)

triangle2_area = calculate_triangle_area(15, 8)

print("Total area of all triangles:", total_area)  # Output: Total area of all triangles: 60.000000000000014
    