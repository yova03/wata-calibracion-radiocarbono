---
objetivo: "Orientar la preparación del depósito completo de la investigación 06 en Zenodo."
uso: "Leer el dictamen, completar metadatos y revisar el ZIP antes de subirlo."
---

# Depósito Zenodo: investigación completa

**Estado:** borrador local. No hay registro publicado ni DOI reservado.

- [Dictamen de revisión](../REVISION_ZENODO_2026-09-28.md).
- [Metadatos propuestos](./metadatos_borrador.md).
- [Fuentes sin enlace institucional](../02_datos/fechados/FUENTES_SIN_ENLACE.md).
- `preparar_archivo.py`: crea un ZIP para depósito con código, datos depurados,
  informes y figuras. Excluye el historial Git, cachés, versiones retiradas,
  archivos de curvas de terceros y la columna de extractos textuales del CSV.

La autoría, el ORCID y las licencias están documentados. El ZIP está preparado
para revisión del depósito; el dictamen distingue sus límites científicos y
las fuentes que aún carecen de enlace público.

**Archivo preparado:** `borrador/investigacion_cusco_wata_v0.1.0_DEPOSITO.zip`
(1 578 402 bytes; SHA-256:
`a6c2e484fc16614e369d60fdfbe7854b090b149979be13ba3a868b1aab34e381`).

## Registro manual en Zenodo

1. Crear un registro nuevo de tipo **Software** y usar los
   [metadatos propuestos](./metadatos_borrador.md).
2. Subir `borrador/investigacion_cusco_wata_v0.1.0_DEPOSITO.zip` y revisar
   el nombre, el tamaño y el manifiesto del archivo. Indicar MIT para el código
   propio y CC BY 4.0 para los materiales propios restantes.
3. Confirmar que la descripción conserva el aviso sobre Batán Urqu y que el
   creador es Daril Yovani Cabrera Huaycochea con su ORCID. Publicar el
   registro para registrar el DOI; copiar después el DOI a este proyecto.
