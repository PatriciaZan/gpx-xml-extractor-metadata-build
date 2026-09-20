# from simplification.cutil import simplify_coords

# def simplify_route(
#     points,
#     tolerance=0.0001
# ):

#     coords = [
#         (
#             p["lon"],
#             p["lat"]
#         )
#         for p in points
#     ]

#     simplified = simplify_coords(
#         coords,
#         tolerance
#     )

#     return simplified.tolist()

def simplify_route(points, step=20):

    return [
        {
            "lat": p["lat"],
            "lon": p["lon"]
        }
        for p in points[::step]
    ]