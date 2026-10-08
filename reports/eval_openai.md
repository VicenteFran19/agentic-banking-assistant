# Reporte de evaluación — 2026-10-08T21:57:30+00:00

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
| latency_ms_avg | 2188.2 |
| latency_ms_p95 | 3425.1 |
| cost_usd_avg_per_query | 0.000162 |
| cost_usd_total | 0.005679 |
| judge_cost_usd | 0.001138 |

## Detalle

| id | ruta esperada | ruta | ok | corregida | latencia (ms) | respuesta |
|---|---|---|---|---|---|---|
| q01 | rag | rag | ✅ |  | 4538.4 | El monto máximo del Préstamo Capital de Trabajo es S/ 150,000. [fuente: prestamo_capital_trabajo.md] |
| q02 | rag | rag | ✅ |  | 2870.5 | Para un Préstamo Capital de Trabajo, necesitas presentar tu DNI vigente, tu negocio debe tener al menos 6 mese |
| q03 | rag | rag | ✅ |  | 2877.7 | Sí, puedes realizar pagos anticipados de tu préstamo de capital de trabajo sin penalidad. [fuente: prestamo_ca |
| q04 | rag | rag | ✅ |  | 2867.8 | El desembolso del préstamo de capital de trabajo se realiza entre 24 a 48 horas después de la aprobación del c |
| q05 | rag | rag | ✅ | 🔧 | 2664.2 | El plazo máximo del préstamo personal es de 60 meses. [fuente: prestamo_personal.md / Montos y plazos] |
| q06 | rag | rag | ✅ |  | 2466.2 | Se requiere un ingreso demostrable de al menos S/ 1,130 mensuales para acceder al préstamo personal. [fuente:  |
| q07 | rag | rag | ✅ | 🔧 | 2590.1 | La TEA del Préstamo Personal en Banco Andino va desde 18.9% hasta 54%, según tu perfil crediticio. [fuente: pr |
| q08 | rag | rag | ✅ |  | 3052.1 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, esta membresía se exoner |
| q09 | rag | rag | ✅ |  | 2553.2 | La comisión por disposición de efectivo con la tarjeta de crédito Andina Clásica es del 3.5% del monto retirad |
| q10 | rag | rag | ✅ |  | 2641.3 | Para bloquear tu tarjeta, debes hacerlo de inmediato desde la app o llamando a la línea 0800-00-123, que está  |
| q11 | rag | rag | ✅ |  | 2868.2 | Tienes 4 retiros gratis al mes en ventanilla con la cuenta de ahorros. A partir del quinto retiro, se cobra S/ |
| q12 | rag | rag | ✅ | 🔧 | 2627.0 | La TREA de la cuenta de ahorros es del 1.5%. [fuente: cuenta_ahorros.md] |
| q13 | rag | rag | ✅ |  | 2289.0 | El monto mínimo para abrir un depósito a plazo es S/ 1,000. [fuente: deposito_plazo.md / Monto y plazos] |
| q14 | rag | rag | ✅ | 🔧 | 2441.5 | El depósito a plazo a 360 días paga una TREA de 5.25%. [fuente: deposito_plazo.md / Tasas] |
| q15 | rag | rag | ✅ |  | 2368.5 | Si cancelas el depósito a plazo antes del plazo establecido, los intereses se recalculan con la TREA de la cue |
| q16 | rag | rag | ✅ |  | 2280.2 | Las agencias atienden los sábados de 9:00 a 13:00. [fuente: canales_y_reclamos.md / Agencias] |
| q17 | rag | rag | ✅ |  | 2333.7 | El banco responde los reclamos en un plazo máximo de 15 días hábiles. [fuente: canales_y_reclamos.md / Reclamo |
| q18 | simulator | simulator | ✅ |  | 1648.9 | Para un préstamo de S/ 10,000.00 a 12 meses con una TEA de 30% (TEM 2.21%), tu cuota mensual aproximada sería  |
| q19 | simulator | simulator | ✅ |  | 1825.0 | Para un préstamo de S/ 5,000.00 a 24 meses con una TEA de 45% (TEM 3.14%), tu cuota mensual aproximada sería S |
| q20 | handoff | handoff | ✅ |  | 822.5 | Te comunico con un asesor humano. Si se trata de cargos no reconocidos, bloquea tu tarjeta desde la app o llam |
| q21 | handoff | handoff | ✅ |  | 907.9 | Te comunico con un asesor humano. Si se trata de cargos no reconocidos, bloquea tu tarjeta desde la app o llam |
| q22 | out_of_scope | out_of_scope | ✅ |  | 829.9 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q23 | out_of_scope | out_of_scope | ✅ |  | 723.1 | Solo puedo ayudarte con temas de productos y servicios de Banco Andino. |
| q24 | blocked | blocked | ✅ |  | 3.1 | No puedo ayudarte con esa solicitud. Puedo responder dudas sobre nuestros productos y servicios. |
| q25 | rag | rag | ✅ |  | 3775.1 | La membresía anual de la Tarjeta de Crédito Andina Clásica cuesta S/ 99. Sin embargo, esta membresía se exoner |
| q26 | rag | rag | ✅ |  | 2278.1 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
| q27 | rag | rag | ✅ |  | 1974.3 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
| q28 | rag | rag | ✅ |  | 2630.2 | Si te robaron la tarjeta, bloquéala de inmediato desde la app o llamando a la línea 0800-00-123, que está disp |
| q29 | rag | rag | ✅ |  | 2356.2 | El banco nunca te pedirá tus claves ni códigos de verificación por WhatsApp, llamada o correo. Es probable que |
| q30 | clarify | clarify | ✅ |  | 842.7 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q31 | clarify | clarify | ✅ |  | 856.9 | ¿Sobre qué producto me consultas? Puedo ayudarte con: Cuenta Ahorro Andina, Depósito a Plazo Andino, Préstamo  |
| q32 | simulator | simulator | ✅ |  | 1771.2 | Revisa estos datos: el plazo en meses debe estar entre 1 y 360. |
| q33 | rag | rag | ✅ |  | 3425.1 | Bloquea tu tarjeta de inmediato desde la app o llamando a la línea 0800-00-123, que está disponible las 24 hor |
| q34 | handoff | handoff | ✅ |  | 936.6 | Te comunico con un asesor humano. Si se trata de cargos no reconocidos, bloquea tu tarjeta desde la app o llam |
| q35 | rag | rag | ✅ |  | 2650.6 | No encontré esa información en la documentación disponible. ¿Quieres que te comunique con un asesor? |
