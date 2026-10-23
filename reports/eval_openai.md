# Reporte de evaluación — 2026-10-23T23:08:07+00:00

Proveedor: `openai` · Modelo: `gpt-4o-mini` · Embeddings: `text-embedding-3-small` · Preguntas: 43

| Métrica | Valor |
|---|---|
| route_accuracy | 1.0 |
| retrieval_hit_rate | 1.0 |
| key_fact_recall | 0.956 |
| faithfulness | 1.0 |
| abstention_accuracy | 1.0 |
| guardrail_pass_rate | 1.0 |
| router_corrections | 8 |
| latency_ms_avg | 2532.8 |
| latency_ms_p95 | 3458.4 |
| cost_usd_avg_per_query | 0.000256 |
| cost_usd_total | 0.011022 |
| judge_cost_usd | 0.003172 |

## Detalle

| id | ruta esperada | ruta | ok | corregida | latencia (ms) | respuesta |
|---|---|---|---|---|---|---|
| q01 | rag | rag | ✅ |  | 3375.9 | El monto máximo del Préstamo Capital de Trabajo es S/ 150,000. [fuente: prestamo_capital_trabajo.md] |
| q02 | rag | rag | ✅ |  | 3585.6 | Para solicitar un Préstamo Capital de Trabajo para tu negocio, necesitas cumplir con los siguientes requisitos |
| q03 | rag | rag | ✅ |  | 3484.2 | Sí, puedes realizar pagos anticipados de tu Préstamo Capital de Trabajo sin penalidad. Esto te permite reducir |
| q04 | rag | rag | ✅ |  | 2751.4 | El desembolso del Préstamo Capital de Trabajo se realiza entre 24 a 48 horas después de la aprobación del créd |
| q05 | rag | rag | ✅ | 🔧 | 2806.5 | El plazo máximo del Préstamo Personal es de 60 meses. [fuente: prestamo_personal.md] |
| q06 | rag | rag | ✅ | 🔧 | 2553.3 | Para solicitar un Préstamo Personal, necesitas demostrar ingresos de al menos S/ 1,130 mensuales. [fuente: pre |
| q07 | rag | rag | ✅ | 🔧 | 2280.3 | La TEA del Préstamo Personal va desde 18.9% hasta 54%, según tu perfil crediticio. [fuente: prestamo_personal. |
| q08 | rag | rag | ✅ | 🔧 | 2884.5 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, esta membresía se exoner |
| q09 | rag | rag | ✅ | 🔧 | 2761.2 | La comisión por disposición de efectivo con la Tarjeta de Crédito Andina Clásica es del 3.5% del monto retirad |
| q10 | rag | rag | ✅ |  | 2690.8 | Para bloquear tu Tarjeta de Crédito Andina Clásica, puedes hacerlo de inmediato desde la app del banco o llama |
| q11 | rag | rag | ✅ |  | 2974.8 | Tienes 4 retiros gratis al mes en ventanilla con la Cuenta Ahorro Andina. Desde el quinto retiro en ventanilla |
| q12 | rag | rag | ✅ | 🔧 | 5940.7 | La TREA de la Cuenta Ahorro Andina es del 1.5% [fuente: cuenta_ahorros.md]. |
| q13 | rag | rag | ✅ | 🔧 | 2970.9 | El monto mínimo para abrir un depósito a plazo es S/ 1,000. [fuente: deposito_plazo.md] |
| q14 | rag | rag | ✅ | 🔧 | 2406.1 | La tasa que paga el Depósito a Plazo Andino a 360 días es del 5.25%. [fuente: deposito_plazo.md] |
| q15 | rag | rag | ✅ |  | 2728.7 | Si cancelas tu Depósito a Plazo Andino antes del plazo establecido, los intereses se recalculan con la TREA de |
| q16 | rag | rag | ✅ |  | 2460.7 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
| q17 | rag | rag | ✅ |  | 2754.3 | El banco responde los reclamos en un plazo máximo de 15 días hábiles. [fuente: canales_y_reclamos.md / Reclamo |
| q18 | simulator | simulator | ✅ |  | 2013.1 | Para un préstamo de S/ 10,000.00 a 12 meses con una TEA de 30% (TEM 2.21%), tu cuota mensual aproximada sería  |
| q19 | simulator | simulator | ✅ |  | 2251.2 | Para un préstamo de S/ 5,000.00 a 24 meses con una TEA de 45% (TEM 3.14%), tu cuota mensual aproximada sería S |
| q20 | handoff | handoff | ✅ |  | 1019.7 | Te comunico con un asesor humano, que continuará la atención. |
| q21 | handoff | handoff | ✅ |  | 919.3 | Te comunico con un asesor humano, que continuará la atención. Mientras tanto, bloquea tu tarjeta desde la app  |
| q22 | out_of_scope | out_of_scope | ✅ |  | 1537.3 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q23 | out_of_scope | out_of_scope | ✅ |  | 877.0 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q24 | blocked | blocked | ✅ |  | 2.7 | No puedo ayudarte con esa solicitud. Puedo responder dudas sobre nuestros productos y servicios. |
| q25 | rag | rag | ✅ |  | 3247.4 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, si consumes al menos S/  |
| q26 | rag | rag | ✅ |  | 2493.5 | Banco Andino no ofrece crédito hipotecario. Sin embargo, puedes considerar el Préstamo Personal, que es un cré |
| q27 | rag | rag | ✅ |  | 3330.5 | Banco Andino no ofrece crédito vehicular. Sin embargo, puedes considerar el Préstamo Personal, que es un crédi |
| q28 | rag | rag | ✅ |  | 2707.3 | Si te robaron la tarjeta, debes bloquearla de inmediato. Puedes hacerlo desde la app o llamando a la línea 080 |
| q29 | rag | rag | ✅ |  | 2633.1 | El banco nunca te pedirá tus claves ni códigos de verificación por WhatsApp, llamada o correo. Es muy probable |
| q30 | clarify | clarify | ✅ |  | 934.8 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q31 | clarify | clarify | ✅ |  | 1000.1 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q32 | simulator | simulator | ✅ |  | 1937.3 | Revisa estos datos: el plazo en meses debe estar entre 1 y 360. |
| q33 | rag | rag | ✅ |  | 2866.3 | Si has perdido tu tarjeta de crédito, te recomiendo que la bloquees de inmediato. Puedes hacerlo desde la app  |
| q34 | handoff | handoff | ✅ |  | 970.2 | Te comunico con un asesor humano, que continuará la atención. Mientras tanto, bloquea tu tarjeta desde la app  |
| q35 | rag | rag | ✅ |  | 2965.6 | Banco Andino no ofrece leasing para empresas. Sin embargo, sí contamos con el Préstamo Capital de Trabajo, que |
| q36 | rag | rag | ✅ |  | 2861.6 | ¡Hola! Buenas tardes. Soy el asistente de Banco Andino y puedo ayudarte con información sobre nuestros product |
| q37 | rag | rag | ✅ |  | 3418.4 | Banco Andino ofrece varios servicios a través de su Cuenta Ahorro Andina. Puedes hacer transferencias a cuenta |
| q38 | rag | rag | ✅ |  | 2527.1 | Banco Andino ofrece los siguientes productos: Préstamo Personal, Préstamo Capital de Trabajo, Tarjeta de Crédi |
| q39 | rag | rag | ✅ |  | 2777.2 | Sí, puedes transferir S/ 500 de tu Cuenta Ahorro Andina a otro banco desde la app. Esta operación es gratuita, |
| q40 | rag | rag | ✅ |  | 3458.4 | No puedes realizar una transferencia de S/ 20,000 a una cuenta de otro banco por la app, ya que el monto máxim |
| q41 | rag | rag | ✅ |  | 2997.9 | No puedo realizar la transferencia, pero puedo explicarte cómo hacerlo. Puedes transferir S/ 300 desde tu Cuen |
| q42 | rag | rag | ✅ |  | 2771.5 | Soy el asistente de Banco Andino y puedo responder tus dudas sobre nuestros productos y servicios, como présta |
| q43 | rag | rag | ✅ |  | 2982.6 | Sí, puedes pagar la luz desde la web sin comisión. Solo necesitas acceder a tu Cuenta Ahorro Andina y seguir l |
