from math import radians, sin, cos, sqrt, atan2

def haversine(coord1, coord2, unit='km'):
    """
    İki koordinat arasındaki mesafeyi Haversine formülü ile hesaplar.

    :param coord1: İlk koordinat (enlem, boylam)
    :param coord2: İkinci koordinat (enlem, boylam)
    :param unit: Mesafe birimi ('km', 'mi' veya 'm')
    :return: Hesaplanan mesafe
    """
    # Dünya yarıçapı (km)
    R = 6371.0

    # Koordinatları radyan cinsine çevir
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    # Haversine formülü
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Mesafeyi hesapla ve istenen birimde döndür
    if unit == 'km':
        return R * c
    elif unit == 'mi':
        return R * c * 0.621371
    elif unit == 'm':
        return R * c * 1000
    else:
        raise ValueError("Geçersiz birim. 'km', 'mi', veya 'm' kullanın.")

def calculate_distances(coordinates, unit='km'):
    """
    Verilen koordinat listesindeki mesafeleri ve toplam mesafeyi hesaplar.

    :param coordinates: Koordinat listesi [(enlem, boylam), ...]
    :param unit: Mesafe birimi ('km', 'mi' veya 'm')
    :return: Mesafe listesi ve toplam mesafe
    """
    # Verilen koordinat listesindeki mesafeleri hesapla
    distances = []

    for i in range(len(coordinates) - 1):
        distance = haversine(coordinates[i], coordinates[i + 1], unit)
        distances.append(distance)

    # Toplam mesafeyi hesapla
    total_distance = sum(distances)

    return distances, total_distance

# Kullanım örneği
