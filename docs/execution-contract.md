# Contrato propuesto: evidencia de ejecución

Formato genérico `0.1` propuesto para SalvaOps. No acredita que exista una API, un motor de aprobaciones o una exportación implementada.

[JSON Schema](../schemas/execution-evidence.schema.json) · [Ejemplo ficticio](../examples/execution-evidence.json)

## Modelo

Una ejecución conecta proyecto, tarea, objetivo, restricciones, tipo de actor, estado, decisión de aprobación y resultado. Estados: `planned`, `running`, `succeeded`, `failed`, `blocked`, `cancelled`.

El schema rechaza campos no previstos; credenciales, rutas locales y logs privados no tienen lugar en este manifiesto público. Esto no sustituye revisión de textos y URLs: esos campos pueden contener información sensible aunque cumplan el schema.

Una ejecución `succeeded` requiere resultado y al menos una validación con estado `passed`; todas las validaciones declaradas deben haber pasado. Si requiere aprobación, esta debe estar `approved` y aportar `reference_url`. El schema no valida que quien aprobó tuviera autoridad ni que la decisión precediera a la ejecución; eso requiere control de aplicación.

## Validación local

Python 3.10+ y entorno virtual recomendado:

```sh
python -m venv .venv
# Activar el entorno según el sistema operativo.
python -m pip install -r requirements-validation.txt
python -m unittest discover -s tests -v
```

Pruebas: Draft 2020-12, ejemplo válido, campos de credenciales rechazados, estados inválidos, éxito sin resultado, aprobación pendiente o sin referencia y fechas inválidas. CI ejecuta estas pruebas además del checker de documentos.

## Límites y decisiones pendientes

- No hay verificación criptográfica, lectura de URLs ni validación de resultados reales.
- Orden de fechas, transiciones permitidas, identidad del actor, autorización, retención y correlación de IDs requieren reglas de aplicación.
- `example.com` es un dominio reservado para documentación. Ejemplo completamente ficticio, sin acceso a proyectos o integraciones reales.
- El estado de aprobación representa una decisión declarada; no autoriza acciones por sí mismo.

[Contexto del producto](overview.md) · [Hoja de ruta](roadmap.md)
