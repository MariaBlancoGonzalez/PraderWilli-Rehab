## TFG: Juego por visión por computador para niños con síndrome de Prader-Willi

Este repositorio contiene el código fuente y los recursos relacionados con mi Trabajo de Fin de Grado (TFG), titulado "Sistema de soporte a la rehabilitación física de niños afectados por el síndrome de Prader-Willi". El objetivo de este proyecto es desarrollar un juego interactivo utilizando Python y la biblioteca Pygame, junto con OpenCV (cv2) y MediaPipe, para brindar una experiencia de juego adaptada a niños que padecen el síndrome de Prader-Willi.

### Descripción del proyecto

El síndrome de Prader-Willi es un trastorno genético poco común que afecta a niños desde el nacimiento. El juego desarrollado en este proyecto tiene como objetivo proporcionar una herramienta interactiva para ayudar a estos niños a aprender y practicar habilidades de control y atención.

El juego se basa en la visión por computador y utiliza la cámara web del dispositivo para capturar el movimiento del jugador. Mediante el uso de MediaPipe, se realiza un seguimiento de las manos y otros puntos de interés en tiempo real para detectar los gestos y movimientos del niño. Esto permite que el juego se adapte a las habilidades y capacidades del niño, brindando una experiencia de juego personalizada.

El proyecto también incluye elementos de gamificación para hacer que el juego sea más atractivo y motivador para los niños.

### Funcionalidades principales

   - Interacción basada en la detección de gestos y movimientos utilizando OpenCV y MediaPipe.
   - Seguimiento en tiempo real de las manos y otros puntos de interés del jugador.
   - Elementos gráficos atractivos y amigables para el público infantil.
   - Retroalimentación visual y auditiva para estimular y motivar al niño durante el juego.
   - Registro de puntuaciones y seguimiento del progreso del niño.
    
### Instrucciones de instalación

**1.- Clona el repositorio en tu máquina local**
```
git clone https://github.com/MariaBlancoGonzalez/PraderWilli.git
```
**2.- Instala las dependencias**
```
pip install -r requirements.txt
```

**3.- Ejecuta el juego**
```
make run
```
