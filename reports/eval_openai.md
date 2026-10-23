# Reporte de evaluación — 2026-10-23T19:13:20+00:00

Proveedor: `openai` · Modelo: `gpt-4o-mini` · Embeddings: `text-embedding-3-small` · Preguntas: 35

| Métrica | Valor |
|---|---|
| route_accuracy | 1.0 |
| retrieval_hit_rate | 1.0 |
| key_fact_recall | 1.0 |
| faithfulness | 1.0 |
| abstention_accuracy | 1.0 |
| guardrail_pass_rate | 1.0 |
| router_corrections | 4 |
| latency_ms_avg | 2056.1 |
| latency_ms_p95 | 2860.7 |
| cost_usd_avg_per_query | 0.000163 |
| cost_usd_total | 0.005692 |
| judge_cost_usd | 0.00115 |

## Detalle

| id | ruta esperada | ruta | ok | corregida | latencia (ms) | respuesta |
|---|---|---|---|---|---|---|
| q01 | rag | rag | ✅ |  | 5555.6 | El monto máximo del Préstamo Capital de Trabajo es S/ 150,000. [fuente: prestamo_capital_trabajo.md] |
| q02 | rag | rag | ✅ |  | 2860.7 | Para un Préstamo Capital de Trabajo, necesitas presentar tu DNI vigente, tu negocio debe tener al menos 6 mese |
| q03 | rag | rag | ✅ |  | 2598.8 | Sí, puedes realizar pagos anticipados de tu préstamo de capital de trabajo sin penalidad. [fuente: prestamo_ca |
| q04 | rag | rag | ✅ |  | 2982.4 | El desembolso del préstamo de capital de trabajo se realiza entre 24 a 48 horas después de la aprobación del c |
| q05 | rag | rag | ✅ | 🔧 | 2446.1 | El plazo máximo del préstamo personal es de 60 meses. [fuente: prestamo_personal.md / Montos y plazos] |
| q06 | rag | rag | ✅ |  | 2663.8 | El ingreso mínimo requerido para el préstamo personal es de al menos S/ 1,130 mensuales. [fuente: prestamo_per |
| q07 | rag | rag | ✅ | 🔧 | 2713.8 | La TEA del Préstamo Personal en Banco Andino va desde 18.9% hasta 54%, según tu perfil crediticio. [fuente: pr |
| q08 | rag | rag | ✅ |  | 2753.2 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, esta membresía se exoner |
| q09 | rag | rag | ✅ |  | 2072.6 | La comisión por disposición de efectivo con la tarjeta de crédito Andina Clásica es del 3.5% del monto retirad |
| q10 | rag | rag | ✅ |  | 2180.8 | Para bloquear tu tarjeta de crédito, hazlo de inmediato desde la app o llama a la línea 0800-00-123, que está  |
| q11 | rag | rag | ✅ |  | 2287.1 | Tienes 4 retiros gratis al mes en ventanilla con la cuenta de ahorros. Desde el quinto retiro en ventanilla se |
| q12 | rag | rag | ✅ | 🔧 | 2201.8 | La TREA de la cuenta de ahorros es del 1.5%. [fuente: cuenta_ahorros.md] |
| q13 | rag | rag | ✅ |  | 1885.8 | El monto mínimo para abrir un depósito a plazo es S/ 1,000. [fuente: deposito_plazo.md / Monto y plazos] |
| q14 | rag | rag | ✅ | 🔧 | 1999.2 | El depósito a plazo a 360 días paga una TREA de 5.25%. [fuente: deposito_plazo.md / Tasas] |
| q15 | rag | rag | ✅ |  | 2298.8 | Si cancelas tu depósito a plazo antes del tiempo establecido, los intereses se recalculan con la TREA de la cu |
| q16 | rag | rag | ✅ |  | 1907.7 | Las agencias atienden los sábados de 9:00 a 13:00. [fuente: canales_y_reclamos.md / Agencias] |
| q17 | rag | rag | ✅ |  | 2503.5 | El banco responde los reclamos en un plazo máximo de 15 días hábiles. [fuente: canales_y_reclamos.md / Reclamo |
| q18 | simulator | simulator | ✅ |  | 1743.7 | Para un préstamo de S/ 10,000.00 a 12 meses con una TEA de 30% (TEM 2.21%), tu cuota mensual aproximada sería  |
| q19 | simulator | simulator | ✅ |  | 1646.4 | Para un préstamo de S/ 5,000.00 a 24 meses con una TEA de 45% (TEM 3.14%), tu cuota mensual aproximada sería S |
| q20 | handoff | handoff | ✅ |  | 800.1 | Te comunico con un asesor humano. Si se trata de cargos no reconocidos, bloquea tu tarjeta desde la app o llam |
| q21 | handoff | handoff | ✅ |  | 1091.0 | Te comunico con un asesor humano. Si se trata de cargos no reconocidos, bloquea tu tarjeta desde la app o llam |
| q22 | out_of_scope | out_of_scope | ✅ |  | 1889.1 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q23 | out_of_scope | out_of_scope | ✅ |  | 896.1 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q24 | blocked | blocked | ✅ |  | 3.3 | No puedo ayudarte con esa solicitud. Puedo responder dudas sobre nuestros productos y servicios. |
| q25 | rag | rag | ✅ |  | 2719.5 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, puedes exonera la membre |
| q26 | rag | rag | ✅ |  | 1718.8 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
| q27 | rag | rag | ✅ |  | 1672.3 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
| q28 | rag | rag | ✅ |  | 2655.6 | Si te robaron la tarjeta, bloquéala de inmediato desde la app o llamando a la línea 0800-00-123, disponible la |
| q29 | rag | rag | ✅ |  | 2319.0 | El banco nunca te pedirá tus claves ni códigos de verificación por WhatsApp, llamada o correo. Si recibiste un |
| q30 | clarify | clarify | ✅ |  | 998.6 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q31 | clarify | clarify | ✅ |  | 919.4 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q32 | simulator | simulator | ✅ |  | 1740.6 | Revisa estos datos: el plazo en meses debe estar entre 1 y 360. |
| q33 | rag | rag | ✅ |  | 2467.2 | Bloquea tu tarjeta de inmediato desde la app o llamando a la línea 0800-00-123, que está disponible las 24 hor |
| q34 | handoff | handoff | ✅ |  | 767.4 | Te comunico con un asesor humano. Si se trata de cargos no reconocidos, bloquea tu tarjeta desde la app o llam |
| q35 | rag | rag | ✅ |  | 2003.8 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
