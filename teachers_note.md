Notas para el Profesor: Simulación de Seguridad IoT

Este documento proporciona una guía para estructurar la actividad de iot-secure-app en el aula, facilitando la discusión y la evaluación.

Duración Sugerida

Esta actividad está diseñada para ser flexible. Una estructura recomendada es:

Opción A (3 Sesiones de 90 min):

Sesión 1: Introducción a la Seguridad IoT. Discusión de vectores de ataque. Trabajo práctico con el Módulo 1 (Amenazas IoT: UART y MQTT).

Sesión 2: Análisis de binarios y criptografía. Trabajo práctico con el Módulo 2 (Firmware/Contraseñas) y Módulo 3 (Blockchain).

Sesión 3: Discusión de mitigaciones. Revisión del Módulo 4 (Auditoría) y preparación de la entrega final.

Opción B (2 Sesiones + Tarea):

Sesión 1 (90 min): Introducción y Módulo 1 (UART/MQTT).

Sesión 2 (90 min): Módulo 2 (Firmware) y Módulo 3 (Blockchain).

Tarea (Trabajo en casa): Completar el Módulo 4 (Auditoría) y redactar el informe/entrega basándose en las capturas y exportaciones.

Preguntas de Discusión Clave

Utilice estas preguntas para guiar la discusión en clase después de que los estudiantes hayan experimentado los módulos:

(Módulo 1) ¿Por qué un puerto UART de depuración es un riesgo de seguridad físico tan grande? ¿Cómo se mitigaría esto en un producto real (ej. "epoxy blob", deshabilitar UART en el firmware de producción)?

(Módulo 1) En la simulación de MQTT, el atacante se suscribe a #. ¿Qué significa este carácter y por qué es una configuración tan peligrosa en un broker productivo? (Respuesta: Es un comodín de múltiples niveles, suscribe a todos los tópicos).

(Módulo 2) Discutan el "trade-off" (balance) entre seguridad y facilidad de desarrollo. ¿Por qué un desarrollador podría dejar credenciales hardcodeadas en el firmware? (Respuesta: Prisas, facilidad para pruebas, suponer que "nadie lo verá").

(Módulo 3) La blockchain ofrece integridad, pero no confidencialidad. ¿Qué significa esta distinción? (Respuesta: Se puede probar que los datos no han cambiado, pero cualquiera puede leerlos). ¿Cómo protegerían los datos del sensor dentro de la blockchain? (Respuesta: Cifrándolos antes de escribirlos).

(Módulo 4) Revisando el checklist de auditoría, ¿cuál creen que es el riesgo más probable de encontrar en un dispositivo IoT barato (ej. una cámara IP de bajo coste)? ¿Y cuál consideran el más peligroso?

Errores Comunes a Vigilar en las Entregas

Confusión Criptográfica: Confundir hashing (visto en el Módulo 2, fuerza bruta) con cifrado. Asegúrese de que entienden que un hash es de un solo sentido (one-way).

Fuerza Bruta: No entender por qué funciona el ataque de fuerza bruta (comparación de hash contra hash, no de contraseña contra contraseña).

Magia de la Blockchain: Pensar que la blockchain "oculta" o "cifra" los datos automáticamente. (Ver Pregunta 4).

Culpar al Protocolo: Pensar que "MQTT es inseguro". El problema demostrado no es el protocolo en sí, sino la configuración insegura (sin TLS, sin autenticación, sin ACLs).

Entregar Herramientas: Entregar los scripts self_check.py o pack_for_students.py como parte de su trabajo, sin entender que eran herramientas de ayuda.

Sugerencias de Evaluación (Foco en Evidencia)

Dado que es una simulación, la evaluación debe centrarse en la evidencia de que completaron y entendieron los pasos.

1. Evidencia de Explotación (Capturas de Pantalla):
Solicite capturas de pantalla específicas que demuestren la explotación de cada vulnerabilidad:

Módulo 1: Una captura del log de UART (Página 1, Tab 1) mostrando las credenciales PASS: o MyPass expuestas.

Módulo 1: Una captura del log del Broker MQTT (Página 1, Tab 2) mostrando el JSON con las credenciales device_admin/admin_pass_123.

Módulo 2: El resultado del "Análisis de Firmware" (Página 2, Tab 1) mostrando la root_password_!@# o la key_a1b2c3d4e5f67890.

Módulo 2: El log del ataque de "Fuerza Bruta" (Página 2, Tab 2) mostrando el mensaje de "¡ÉXITO! Contraseña encontrada: 'admin'".

Módulo 3: Una captura de la cadena (Página 3) después de presionar "Verificar" con el mensaje en rojo de "¡Fallo de Integridad!" tras alterar un bloque.

2. Evidencia de Exportación (Archivos/Texto):

Módulo 3: Pedir que copien y peguen el JSON de la cadena antes y después de la alteración para comparar.

3. Evidencia de Comprensión (Análisis Escrito):

Pedir que elijan 2 de las "Preguntas de Discusión" (ver arriba) y escriban una respuesta breve (1-2 párrafos) para cada una.

Pedir que completen el Módulo 4 (Auditoría) y expliquen por qué marcaron 3 de las casillas como lo hicieron, conectándolo con lo que vieron en los módulos 1-3.
