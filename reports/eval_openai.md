# Reporte de evaluación — 2026-10-23T23:14:52+00:00

Proveedor: `openai` · Modelo: `gpt-4o-mini` · Embeddings: `text-embedding-3-small` · Preguntas: 43

| Métrica | Valor |
|---|---|
| route_accuracy | 1.0 |
| retrieval_hit_rate | 1.0 |
| key_fact_recall | 0.956 |
| faithfulness | 1.0 |
| abstention_accuracy | 1.0 |
| guardrail_pass_rate | 1.0 |
| router_corrections | 7 |
| latency_ms_avg | 2391.0 |
| latency_ms_p95 | 3378.7 |
| cost_usd_avg_per_query | 0.000262 |
| cost_usd_total | 0.011258 |
| judge_cost_usd | 0.003356 |

## Detalle

| id | ruta esperada | ruta | ok | corregida | latencia (ms) | respuesta |
|---|---|---|---|---|---|---|
| q01 | rag | rag | ✅ |  | 3210.9 | El monto máximo del Préstamo Capital de Trabajo es S/ 150,000. [fuente: prestamo_capital_trabajo.md] |
| q02 | rag | rag | ✅ |  | 3076.1 | Para solicitar un Préstamo Capital de Trabajo para tu negocio, necesitas presentar tu DNI vigente, tu negocio  |
| q03 | rag | rag | ✅ |  | 3385.3 | Sí, puedes realizar pagos anticipados de tu Préstamo Capital de Trabajo sin penalidad. Esto te permite reducir |
| q04 | rag | rag | ✅ |  | 2474.5 | El desembolso del Préstamo Capital de Trabajo se realiza entre 24 a 48 horas después de la aprobación del créd |
| q05 | rag | rag | ✅ | 🔧 | 2672.4 | El plazo máximo del Préstamo Personal es de 60 meses. [fuente: prestamo_personal.md] |
| q06 | rag | rag | ✅ | 🔧 | 2368.8 | Para el Préstamo Personal, se requiere un ingreso demostrable de al menos S/ 1,130 mensuales. [fuente: prestam |
| q07 | rag | rag | ✅ | 🔧 | 2419.5 | La TEA del Préstamo Personal va desde 18.9% hasta 54%, según tu perfil crediticio. [fuente: prestamo_personal. |
| q08 | rag | rag | ✅ | 🔧 | 2715.4 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, esta membresía se exoner |
| q09 | rag | rag | ✅ |  | 2717.0 | La comisión por disposición de efectivo con la Tarjeta de Crédito Andina Clásica es del 3.5% del monto retirad |
| q10 | rag | rag | ✅ |  | 2748.2 | Puedes bloquear tu Tarjeta de Crédito Andina Clásica de inmediato desde la app o llamando a la línea 0800-00-1 |
| q11 | rag | rag | ✅ |  | 2870.2 | Tienes 4 retiros gratis al mes en ventanilla con tu Cuenta Ahorro Andina. Desde el quinto retiro en ventanilla |
| q12 | rag | rag | ✅ | 🔧 | 2466.6 | La TREA de la Cuenta Ahorro Andina es del 1.5%. [fuente: cuenta_ahorros.md] |
| q13 | rag | rag | ✅ | 🔧 | 2560.1 | El monto mínimo para abrir un depósito a plazo es S/ 1,000. [fuente: deposito_plazo.md / Monto y plazos] |
| q14 | rag | rag | ✅ | 🔧 | 2479.9 | La tasa que paga el Depósito a Plazo Andino a 360 días es del 5.25%. [fuente: deposito_plazo.md] |
| q15 | rag | rag | ✅ |  | 3071.8 | Si cancelas tu Depósito a Plazo Andino antes del plazo establecido, los intereses se recalculan con la TREA de |
| q16 | rag | rag | ✅ |  | 2226.2 | Las agencias de Banco Andino atienden los sábados de 9:00 a 13:00. [fuente: canales_y_reclamos.md] |
| q17 | rag | rag | ✅ |  | 2518.3 | El banco responde los reclamos en un plazo máximo de 15 días hábiles. [fuente: canales_y_reclamos.md / Reclamo |
| q18 | simulator | simulator | ✅ |  | 1948.3 | Para un préstamo de S/ 10,000.00 a 12 meses con una TEA de 30% (TEM 2.21%), tu cuota mensual aproximada sería  |
| q19 | simulator | simulator | ✅ |  | 1970.6 | Para un préstamo de S/ 5,000.00 a 24 meses con una TEA de 45% (TEM 3.14%), tu cuota mensual aproximada sería S |
| q20 | handoff | handoff | ✅ |  | 1003.0 | Te comunico con un asesor humano, que continuará la atención. |
| q21 | handoff | handoff | ✅ |  | 1047.6 | Te comunico con un asesor humano, que continuará la atención. Mientras tanto, bloquea tu tarjeta desde la app  |
| q22 | out_of_scope | out_of_scope | ✅ |  | 890.7 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q23 | out_of_scope | out_of_scope | ✅ |  | 976.3 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q24 | blocked | blocked | ✅ |  | 2.1 | No puedo ayudarte con esa solicitud. Puedo responder dudas sobre nuestros productos y servicios. |
| q25 | rag | rag | ✅ |  | 3431.3 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, si consumes al menos S/  |
| q26 | rag | rag | ✅ |  | 2752.8 | Banco Andino no ofrece crédito hipotecario. Sin embargo, puedes considerar el Préstamo Personal, que es un cré |
| q27 | rag | rag | ✅ |  | 2714.4 | Banco Andino no ofrece un crédito vehicular. Sin embargo, puedes considerar el Préstamo Personal, que es un cr |
| q28 | rag | rag | ✅ |  | 2840.8 | Si te robaron tu Tarjeta de Crédito Andina Clásica, debes bloquearla de inmediato. Puedes hacerlo desde la app |
| q29 | rag | rag | ✅ |  | 3078.3 | No, ese mensaje no es del banco. El Banco Andino nunca te pedirá tus claves ni códigos de verificación por Wha |
| q30 | clarify | clarify | ✅ |  | 1013.6 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q31 | clarify | clarify | ✅ |  | 930.7 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q32 | simulator | simulator | ✅ |  | 2184.4 | Revisa estos datos: el plazo en meses debe estar entre 1 y 360. |
| q33 | rag | rag | ✅ |  | 2513.3 | Si perdiste tu tarjeta de crédito, debes bloquearla de inmediato. Puedes hacerlo desde la app de Banco Andino  |
| q34 | handoff | handoff | ✅ |  | 942.6 | Te comunico con un asesor humano, que continuará la atención. Mientras tanto, bloquea tu tarjeta desde la app  |
| q35 | rag | rag | ✅ |  | 3378.7 | Banco Andino no ofrece leasing para empresas. Sin embargo, sí contamos con el Préstamo Capital de Trabajo, que |
| q36 | rag | rag | ✅ |  | 2515.2 | ¡Hola! Buenas tardes. Soy el asistente de Banco Andino y puedo ayudarte con dudas sobre nuestros productos, se |
| q37 | rag | rag | ✅ |  | 3449.3 | Banco Andino ofrece varios servicios a través de su Cuenta Ahorro Andina. Puedes hacer transferencias a cuenta |
| q38 | rag | rag | ✅ |  | 2544.1 | Banco Andino ofrece los siguientes productos: Préstamo Personal, Préstamo Capital de Trabajo, Tarjeta de Crédi |
| q39 | rag | rag | ✅ |  | 2987.6 | Sí, puedes transferir S/ 500 de tu Cuenta Ahorro Andina a otro banco desde la app. Esta operación es gratuita, |
| q40 | rag | rag | ✅ |  | 2860.5 | No puedes realizar una transferencia de S/ 20,000 a una cuenta de otro banco por la app, ya que el límite diar |
| q41 | rag | rag | ✅ |  | 3138.8 | No puedo realizar la transferencia, pero puedo explicarte cómo hacerlo. Puedes transferir S/ 300 desde tu Cuen |
| q42 | rag | rag | ✅ |  | 3299.0 | Soy el asistente de Banco Andino y puedo responder tus dudas sobre nuestros productos y servicios, como présta |
| q43 | rag | rag | ✅ |  | 2418.1 | Sí, puedes pagar la luz desde la web sin comisión. Solo necesitas acceder a tu Cuenta Ahorro Andina y seguir l |
