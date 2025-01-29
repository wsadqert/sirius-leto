from basics import Point, Ray, Segment, Vector
import math

def calculate_ray_direction(ray: Ray) -> Vector:
	# Calculate the direction vector of the ray
	dx = ray.x2 - ray.x1
	dy = ray.y2 - ray.y1
	length = ray.length

	if length == 0:
		return Vector()  # The ray has no direction
	return Vector(dx / length, dy / length)

def _intersect_ray_segment(ray: Ray, ray_direction: Vector, segment: Segment) -> Point | None:
	# Ray represented as P + tD, where P is the start point, D is the direction, and t is a scalar
	# Segment represented as A + u(B - A), where A is the start point, B is the end point, and u is a scalar

	ray_start = ray.get_points()[0]

	# Ray start point
	P = ray_start.to_tuple()
	D = ray_direction.to_tuple()

	# Segment start and end points
	A = segment.get_points()[0].to_tuple()
	B = segment.get_points()[1].to_tuple()

	# Calculate the denominator
	denom = D[0] * (B[1] - A[1]) - D[1] * (B[0] - A[0])
	if abs(denom) < 1e-10:  # Parallel lines
		return None

	# Calculate the parameters t and u
	t = ((A[0] - P[0]) * (B[1] - A[1]) - (A[1] - P[1]) * (B[0] - A[0])) / denom
	u = ((A[0] - P[0]) * D[1] - (A[1] - P[1]) * D[0]) / denom

	# Check if the intersection point is on the ray and the segment
	if t >= 0 and 0 <= u <= 1:
		intersection_x = P[0] + t * D[0]
		intersection_y = P[1] + t * D[1]
		return Point(intersection_x, intersection_y)

	return None

def ray_segment_intersection(segment: Segment, ray: Ray) -> Point | None:
	ray_direction = calculate_ray_direction(ray)
	
	if not ray_direction:
		return None  # Invalid ray

	intersection = _intersect_ray_segment(ray, ray_direction, segment)
	
	return intersection
