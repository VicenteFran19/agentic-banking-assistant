# Reporte de evaluación — 2026-10-23T22:56:19+00:00

Proveedor: `openai` · Modelo: `gpt-4o-mini` · Embeddings: `text-embedding-3-small` · Preguntas: 43

| Métrica | Valor |
|---|---|
| route_accuracy | 1.0 |
| retrieval_hit_rate | 1.0 |
| key_fact_recall | 0.941 |
| faithfulness | 1.0 |
| abstention_accuracy | 0.667 |
| guardrail_pass_rate | 1.0 |
| router_corrections | 7 |
| latency_ms_avg | 2267.1 |
| latency_ms_p95 | 3038.3 |
| cost_usd_avg_per_query | 0.000254 |
| cost_usd_total | 0.010941 |
| judge_cost_usd | 0.003164 |

## Detalle

| id | ruta esperada | ruta | ok | corregida | latencia (ms) | respuesta |
|---|---|---|---|---|---|---|
| q01 | rag | rag | ✅ |  | 4579.8 | El monto máximo del Préstamo Capital de Trabajo es S/ 150,000. Este préstamo está diseñado para financiar la c |
| q02 | rag | rag | ✅ |  | 3001.3 | Para solicitar un Préstamo Capital de Trabajo para tu negocio, necesitas presentar tu DNI vigente, tu negocio  |
| q03 | rag | rag | ✅ |  | 2504.7 | Sí, puedes realizar pagos anticipados de tu Préstamo Capital de Trabajo sin penalidad. Esto te permite reducir |
| q04 | rag | rag | ✅ |  | 2450.3 | El desembolso del Préstamo Capital de Trabajo se realiza entre 24 a 48 horas después de la aprobación del créd |
| q05 | rag | rag | ✅ | 🔧 | 2303.6 | El plazo máximo del Préstamo Personal es de 60 meses. [fuente: prestamo_personal.md] |
| q06 | rag | rag | ✅ | 🔧 | 2458.4 | Para el Préstamo Personal, se requiere un ingreso demostrable de al menos S/ 1,130 mensuales. [fuente: prestam |
| q07 | rag | rag | ✅ | 🔧 | 2243.4 | La TEA del Préstamo Personal va desde 18.9% hasta 54%, según tu perfil crediticio. [fuente: prestamo_personal. |
| q08 | rag | rag | ✅ |  | 2463.3 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, esta membresía se exoner |
| q09 | rag | rag | ✅ | 🔧 | 2695.6 | La comisión por disposición de efectivo con la Tarjeta de Crédito Andina Clásica es del 3.5% del monto retirad |
| q10 | rag | rag | ✅ |  | 2359.7 | Puedes bloquear tu tarjeta de Crédito Andina Clásica de inmediato desde la app o llamando a la línea 0800-00-1 |
| q11 | rag | rag | ✅ |  | 2678.9 | Tienes 4 retiros gratis al mes en ventanilla con la Cuenta Ahorro Andina. Desde el quinto retiro en ventanilla |
| q12 | rag | rag | ✅ | 🔧 | 2351.8 | La TREA de la Cuenta Ahorro Andina es del 1.5%. [fuente: cuenta_ahorros.md] |
| q13 | rag | rag | ✅ | 🔧 | 2292.6 | El monto mínimo para abrir un depósito a plazo es S/ 1,000. [fuente: deposito_plazo.md / Monto y plazos] |
| q14 | rag | rag | ✅ | 🔧 | 2267.9 | La tasa que paga el Depósito a Plazo Andino a 360 días es del 5.25%. [fuente: deposito_plazo.md] |
| q15 | rag | rag | ✅ |  | 2448.0 | Si cancelas tu Depósito a Plazo Andino antes del plazo establecido, los intereses se recalculan con la TREA de |
| q16 | rag | rag | ✅ |  | 2082.3 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
| q17 | rag | rag | ✅ |  | 2019.7 | El banco responde los reclamos en un plazo máximo de 15 días hábiles. [fuente: canales_y_reclamos.md] |
| q18 | simulator | simulator | ✅ |  | 1832.6 | Para un préstamo de S/ 10,000.00 a 12 meses con una TEA de 30% (TEM 2.21%), tu cuota mensual aproximada sería  |
| q19 | simulator | simulator | ✅ |  | 1888.6 | Para un préstamo de S/ 5,000.00 a 24 meses con una TEA de 45% (TEM 3.14%), tu cuota mensual aproximada sería S |
| q20 | handoff | handoff | ✅ |  | 958.8 | Te comunico con un asesor humano, que continuará la atención. |
| q21 | handoff | handoff | ✅ |  | 1070.3 | Te comunico con un asesor humano, que continuará la atención. Mientras tanto, bloquea tu tarjeta desde la app  |
| q22 | out_of_scope | out_of_scope | ✅ |  | 1392.1 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q23 | out_of_scope | out_of_scope | ✅ |  | 879.3 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q24 | blocked | blocked | ✅ |  | 2.8 | No puedo ayudarte con esa solicitud. Puedo responder dudas sobre nuestros productos y servicios. |
| q25 | rag | rag | ✅ |  | 3155.9 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Además, si consumes al menos S/ 500 a |
| q26 | rag | rag | ✅ |  | 2528.1 | Banco Andino no ofrece crédito hipotecario. Sin embargo, puedes considerar el Préstamo Personal, que es un cré |
| q27 | rag | rag | ✅ |  | 2651.4 | Banco Andino no ofrece crédito vehicular. Sin embargo, puedes considerar el Préstamo Personal, que es un crédi |
| q28 | rag | rag | ✅ |  | 2771.3 | Si te robaron la tarjeta, debes bloquearla de inmediato. Puedes hacerlo desde la app o llamando a la línea 080 |
| q29 | rag | rag | ✅ |  | 2659.0 | El banco nunca te pedirá tus claves ni códigos de verificación por WhatsApp, llamada o correo. Si recibiste un |
| q30 | clarify | clarify | ✅ |  | 1349.0 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q31 | clarify | clarify | ✅ |  | 1132.0 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q32 | simulator | simulator | ✅ |  | 1982.7 | Revisa estos datos: el plazo en meses debe estar entre 1 y 360. |
| q33 | rag | rag | ✅ |  | 3038.3 | Si has perdido tu tarjeta de crédito, te recomiendo que la bloquees de inmediato. Puedes hacerlo desde la app  |
| q34 | handoff | handoff | ✅ |  | 1160.6 | Te comunico con un asesor humano, que continuará la atención. Mientras tanto, bloquea tu tarjeta desde la app  |
| q35 | rag | rag | ✅ |  | 2864.3 | Banco Andino no ofrece leasing para empresas. Sin embargo, sí contamos con el Préstamo Capital de Trabajo, que |
| q36 | rag | rag | ✅ |  | 2254.3 | ¡Hola! Buenas tardes. Soy el asistente de Banco Andino y puedo ayudarte con información sobre nuestros product |
| q37 | rag | rag | ✅ |  | 2754.1 | Banco Andino ofrece varios servicios a través de su Cuenta Ahorro Andina. Puedes hacer transferencias a cuenta |
| q38 | rag | rag | ✅ |  | 2489.6 | Banco Andino ofrece los siguientes productos: Préstamo Personal, Préstamo Capital de Trabajo, Tarjeta de Crédi |
| q39 | rag | rag | ✅ |  | 2530.1 | Sí, puedes transferir S/ 500 de tu Cuenta Ahorro Andina a otro banco desde la app. La transferencia interbanca |
| q40 | rag | rag | ✅ |  | 2826.8 | No puedes realizar una transferencia de S/ 20,000 a una cuenta de otro banco por la app, ya que el monto máxim |
| q41 | rag | rag | ✅ |  | 3189.4 | No puedo realizar la transferencia, pero puedo indicarte cómo hacerlo. Puedes transferir S/ 300 desde tu Cuent |
| q42 | rag | rag | ✅ |  | 2785.5 | Soy tu asistente de Banco Andino y puedo responder dudas sobre nuestros productos y servicios, como préstamos, |
| q43 | rag | rag | ✅ |  | 2136.7 | Sí, puedes pagar la luz desde la web sin comisión. Solo necesitas acceder a tu Cuenta Ahorro Andina para reali |
