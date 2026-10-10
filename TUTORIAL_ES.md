# Tutorial en español: Media Prediction Lab

## 1. Qué problema resuelve

El modelo aprende una relación entre duración, hora y formato, y una tasa de interacción ficticia. Después predice una publicación que todavía no ha ocurrido.

## 2. Pruébalo primero

Abre https://erickvera610.github.io/media-content-lab/ . La demo funciona en tu navegador. Cambia un control y compara la salida. Los datos ficticios no son usuarios reales; los ejemplos tampoco representan trabajo realizado para una empresa.

## 3. Instálalo paso a paso

1. Instala Python desde python.org y Git desde git-scm.com.
2. Abre PowerShell y escribe `python --version` y `git --version`.
3. Escribe `git clone https://github.com/erickvera610/media-content-lab.git`.
4. Escribe `cd media-content-lab`.
5. Escribe `python app.py` y mantén abierta la terminal.
6. Abre http://127.0.0.1:8000 y prueba los controles.
7. Detén el servidor con Ctrl+C.

## 4. La secuencia de trabajo

`Pre-publication metadata → regularized regression → validation tuning → final test`

**Features** son entradas disponibles antes de publicar: duración, hora y formato. **Target** es lo que queremos predecir: tasa de interacción. **Regresión** ajusta pesos para reducir el error. **Regularización ridge** penaliza pesos grandes; probamos tres intensidades. Entrenamiento aprende los pesos; validación selecciona la intensidad; prueba mide el error final. Reentrenamos con entrenamiento más validación después de elegir la intensidad.

Un MAE de 0.005 equivale a aproximadamente 0.5 puntos porcentuales. No uses likes o comentarios como entradas para predecir una publicación antes de publicarla: todavía no existen. Los coeficientes de este ejemplo describen datos generados, no causas comprobadas en redes sociales.

## 5. Leer el código con calma

Empieza por `core.py` y busca `run`. Después abre el archivo especializado indicado en README. Sigue una sola entrada hasta su salida. Lee las pruebas: cada una describe un comportamiento concreto. Por último, revisa `enhanced.js` para comparar la versión del navegador.

## 6. Reproducir los resultados

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
```

Abre `benchmark-results.json` y compara su resumen con `CASE_STUDY.md`. El reporte incluye una hora real de ejecución. Los experimentos con semillas repetidas muestran varios resultados; no escogemos solo el mejor. Las métricas sintéticas de JavaScript pueden diferir de Python.

## 7. Tu siguiente mejora personal

Añade codificación cíclica para la hora y compara con el modelo actual. Después usa un dataset público permitido, documenta privacidad y evita que el mismo creador aparezca en entrenamiento y prueba.

```bash
git switch -c feature/my-improvement
# Edita código y ejecuta las pruebas
git add .
git commit -m "Describe the actual behavior change"
git push -u origin feature/my-improvement
```

Abre un pull request y explica problema, solución, resultado y límite. Se usó asistencia de IA para construir esta base. En una entrevista distingue lo que recibiste, lo que estudiaste y lo que realmente cambiaste.

## 8. Practicar la entrevista

- What problem does this application solve?
- Which data are available when the prediction is made?
- What is the simplest baseline?
- How did you avoid data leakage or inconsistent state?
- Which result surprised you?
- What failure case remains?
- What did you personally improve?

Primero responde en español. Después prepara cuatro frases cortas en inglés: problema, método, resultado y limitación. Usa solo resultados documentados.
