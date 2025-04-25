# Bitácora de Desarrollo – SATORI.404

**Fecha:** 2025-04-25

## Avances Técnicos

- Implementación de sistema base de templates en Django (`base.html`, `index.html`).
- Incorporación de estructura HTML con `header`, `nav`, `main` y `footer`.
- Estilización con CSS modular (`base.css`) y paleta oscura con gradientes dinámicos en la barra de navegación.
- Diseño e integración de navegación superior con enlaces: Manifiesto, Sistema, Experimentación, Instalación, Documentación.
- Inclusión de animación `glitchTitle` en el encabezado principal con transición visual entre variantes del título.
- Montaje de archivos estáticos mediante volúmenes en Docker (`static`, `staticfiles`) y verificación de rutas.

## Correcciones

- Se eliminó importación incorrecta (`request` desde `shortcuts`) en `views.py`.
- Se solucionó error 404 en carga de `base.css` ajustando volúmenes en `docker-compose.yml`.

## Próximos Pasos

- Mejorar sincronización de animaciones en `h1` para representar transiciones semánticas ("satori 404" ⇄ "SATORI.404").
- Implementar nodos funcionales (`morfeo_video_club`, `bitácora`, `R2D2`) como secciones integradas en la plantilla.
- Añadir soporte responsive y diseño de menú colapsable para dispositivos móviles.
