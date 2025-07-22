from .models import ObjectPose, NBVResponse, NBVPoint
import numpy as np
import open3d as o3d
import os

# --- On server startup: load & preprocess mesh ---
MESH_PATH = "sodaCan.glb"  # Place this file in your nbv_backend folder

if not os.path.exists(MESH_PATH):
    raise FileNotFoundError(f"{MESH_PATH} not found. Place sodaCan.glb in your backend folder.")

# Load and normalize mesh once
mesh = o3d.io.read_triangle_mesh(MESH_PATH)
mesh.compute_vertex_normals()
center = mesh.get_center()
mesh.translate(-center)
bbox = mesh.get_axis_aligned_bounding_box()
scale = 1.0 / max(bbox.get_extent())
mesh.scale(scale, center=(0, 0, 0))

# --- NBV candidate generator functions (from notebook) ---
def fibonacci_sphere(samples=8, radius=0.5):
    points = []
    phi = np.pi * (3. - np.sqrt(5.))
    for i in range(samples):
        y = 1 - (i / float(samples - 1)) * 2
        r = np.sqrt(1 - y * y)
        theta = phi * i
        x = np.cos(theta) * r
        z = np.sin(theta) * r
        points.append([x * radius, y * radius, z * radius])
    return np.array(points)

def generate_normal_based_views(mesh, num_views=8, distance=0.3):
    pcd = mesh.sample_points_uniformly(number_of_points=num_views)
    pcd.estimate_normals()
    points = np.asarray(pcd.points)
    normals = np.asarray(pcd.normals)
    candidate_views = points - normals * distance
    return candidate_views

def plan_next_best_view(object_pose: ObjectPose) -> NBVResponse:
    """
    Generate NBV candidates around the 'soda can', then transform by input object_pose (x, y, z).
    """
    # Generate both types of candidates (as in notebook)
    sphere_views = fibonacci_sphere(samples=8, radius=0.5)
    normal_views = generate_normal_based_views(mesh, num_views=8, distance=0.3)
    candidate_views = np.vstack([sphere_views, normal_views])

    # Offset all NBV candidates by object_pose
    offset = np.array([object_pose.x, object_pose.y, object_pose.z])
    candidate_views = candidate_views + offset

    # Azimuth & elevation can be computed relative to object center if you want to include them
    nbv_points = []
    for pt in candidate_views:
        rel = pt - offset
        r = np.linalg.norm(rel)
        azimuth = np.degrees(np.arctan2(rel[1], rel[0]))
        elevation = np.degrees(np.arcsin(rel[2] / r)) if r > 0 else 0
        nbv_points.append(NBVPoint(
            x=float(pt[0]),
            y=float(pt[1]),
            z=float(pt[2]),
            azimuth=float(azimuth),
            elevation=float(elevation),
        ))
    return NBVResponse(nbv_points=nbv_points)

