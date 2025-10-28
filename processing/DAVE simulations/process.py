import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Polygon
import numpy as np


def densify_polygon(geom, max_segment_length=50):
    """
    Add intermediate points to polygon edges to maintain shape during CRS transformation.

    Args:
        geom: Shapely polygon geometry
        max_segment_length: Maximum length (in meters) between vertices

    Returns:
        Densified polygon
    """
    if geom.geom_type != "Polygon":
        return geom

    def densify_line(coords, max_length):
        """Add points along a line segment if it exceeds max_length."""
        new_coords = []
        for i in range(len(coords) - 1):
            start = np.array(coords[i])
            end = np.array(coords[i + 1])
            new_coords.append(coords[i])

            # Calculate distance
            dist = np.linalg.norm(end - start)

            # Add intermediate points if needed
            if dist > max_length:
                num_points = int(np.ceil(dist / max_length))
                for j in range(1, num_points):
                    t = j / num_points
                    intermediate = start + t * (end - start)
                    new_coords.append(tuple(intermediate))

        new_coords.append(coords[-1])
        return new_coords

    # Densify exterior ring
    exterior_coords = list(geom.exterior.coords)
    densified_exterior = densify_line(exterior_coords, max_segment_length)

    # Densify interior rings (holes) if any
    densified_interiors = []
    for interior in geom.interiors:
        interior_coords = list(interior.coords)
        densified_interiors.append(densify_line(interior_coords, max_segment_length))

    return Polygon(densified_exterior, densified_interiors)


# Load the GeoPackage file
print("Loading GPKG file...")
gdf = gpd.read_file(
    "hourly_adult_population_Vaud_Geneva_DOY199.gpkg",
    layer="hourly_adult_population_Vaud_Geneva_DOY199",
)

print(f"Loaded {len(gdf)} features")
print(f"Original CRS: {gdf.crs}")

# Rename columns from "0", "1", ... "23" to "hour_0", "hour_1", ... "hour_23"
# This makes it clearer that these are hourly population values
hour_columns = [str(i) for i in range(24)]
rename_dict = {str(i): f"hour_{i}" for i in range(24)}
gdf = gdf.rename(columns=rename_dict)

print(f"Renamed hour columns: {list(rename_dict.values())}")

# Densify geometries before transformation to prevent distortion
print("Densifying polygon edges to preserve shape during transformation...")
gdf["geometry"] = gdf["geometry"].apply(densify_polygon)
print(f"Sample polygon now has {len(gdf.geometry.iloc[0].exterior.coords)} vertices")

# Transform from EPSG:2056 (Swiss LV95) to EPSG:4326 (WGS84)
print("Transforming to WGS84...")
gdf = gdf.to_crs("EPSG:4326")

print(f"Transformed CRS: {gdf.crs}")
print(f"Columns: {list(gdf.columns)}")

# Save to GeoJSON - all 24 hourly values will be preserved as properties
output_file = "hourly_adult_population_wgs84.geojson"
print(f"Saving to {output_file}...")
gdf.to_file(output_file, driver="GeoJSON")

print("Done!")
print(f"Output file: {output_file}")
print("Each feature contains 24 hourly population values (hour_0 through hour_23)")
