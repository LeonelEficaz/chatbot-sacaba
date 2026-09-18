# Documentacion de APIs del proyecto

## 1. Resumen

El proyecto tiene configuradas tres integraciones externas relacionadas con inteligencia artificial:

1. OpenAI.
2. Hugging Face.
3. Google Gemini.

Sin embargo, en el estado actual de los archivos disponibles, estas integraciones no estan conectadas a una funcion de backend. Las variables aparecen en `.env`, pero no deben publicarse ni compartirse. El archivo `.env` esta excluido mediante `.gitignore`.

## 2. OpenAI

### Variables configuradas

```env
OPENAI_API_KEY=clave_privada
OPENAI_MODEL=gpt-4o-mini
OPENAI_AUDIO_MODEL=whisper-1
```

### Funcion

OpenAI puede utilizarse para implementar el chatbot municipal. El modelo `gpt-4o-mini` esta orientado a generar respuestas de texto, explicar tramites, responder preguntas frecuentes y mantener una conversacion con el ciudadano.

El modelo `whisper-1` sirve para convertir audio en texto. Por ejemplo, un ciudadano podria enviar una pregunta de voz y el sistema podria transcribirla antes de enviarla al modelo conversacional.

### Flujo previsto

1. El usuario escribe o graba una consulta.
2. El backend recibe la consulta.
3. Si la consulta es audio, Whisper la convierte a texto.
4. El backend envia el texto a `gpt-4o-mini`.
5. El modelo genera una respuesta sobre tramites, multas, horarios o contacto.
6. El backend devuelve la respuesta al navegador.

### Seguridad

La clave de OpenAI debe permanecer unicamente en el servidor, dentro de una variable de entorno. Nunca debe escribirse en JavaScript, HTML, GitHub ni capturas de pantalla.

## 3. Hugging Face

### Variable configurada

```env
HF_API_TOKEN=token_privado
```

### Funcion

Hugging Face permite consumir modelos de inteligencia artificial publicados en su plataforma. Puede utilizarse para clasificacion de texto, traduccion, analisis de intenciones, generacion de respuestas o reconocimiento de lenguaje, dependiendo del modelo seleccionado.

En este proyecto podria utilizarse para:

- Identificar si la consulta corresponde a un tramite, multa, horario o contacto.
- Clasificar la intencion del usuario.
- Traducir consultas entre espanol y quechua si existe un modelo apropiado.
- Procesar texto con modelos especializados.

### Flujo previsto

1. El backend recibe el texto del ciudadano.
2. El backend envia el texto y el token a un modelo de Hugging Face.
3. El modelo procesa la consulta.
4. El backend interpreta el resultado.
5. El sistema devuelve una respuesta al usuario.

El token solo debe utilizarse en el backend y nunca en el navegador.

## 4. Google Gemini

### Variables configuradas

```env
GEMINI_API_KEY=clave_privada
GEMINI_MODEL=gemini-1.5-flash
```

### Funcion

Gemini puede utilizarse como alternativa a OpenAI para generar respuestas de texto. `gemini-1.5-flash` esta orientado a respuestas rapidas y puede apoyar la atencion automatizada del chatbot.

Puede responder consultas sobre:

- Requisitos de tramites.
- Costos y tiempos aproximados.
- Ubicacion de oficinas.
- Multas municipales y de transito.
- Horarios de atencion.
- Informacion institucional.

### Flujo previsto

1. El ciudadano envia una pregunta.
2. El backend agrega instrucciones para que la respuesta sea clara y municipal.
3. Gemini procesa la solicitud.
4. El backend valida o adapta la respuesta.
5. La respuesta se muestra en el chatbot.

La clave de Gemini tambien debe mantenerse en el servidor y fuera del repositorio.

## 5. Cuantas APIs tiene el proyecto

### APIs externas configuradas

El proyecto tiene **3 servicios externos configurados**:

| Servicio | Modelos o recurso | Funcion prevista |
|---|---|---|
| OpenAI | `gpt-4o-mini` | Generacion de respuestas de texto. |
| OpenAI | `whisper-1` | Transcripcion de audio a texto. |
| Hugging Face | Modelo seleccionado por la aplicacion | Clasificacion, traduccion o procesamiento de texto. |
| Google Gemini | `gemini-1.5-flash` | Generacion alternativa de respuestas. |

Aunque la tabla contiene cuatro recursos, pertenecen a tres proveedores o servicios: OpenAI, Hugging Face y Google Gemini.

### Estado actual

En los archivos disponibles actualmente no se encontraron llamadas efectivas a estos servicios. Por tanto:

- APIs configuradas: 3 proveedores.
- Recursos o modelos configurados: 4.
- APIs externas activas en el codigo disponible: 0.
- Claves que deben protegerse: 3 tipos de credenciales.

## 6. Diferencia entre API y variable de entorno

Una variable como `OPENAI_API_KEY` no es la API completa. Es una credencial que permite autenticar solicitudes ante un servicio.

La API es el servicio remoto y sus operaciones. La clave es el mecanismo privado que autoriza al sistema a utilizarlo.

Ejemplo conceptual:

```text
Aplicacion Flask -> API de OpenAI -> Respuesta del modelo
        |
        +-> OPENAI_API_KEY almacenada en el servidor
```

## 7. Recomendaciones de seguridad

- No subir `.env` a GitHub.
- No colocar claves en `index.html` ni en archivos JavaScript del navegador.
- Revocar y regenerar cualquier clave que haya sido expuesta.
- Usar variables de entorno en el servidor.
- Limitar permisos y cuotas de cada proveedor.
- Revisar el consumo para evitar costos inesperados.
- Utilizar respuestas controladas para no presentar requisitos municipales incorrectos.

## 8. Conclusiones

El proyecto fue preparado para trabajar con tres proveedores de inteligencia artificial: OpenAI, Hugging Face y Google Gemini. OpenAI tiene configurados un modelo de texto y uno de audio; Hugging Face tiene un token para modelos externos; y Gemini tiene configurado un modelo de respuestas rapidas.

La configuracion por si sola no significa que las APIs esten funcionando. Para activarlas se necesita implementar en el backend las solicitudes HTTP o los SDK oficiales, validar las respuestas y conectar el resultado con el chatbot. Las claves actuales deben mantenerse privadas y no formar parte del repositorio publico.
