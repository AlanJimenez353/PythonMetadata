from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def get_exif_data(image):
    exif_data = {}
    if hasattr(image, '_getexif'):
        exif_info = image._getexif()
        if exif_info is not None:
            for tag, value in exif_info.items():
                decoded = TAGS.get(tag, tag)
                exif_data[decoded] = value
    return exif_data

def get_gps_info(exif_data):
    gps_info = {}
    if 'GPSInfo' in exif_data:
        for key in exif_data['GPSInfo'].keys():
            decode = GPSTAGS.get(key,key)
            gps_info[decode] = exif_data['GPSInfo'][key]

        # Convert GPS coordinates to degrees
        def convert_to_degrees(value):
            d = float(value[0])
            m = float(value[1])
            s = float(value[2])
            return d + (m / 60.0) + (s / 3600.0)
        
        # Get the latitude and longitude
        latitude = convert_to_degrees(gps_info['GPSLatitude'])
        if gps_info['GPSLatitudeRef'] != 'N':
            latitude = -latitude

        longitude = convert_to_degrees(gps_info['GPSLongitude'])
        if gps_info['GPSLongitudeRef'] != 'E':
            longitude = -longitude

        return latitude, longitude
    else:
        return None

def get_image_metadata(image_path):
    with Image.open(image_path) as img:
        metadata = {
            "format": img.format,
            "size": img.size,
            "mode": img.mode
        }

        exif_data = get_exif_data(img)
        metadata["exif"] = exif_data

        gps_info = get_gps_info(exif_data)
        if gps_info:
            metadata["GPS"] = {
                "latitude": gps_info[0],
                "longitude": gps_info[1]
            }
        
        return metadata

# Ruta a la imagen específica
image_path = "C:\\Users\\Alan\\Documents\\CodeProjects\\Metadata\\Resourses\\ImagesToAnalize\\Foto1.jfif"

# Obtener y mostrar la metadata
metadata = get_image_metadata(image_path)
print(f"Metadata de la imagen {image_path}:")
for key, value in metadata.items():
    print(f"  {key}: {value}")

if "GPS" in metadata:
    print("Ubicación GPS:")
    print(f"  Latitud: {metadata['GPS']['latitude']}")
    print(f"  Longitud: {metadata['GPS']['longitude']}")
else:
    print("No se encontró información GPS en los datos EXIF.")
