"""
Autoridad
"""
import json
from pathlib import Path
from comunes.funciones import cambiar_texto_a_identificador
from depositos.base import Base


class Autoridad(Base):
    """ Autoridad """

    def __init__(self, config, ruta, distrito_nombre):
        super().__init__(config, ruta)
        self.distrito_nombre = distrito_nombre
        self.nombre = ''
        self.archivos = []  # Lista de PosixPath
        self.ya_rastreado = False

    def rastrear(self):
        """ Rastrear """
        if self.ya_rastreado is False:
            ruta = Path(self.ruta)
            if not ruta.exists() or not ruta.is_dir():
                raise Exception(f'AVISO: No existe el directorio {self.ruta}')
            if self.config.fecha == '':
                patron = '**/*.pdf'
            else:
                patron = f'**/{self.config.fecha}*'
            self.nombre = ruta.parts[-1]
            for item in ruta.glob(patron):
                if item.is_file() and item.suffix.lower() == '.pdf':  # Solo archivos PDF
                    self.archivos.append(item)
            self.ya_rastreado = True

    def crear_completo_ruta(self):
        """ Crear la ruta al archivo JSON /var/www/html/consultas/v2.0/<RAMA>/<DISTRITO>/<AUTORIDAD>.json """
        return Path(
            self.config.servidor_json_ruta,
            cambiar_texto_a_identificador(self.distrito_nombre),
            cambiar_texto_a_identificador(self.nombre) + '.json',
        )

    def crear_completo_contenido(self):
        """ Crear el contenido JSON """
        if self.ya_rastreado is False:
            self.rastrear()
        if len(self.archivos) == 0:
            return(json.dumps({'data': []}))  # No se encontraron archivos
        if self.config.metadatos_partes == 'fecha_descripcion':
            funcion = self.separar_fecha_descripcion
        elif self.config.metadatos_partes == 'fecha_expediente_descripcion':
            funcion = self.separar_fecha_expediente_descripcion
        elif self.config.metadatos_partes == 'fecha_sentencia_expediente_genero_descripcion':
            funcion = self.separar_fecha_sentencia_expediente_genero_descripcion
        else:
            raise Exception(f'AVISO: Mal configurado, no está programado {self.config.metadatos_partes}')
        listado = [funcion(archivo) for archivo in self.archivos]
        titulo = f'Reporte por autoridad de {self.config.rama}'
        return json.dumps({'titulo': titulo, 'elaborado': self.config.ahora_str, 'data': listado})

    def guardar_completo(self):
        """ Guardar JSON """
        return self.guardar(
            self.crear_completo_ruta(),
            self.crear_completo_contenido(),
        )

    def __repr__(self):
        archivos_repr = '\n      '.join([archivo.name for archivo in self.archivos])
        if self.ya_rastreado:
            if len(self.archivos) > 0:
                return '<Autoridad> {}\n      {}'.format(self.nombre, archivos_repr)
            else:
                return '<Autoridad> No se encontraron archivos'
        return '<Autoridad>'
