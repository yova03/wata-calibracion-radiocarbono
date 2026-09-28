---
objetivo: "Registrar la procedencia, la integridad y la cita obligatoria de las curvas de calibración usadas por wata."
uso: "Consultar antes de citar una calibración o de publicar el repositorio; los hashes permiten comprobar que el archivo no cambió."
---

# Origen de las curvas de calibración

Descargadas de <https://intcal.org/curves/> el 28 de setiembre de 2026, sin
modificaciones. `python -m wata curvas` repite la descarga si faltan y muestra
el SHA-256.

| Archivo | Curva | SHA-256 | Uso en wata |
|---|---|---|---|
| `shcal20.14c` | SHCal20, hemisferio sur | `e214d987bc4dbddfbc91c0aca4573a71db22a17c93d8bc55fa609bb58ae39b0d` | predeterminada |
| `intcal20.14c` | IntCal20, hemisferio norte | `974a66649f2ac8a53e6c99e256b019ac6982f999b12dcf7193162d4c1c09168e` | alternativa y curva mixta |
| `shcal13.14c` | SHCal13 | `86281560cdcf58765fc11fc2bc8dccacea471b4693afd81ab1e63fb23c527cb2` | solo validación |
| `intcal13.14c` | IntCal13 | `0af281d2b559143ea9230c45e3c709137d868b8dbc09abf1ad16739fdb424cbd` | solo validación |

Los archivos de 2020 tienen el mismo SHA-256 que los que distribuye IOSACal
0.7.0. A la fecha de descarga, intcal.org no lista ninguna curva posterior a
2020.

## Resolución

Entre 0 y 5000 cal BP las curvas de 2020 vienen año por año; luego, cada 5,
10 y 20 años. Las de 2013 vienen cada 5 años desde el presente. wata
interpola todas a una rejilla anual.

## Cita obligatoria

Toda calibración hecha con wata debe citar la curva:

- Hogg, A. G., Heaton, T. J., Hua, Q., Palmer, J. G., Turney, C. S. M.,
  Southon, J., Bayliss, A., Blackwell, P. G., Boswijk, G., Bronk Ramsey, C.,
  Pearson, C., Petchey, F., Reimer, P., Reimer, R. y Wacker, L. (2020).
  SHCal20 Southern Hemisphere calibration, 0–55,000 years cal BP.
  *Radiocarbon, 62*(4), 759–778. https://doi.org/10.1017/RDC.2020.59
- Reimer, P., Austin, W. E. N., Bard, E., Bayliss, A., Blackwell, P. G.,
  Bronk Ramsey, C., Butzin, M., Cheng, H., Edwards, R. L., Friedrich, M.,
  Grootes, P. M., Guilderson, T. P., Hajdas, I., Heaton, T. J., Hogg, A. G.,
  Hughen, K. A., Kromer, B., Manning, S. W., Muscheler, R., … Talamo, S.
  (2020). The IntCal20 Northern Hemisphere radiocarbon age calibration curve
  (0–55 cal kBP). *Radiocarbon, 62*(4), 725–757.
  https://doi.org/10.1017/RDC.2020.41

Autores, títulos y DOI proceden del encabezado de cada archivo `.14c`; el
volumen y las páginas, de la revista.

## Condiciones de redistribución

intcal.org no publica términos de uso explícitos para los archivos `.14c`.
OxCal declara que los incluye «with the kind permission of the compilers»;
IOSACal (GPL-3) y el paquete R `rintcal` (CRAN) los redistribuyen. Antes de
hacer público el repositorio conviene decidir entre incluir los archivos con
su cita o dejar que `python -m wata curvas` los descargue en cada instalación.
