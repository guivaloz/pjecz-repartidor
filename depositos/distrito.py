"""
Distrito
"""
import json
from pathlib import Path
from comunes.funciones import cambiar_texto_a_identificador
from depositos.base import Base
from depositos.autoridad import Autoridad


class Distrito(Base):
    """ Distrito """

    def __init__(self, config, ruta):
        super().__init__(config, ruta)
        self.nombre = ''
        self.autoridades = []
        self.ya_rastreado = False

    def rastrear(self):
        """ Rastrear """
        if self.ya_rastreado is False:
            ruta = Path(self.ruta)
            if not ruta.exists() or not ruta.is_dir():
                raise Exception(f'AVISO: No existe el directorio {self.ruta}')
            if self.config.autoridad == '':
                patron = '*'
            else:
                patron = f'{self.config.autoridad}*'
            self.nombre = ruta.parts[-1]
            for item in ruta.glob(patron):
                if item.is_dir():
                    autoridad = Autoridad(self.config, str(item), self.nombre)
                    autoridad.rastrear()
                    self.autoridades.append(autoridad)
            self.ya_rastreado = True

    def crear_reporte_ruta(self):
        """ Crear la ruta al archivo JSON para el reporte """
        return(Path(
            self.config.servidor_json_ruta,
            cambiar_texto_a_identificador(self.nombre),
            'reporte.json',
        ))

    def crear_reporte_contenido(self):
        if self.ya_rastreado is False:
            self.rastrear()
        listado = []
        for autoridad in self.autoridades:
            listado.append({'distrito': self.nombre, 'autoridad': autoridad.nombre})
        titulo = f'Reporte por distrito de {self.config.rama}'
        return(json.dumps({'titulo': titulo, 'elaborado': self.config.ahora_str, 'data': listado}))

    def guardar_reporte(self):
        """ Guardar JSON para el reporte """
        return(self.guardar(
            self.crear_reporte_ruta(),
            self.crear_reporte_contenido(),
        ))

    def __repr__(self):
        autoridades_repr = '\n    '.join([repr(autoridad) for autoridad in self.autoridades])
        if self.ya_rastreado:
            return('<Distrito> {}\n    {}'.format(self.nombre, autoridades_repr))
        else:
            return('<Distrito>')
