# Cómo entender y presentar este proyecto

1. Lee primero el problema y los datos en README.md.
2. Ejecuta la demo para entender las entradas y salidas.
3. Ejecuta las pruebas: `python -m unittest discover -v`.
4. Reproduce el experimento indicado abajo. Mira el resultado y compáralo con la referencia sencilla.
5. Explica qué datos se reservaron para prueba, qué decisiones se tomaron antes y en qué casos falla.

Ejecuta `python benchmark.py` para la demostración sintética. Para tus datos usa `python train_csv.py posts.csv --output trained-model.json`. Entrenar significa ajustar coeficientes con ejemplos anteriores; evaluar significa medir el error en publicaciones posteriores. MAE es el error absoluto promedio; 0,01 equivale a un punto porcentual de tasa de interacción. El archivo JSON conserva los coeficientes para inspeccionarlos.

Para una entrevista, prepara una explicación de dos minutos: problema → datos → método → comparación → resultado → límites. Identifica qué código te ayudó a generar IA y demuestra que entiendes cada decisión.


## Mejoras del 11 de octubre de 2026

Entrenamos con 39.644 artículos reales históricos. Reservamos días completos para entrenamiento, validación y prueba. La regresión ridge superó ligeramente la referencia: la reducción del error logarítmico fue 2,52%. No es un pronóstico validado para FOX. Ejecuta news_train.py y prueba news-demo.html. Los registros de experimentos se guardan en SQLite.

La página evidence.html conecta resultados, pruebas y código para un revisor. RECRUITER_GUIDE.md relaciona capacidades demostradas con áreas de tus candidaturas y señala lo que estos proyectos todavía no demuestran.
