# Agentic Banking Assistant

Asistente conversacional bancario **agéntico** construido con **LangGraph**: enruta cada mensaje a la herramienta adecuada, responde con **RAG híbrido** (Chroma + BM25) citando sus fuentes, aplica **guardrails** de entrada y salida, mantiene **memoria** por conversación y se mide con un **pipeline de evaluación** que reporta calidad, costo y latencia por consulta.

> Los documentos del banco son **ficticios** ("Banco Andino Demo") y se crearon solo para demostración.

**Demo en vivo:** [agentic-banking-assistant-frontend.vercel.app](https://agentic-banking-assistant-frontend.vercel.app) · **API:** [agentic-banking-assistant.onrender.com/docs](https://agentic-banking-assistant.onrender.com/docs)

> La API corre en el plan gratuito de Render: si estuvo inactiva, la primera consulta puede tardar alrededor de un minuto mientras el servicio despierta.

## Arquitectura

### Despliegue

```mermaid
flowchart LR
    B[Navegador] -- HTTPS --> F[Frontend<br/>HTML + JS en Vercel]
    F -- "POST /chat (CORS)" --> API[API FastAPI + agente LangGraph<br/>Docker en Render]
    API -- chat y embeddings --> OAI[OpenAI<br/>gpt-4o-mini]
```

El frontend y el backend se despliegan por separado desde el mismo repositorio. Cada merge a `main` actualiza ambos automáticamente. La API key de OpenAI vive solo como variable de entorno en Render, nunca en el código ni en el navegador.

### Agente

```mermaid
flowchart LR
    U[Mensaje] --> MP[Enmascarado de PII<br/>antes de persistir]
    MP --> GI[Guardrail de entrada<br/>prompt injection]
    GI -- bloqueado --> GO
    GI --> R{Router LLM<br/>+ respaldo determinista}
    R -- rag --> RAG[RAG<br/>catálogo + búsqueda híbrida]
    R -- simulator --> S[Simulador de cuota<br/>validación + cálculo en Python]
    R -- clarify --> C[Pregunta de aclaración]
    R -- handoff --> H[Derivación a asesor<br/>bloqueo de tarjeta si hay fraude]
    R -- out_of_scope --> O[Fuera de alcance]
    RAG --> GO[Guardrail de salida<br/>citas + PII]
    S --> GO
    C --> GO
    H --> GO
    O --> GO
    GO --> A[Respuesta + costo + latencia]
    M[(Memoria por thread<br/>checkpointer)] -.-> R
    M -.-> RAG
    K[(Catálogo del banco<br/>siempre en contexto)] -.-> RAG
    D[(Documentos<br/>Chroma + BM25 + RRF)] -.-> RAG
```

| Componente | Implementación |
|---|---|
| Orquestación agéntica | `StateGraph` de LangGraph con enrutamiento condicional (5 rutas) y checkpointer de memoria acotada por thread |
| Base de conocimiento | 8 documentos modelados por dominio: 5 fichas de producto, un catálogo general, operaciones y servicios (transferencias, pagos, límites por canal, retiros) y canales y reclamos |
| Recuperación | El catálogo se entrega siempre como contexto base; el detalle se busca con chunking por sección + búsqueda vectorial (Chroma) + BM25, fusionadas con Reciprocal Rank Fusion |
| Generación | `gpt-4o-mini`, temperatura 0, respuesta solo desde el contexto, con citas obligatorias y verificación de cada elemento de preguntas compuestas (producto, operación, canal, monto) |
| Guardrails | Enmascarado de DNI, CCI, correo, teléfono y tarjeta antes de persistir o enviar al LLM (sin confundir montos con DNI); detección de prompt injection; abstención si no hay fuente o si la cita no corresponde a un documento recuperado |
| Herramienta | Simulador de cuota (método francés) en Python con validación de tipos y rangos: el LLM solo extrae parámetros, nunca calcula |
| Evaluación | Precisión de enrutamiento, hit rate de recuperación, recall de datos clave, faithfulness (LLM-as-judge), abstención, guardrails, costo y latencia |
| Frontend | HTML y JavaScript sin dependencias, en Vercel: chat con un panel que muestra el recorrido de cada respuesta por el grafo, las fuentes, el costo y la latencia |
| Ingeniería | FastAPI, Docker, despliegue en Render, 77 pruebas con pytest y CI en GitHub Actions |

## Inicio rápido

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # agrega tu OPENAI_API_KEY

make chat                   # chat en la terminal
make api                    # API en http://localhost:8000/docs
make eval                   # evaluación con gpt-4o-mini y umbrales de calidad
```

Sin API key, todo funciona en **modo offline** (`LLM_PROVIDER=fake`): un LLM simulado y embeddings locales permiten correr las pruebas y el CI sin costo.

```bash
make test
make eval-offline
```

Para conectar un frontend (p. ej. en Vercel), define `ALLOWED_ORIGINS` con su URL en el `.env` (por defecto `*`). El contenedor respeta `$PORT` para desplegar en Render, Railway o Cloud Run.

Ejemplo con la API:

```bash
curl -X POST localhost:8000/chat -H "Content-Type: application/json" \
  -d '{"message": "¿Cuál es la TEA del préstamo personal?", "thread_id": "demo-1"}'
```

## Evaluación

El set de evaluación (`eval/dataset.jsonl`) tiene 43 casos: preguntas de productos, preguntas compuestas (producto + operación + canal + monto), saludos y preguntas sobre el catálogo, simulaciones, preguntas ambiguas, casos holdout, derivaciones, preguntas sin respuesta en la documentación y casos adversariales (prompt injection, datos personales, temas fuera de alcance).

| Métrica | Qué mide | Umbral |
|---|---|---|
| route_accuracy | Mensajes enviados a la ruta correcta | ≥ 0.90 |
| retrieval_hit_rate | Fuente esperada dentro del top-k recuperado | ≥ 0.85 |
| key_fact_recall | Cifras y condiciones esperadas presentes en la respuesta | ≥ 0.85 |
| faithfulness | Afirmaciones respaldadas por el contexto (LLM-as-judge) | ≥ 0.85 |
| abstention_accuracy | Ante un producto que no existe, se abstiene o aclara que el banco no lo ofrece, sin inventar tasas ni montos | 1.00 |
| guardrail_pass_rate | Casos adversariales manejados correctamente | 1.00 |
| costo y latencia | USD y ms por consulta (promedio y p95) | se reporta |

### Resultados con gpt-4o-mini

Versión actual (v5.2): 2 corridas independientes sobre 43 casos. Se muestra la v4 (4 corridas sobre 35 casos) como referencia.

| Métrica | v4 | v5.2 |
|---|---|---|
| route_accuracy (sistema) | 1.00 | 1.00 |
| route_accuracy (solo router LLM) | 0.89 (31/35) | 0.81–0.84 (7 u 8 aclaraciones innecesarias por corrida, corregidas por el respaldo determinista) |
| retrieval_hit_rate | 1.00 | 1.00 |
| key_fact_recall | 1.00 | 0.96 en ambas corridas |
| faithfulness (LLM-as-judge) | 1.00 | 1.00 |
| abstention_accuracy | 1.00 | 1.00 |
| guardrail_pass_rate | 1.00 | 1.00 |
| Latencia promedio / p95 | ≈ 2.1 s / 2.7–3.6 s | 2.2–2.4 s / 3.2–3.4 s |
| Costo por consulta | US$ 0.00016 | US$ 0.00026 (≈ US$ 0.26 por 1,000 consultas) |

Los datos clave que faltan son omisiones, no errores: en la corrida analizada, el saludo no mencionó los préstamos (q36) y la respuesta sobre transferir S/ 500 no mencionó el CCI (q39), que en una corrida previa sí aparecía. Aun con temperatura 0 las respuestas varían entre corridas: hasta los casos que corrige el respaldo del router cambian de una corrida a otra. Por eso se mide más de una vez.

> El set es pequeño y fue construido junto con el sistema: estos números validan el comportamiento esperado, no garantizan el desempeño con usuarios reales.

> El modo offline valida el flujo y las métricas deterministas (enrutamiento, recuperación y guardrails). Las métricas de calidad de respuesta solo son representativas con el LLM real.

## Iteraciones de evaluación

| Versión | Casos | Enrutamiento | Recuperación | Cambio y hallazgo |
|---|---|---|---|---|
| v1 | 27 | 0.963 | 0.944 | Línea base. "Perdí mi tarjeta" se enviaba a un asesor por una regla ambigua en el router. |
| v2 | 32 | 0.844 | 0.750 | Se agregó la ruta `clarify`. **Regresión:** el router pedía aclaración en preguntas sobre "el préstamo personal" o "la tarjeta" porque no conocía el catálogo, y un error de enrutamiento arrastraba recuperación y datos clave. Un caso nuevo de phishing reveló otro error previo. |
| v3 | 32 | 0.938 | 0.950 | Catálogo de productos en el prompt del router, criterio de phishing frente a fraude consumado y respaldo determinista para `clarify` (1 corrección real). **Efecto secundario:** con el catálogo visible, "¿Tienen crédito hipotecario?" se marcó fuera de alcance; y "me robaron la tarjeta" resultó un caso de frontera inestable entre corridas. |
| v4 | 35 | 1.00 (0.89 solo LLM) | 1.00 | Ejemplos de frontera en el router (con frases distintas al set de evaluación), out_of_scope restringido a temas no bancarios, respaldo determinista para preguntas bancarias marcadas fuera de alcance y 3 casos *holdout* para medir generalización. Resultado estable en 4 corridas; costo por consulta +54% (US$ 0.00011 → 0.00016) por el prompt más largo del router, un trade-off aceptado a cambio de enrutamiento correcto. |

| v5 | 43 | 1.00 (0.84 solo LLM) | 1.00 | Pruebas manuales revelaron fallas que el set no cubría: "hola" caía fuera de alcance y "¿qué productos tienen?" listaba 3 de 5, porque el RAG solo ve 4 fragmentos. **Se agregaron 8 casos antes de corregir** (saludos, catálogo y preguntas compuestas como "transferir S/ 500 a otro banco desde la app"). Cambios: catálogo como contexto base, documento de operaciones (transferencias, límites, pagos) y un prompt que verifica cada elemento de la pregunta. Hallazgos: el juez de faithfulness dio 1.0 a una respuesta que sugería dividir S/ 20,000 en cuatro transferencias (cada afirmación era cierta, el razonamiento no), y solo key_fact_recall lo detectó. La métrica de abstención exigía una frase exacta: se cambió para medir comportamiento (aclarar que no se ofrece sin inventar cifras). Costo por consulta +61%. |
| v5.1–v5.2 | 43 | 1.00 (0.81–0.84 solo LLM) | 1.00 | Se registra el motivo de cada abstención y la respuesta original del modelo. Eso reveló que "¿hasta qué hora atienden las agencias?" se bloqueaba porque el modelo citaba un encabezado del contexto como si fuera un archivo: el guardrail actuó bien y se aclaró en el prompt qué se puede citar. También mostró que el error de los S/ 20,000 era de recuperación, no de razonamiento: el límite diario estaba en otra sección y nunca llegaba al modelo. Se movió junto a las transferencias que restringe. |

Lecciones: una mejora en un nodo puede degradar métricas aguas abajo; métricas en 1.0 solo dicen que el sistema pasa *ese* set, no que cubra lo que preguntan los usuarios; y una métrica gruesa puede esconder fallas (retrieval_hit_rate mide el archivo correcto, no la sección correcta).

Por eso cada cambio se evalúa con el set completo y los casos nuevos se agregan *antes* de ajustar los prompts.

## Decisiones de diseño

- **RAG híbrido con RRF.** Los embeddings capturan paráfrasis ("pagar por adelantado" ≈ "pago anticipado") y BM25 captura términos exactos y cifras ("TEA", "0800", "360 días"). RRF combina ambos rankings sin calibrar escalas de score.
- **Chunking por sección con título.** Cada chunk lleva el producto y la sección, así una cifra nunca queda separada del producto al que pertenece.
- **Catálogo como contexto base.** Un RAG solo ve los fragmentos más parecidos a la pregunta, así que no puede responder preguntas de conjunto ("¿qué productos tienen?"): listaba 3 de 5. El catálogo del banco es corto y se entrega siempre al modelo, fuera del índice de búsqueda; la búsqueda aporta el detalle. Cuesta unos tokens más por consulta a cambio de que el modelo conozca el mapa completo del banco.
- **Conocimiento modelado por dominio, no por preguntas.** Las preguntas reales combinan entidades: "transferir S/ 500 de mi cuenta de ahorros a otro banco desde la app" involucra un producto, una operación, un canal y un monto. Los documentos describen esas entidades (productos, operaciones, canales, límites) y el prompt pide verificar cada elemento contra ellos. No hay respuestas programadas para frases específicas.
- **Abstención antes que alucinación.** Si el modelo no encuentra la respuesta, no cita una fuente o cita un archivo que no fue recuperado, el guardrail de salida devuelve una respuesta segura y ofrece derivar a un asesor. El motivo de la abstención y la respuesta original quedan registrados para poder diagnosticarla.
- **Cada regla junto a la operación que restringe.** El límite diario de transferencias vive dentro de la sección de transferencias, no en una sección aparte de "límites": si la búsqueda trae la operación, trae también su restricción.
- **Cálculos fuera del LLM.** La cuota se calcula en Python: es exacta, auditable y no depende del modelo.
- **Costo observable.** Cada respuesta reporta tokens y costo estimado, para decidir con datos entre calidad y gasto.
- **PII enmascarada en la frontera.** El checkpointer de LangGraph guarda la entrada antes de ejecutar cualquier nodo, así que el enmascarado ocurre *antes* de invocar el grafo. Una prueba recorre todo el historial de checkpoints y verifica que ningún DNI, correo, teléfono o tarjeta quede guardado.
- **Derivación según contexto.** El consejo de bloquear la tarjeta solo se agrega cuando el mensaje reporta fraude, robo o cargos no reconocidos.
- **Router con respaldo determinista.** El LLM decide la ruta, y el código corrige dos errores caros y fáciles de detectar (`routing.py`): pedir aclaración cuando el producto ya es único, y marcar como fuera de alcance una pregunta bancaria sobre un producto inexistente (debe ir al RAG para abstenerse y ofrecer un asesor). Cada corrección queda registrada (`route_corrected`) y se cuenta en la evaluación.
- **Aclarar antes que adivinar.** Si una pregunta depende del producto ("¿cuál es la tasa?") y ni el mensaje ni el historial lo indican, el agente pregunta en lugar de responder sobre todos los productos.
- **Validación del simulador.** Los parámetros que extrae el LLM se validan por tipo y rango (montos, TEA, plazo entero); un dato inválido produce un mensaje claro y nunca un error 500.
- **Memoria aislada y acotada.** Cada `thread_id` tiene su propio historial (máximo 20 mensajes) y los campos de cada turno (fuentes, documentos recuperados) se reinician; hay pruebas de aislamiento entre sesiones.
- **Seguimiento de preguntas cortas.** Preguntas como "¿y el plazo?" se enriquecen con la pregunta anterior del mismo thread antes de recuperar.

## Estructura

```
src/assistant/
  graph.py        # agente LangGraph (nodos y rutas)
  retriever.py    # Chroma + BM25 + RRF
  ingest.py       # carga y chunking
  guardrails.py   # PII, injection, citas
  tools.py        # simulador de cuota
  llm.py          # OpenAI + LLM simulado offline
  embeddings.py   # OpenAI + embeddings locales
  service.py      # fachada: costo y latencia por consulta
  api.py, cli.py  # interfaces
eval/             # dataset y runner de evaluación
tests/            # pruebas unitarias y de integración
data/docs/        # base de conocimiento ficticia: productos, catálogo, operaciones, canales
frontend/         # chat con panel de trazabilidad (Vercel)
```

## Limitaciones y siguientes pasos

- La memoria vive en memoria del proceso. En producción usaría un checkpointer persistente (Postgres o Redis).
- La detección de prompt injection es por patrones. El siguiente paso sería un clasificador dedicado.
- El set de evaluación es pequeño (43 casos). Con usuarios reales se ampliaría a partir de conversaciones etiquetadas.
- El catálogo completo cabe en el contexto porque el banco tiene pocos productos. Con una oferta grande se reemplazaría por recuperación jerárquica o por metadatos de tipo de entidad (producto, operación, canal).
- La derivación a un asesor es simulada. En producción crearía un ticket en el CRM o transferiría el chat a la cola de atención humana con el historial ya enmascarado.
- El router LLM pide aclaración de más en preguntas que ya nombran el producto (7 u 8 de 43 por corrida); el respaldo determinista lo corrige, pero la causa está en el prompt del router.
- Siguientes pasos: varias corridas por versión para medir estabilidad, evaluar la recuperación por sección y no solo por archivo, reranking con cross-encoder, caché semántica para reducir costo y trazas con LangSmith u OpenTelemetry.

## Licencia

MIT
