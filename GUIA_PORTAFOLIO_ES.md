# Cómo entender y presentar este proyecto

1. Lee primero el problema y los datos en README.md.
2. Ejecuta la demo para entender las entradas y salidas.
3. Ejecuta las pruebas: `python -m unittest discover -v`.
4. Reproduce el experimento indicado abajo. Mira el resultado y compáralo con la referencia sencilla.
5. Explica qué datos se reservaron para prueba, qué decisiones se tomaron antes y en qué casos falla.

Ejecuta `python benchmark.py` para la demostración sintética. Para tus datos usa `python train_csv.py posts.csv --output trained-model.json`. Entrenar significa ajustar coeficientes con ejemplos anteriores; evaluar significa medir el error en publicaciones posteriores. MAE es el error absoluto promedio; 0,01 equivale a un punto porcentual de tasa de interacción. El archivo JSON conserva los coeficientes para inspeccionarlos.

Para una entrevista, prepara una explicación de dos minutos: problema → datos → método → comparación → resultado → límites. Identifica qué código te ayudó a generar IA y demuestra que entiendes cada decisión.
