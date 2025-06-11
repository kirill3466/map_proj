import os
import geopandas as gpd
from db.core import get_session
from parcel.models import Parcel


def bulk_create_parcels(geojson_path: str):

    gdf = gpd.read_file(geojson_path)

    with get_session() as session:
        existing_parcels = session.query(Parcel).all()
        existing_codes = {
            parcel.cadastral_code: parcel for parcel in existing_parcels
        }

        parcels_to_add = []
        parcels_to_update = []

        for _, row in gdf.iterrows():
            centroid = row['geometry'].centroid
            longitude = centroid.x
            latitude = centroid.y

            cadastral_code = row.get('code')
            if not cadastral_code:
                continue
            new_parcel_data = {
                'cadastral_code': cadastral_code,
                'code_id': row.get('code_id'),
                'kvartal': row.get('kvartal'),
                'area_value': row.get('area_value'),
                'date_cost': row.get('date_cost'),
                'cad_cost': row.get('cad_cost'),
                'permitted_use': row.get('permitted_use'),
                'readable_address': row.get('readable_address'),
                'ownership_type': row.get('ownership_type'),
                'status': row.get('status'),
                'longitude': longitude,
                'latitude': latitude,
                'description': row.get('description'),
                'owner_id': row.get('owner_id')
            }

            if cadastral_code in existing_codes:
                existing_parcel = existing_codes[cadastral_code]
                for key, value in new_parcel_data.items():
                    if hasattr(existing_parcel, key) and value is not None:
                        setattr(existing_parcel, key, value)
                parcels_to_update.append(existing_parcel)
            else:
                new_parcel = Parcel(**new_parcel_data)
                parcels_to_add.append(new_parcel)

        if parcels_to_add:
            session.bulk_save_objects(parcels_to_add)

        if parcels_to_update:
            for parcel in parcels_to_update:
                session.merge(parcel)

        session.commit()


if __name__ == "__main__":
    path = os.path.dirname(
        os.path.abspath(__file__)
    ) + "/static/geodata/result1.geojson"
    bulk_create_parcels(path)
