# pjecz-repartidor

Repartir los documentos van a ser públicos: A partir de documentos que se van a cargar a Google Storage crea archivos JSON como insumos para las consultas; una forma de publicar consultas está en sitio web programado en JavaScript.

## Ayuda

Ejecute

    $ repartidor --help

## Guardar completos

    $ repartidor --rama acuerdos guardar-completos

## Por programar estos estatus en los reportes de las Listas de Acuerdos

- El color verde indica que la lista fue subida el mismo día que fue generada y antes de las 15:00 horas.
- El color amarillo indica las listas de acuerdo que fueron subidas después de las 15:00 horas del día indicado.
- El color naranja indica las listas de acuerdo subidas después de la fecha de la lista correspondiente.
- El color rojo indica las listas de acuerdos no subidas en la fecha indicada. (No existe archivo)
