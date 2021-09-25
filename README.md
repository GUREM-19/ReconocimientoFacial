# ReconocimientoFacial
Proyecto Software Ubicuo

Realizado con **python** usando la librería de **OpenCV**


- Detecta rostros en tiempo real
  -  Si esta registrado enmarca el rostro y despliega el nombre
  -  Si no esta registrado se despliega el marco con la etiqueta de desconocido 
- Se crea un registro de los rostros (.csv)
   - Fecha y hora de captura
   - Si el rostro se encuentra registrado en la base de datos se registra con su nombre
   - Si el rostro no se encuentra registrado se guarda como desconocido
 - Se registra fácilmente nuevos rostros
  - Solo se tiene que guardar la foto con el nombre de la persona en la carpeta de faces
