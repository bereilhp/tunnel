import cv2
import math

# Constantes a la hora de medir y calcular usando el ordenador
reference_object_width = 80  # mm
focal_length = 45  # mm
sensor_width = 45  # mm

# Crear variable image y vamos a cargar la imagen 'tren.png' usando la función cv2.imread
image = cv2.imread('tren.png')

# Creamos una ventana con nombre 'Tunnel'
cv2.namedWindow('Tunnel')

# Mostramos la imagen tren.png dentro de la ventana
cv2.imshow('Tunnel', image)

# Array de puntos
points = []

# Sacar las coordenadas de los dos puntos y luego calcular la distancia euclidiana y al mismo tiempo transformar pixeles a distancia real
def calculate_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    distance_in_meters = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) * 1000 / (reference_object_width * sensor_width) # En metros 
    return round(distance_in_meters, 3)

# Función que imprime en la imagen la distancia y dependiento del rango la pone de un color o otro 
def draw_distance(image, point1, point2, distance):
    cv2.line(image, point1, point2, (0, 0, 0), 2)
    cv2.putText(image, str(distance) + " m", (point1[0] + 10, point1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 0), 2)

    if distance > 20:
        color = (0, 255, 0)  # Verde
    elif distance > 10:
        color = (0, 150, 150)  # Amarillo
    else:
        color = (0, 0, 255)  # Rojo

    cv2.putText(image, str(distance) + " m", (point1[0] + 10, point1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

# Cuando hacemos click pintar un circulo y ver que son 2 puntos para crear una distancia entre A y B, también guardar imagen 
def select_point(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONUP:
        points.append((x, y))
        cv2.circle(image, (x, y), 5, (0, 0, 0), -1)
        cv2.imshow('Tunnel', image)
        if len(points) % 2 == 0 and len(points) >= 2:
            point1 = points[-2]
            point2 = points[-1]
            distance = calculate_distance(point1, point2)
            draw_distance(image, point1, point2, distance)
            cv2.imwrite('resultado.png', image) # Guardar Imagen

# Registrar los puntos seleccionados en la ventana (Tunnel)
cv2.setMouseCallback('Tunnel', select_point)

while True:
    # Esperar a que se aprete una tecla
    key = cv2.waitKey(1)

    # Si le damos a la tecla de ESC el programa se cierra
    if key == 27:
        break

# Destruir todas las ventanas
cv2.destroyAllWindows()
