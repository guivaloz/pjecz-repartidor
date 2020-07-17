import json
from datetime import datetime
from pathlib import Path
from depositos.base import Base
from depositos.distrito import Distrito


class Deposito(Base):
    """ Depósito """

    def __init__(self, config, ruta):
        super().__init__(config, ruta)
        self.nombre = ''
        self.distritos = []
        self.ya_rastreado = False

    def rastrear(self):
        """ Rastrear """
        if self.ya_rastreado is False:
            ruta = Path(self.ruta)
            if not ruta.exists() or not ruta.is_dir():
                raise Exception(f'AVISO: No existe el directorio {self.ruta}')
            if self.config.distrito == '':
                patron = '*'
            else:
                patron = f'{self.config.distrito}*'
            self.nombre = ruta.parts[-1]
            for item in ruta.glob(patron):
                if item.is_dir():
                    distrito = Distrito(self.config, str(item))
                    distrito.rastrear()
                    self.distritos.append(distrito)
            self.ya_rastreado = True

    def crear_diario_ruta(self):
        """ Crear la ruta al archivo JSON /var/www/html/consultas/v2.0/<RAMA>/<AAAA-MM-DD>.json """
        if self.config.fecha == '':
            raise Exception('AVISO: Falta la fecha.')
        return(Path(
            self.config.servidor_json_ruta,
            self.config.fecha + '.json',
        ))

    def crear_diario_contenido(self):
        """ Crear el contenido JSON """
        if self.config.fecha == '':
            raise Exception('AVISO: Falta la fecha.')
        if self.ya_rastreado is False:
            self.rastrear()
        if self.config.metadatos_partes == 'fecha_descripcion':
            funcion = self.separar_fecha_descripcion
        elif self.config.metadatos_partes == 'fecha_expediente_descripcion':
            funcion = self.separar_fecha_expediente_descripcion
        elif self.config.metadatos_partes == 'fecha_sentencia_expediente_genero_descripcion':
            funcion = self.separar_fecha_sentencia_expediente_genero_descripcion
        else:
            raise Exception(f'AVISO: Mal configurado, no está programado {self.config.metadatos_partes}')
        listado = []
        for distrito in self.distritos:
            distrito.rastrear()
            for autoridad in distrito.autoridades:
                autoridad.rastrear()
                listado += [funcion(archivo, distrito=distrito, autoridad=autoridad) for archivo in autoridad.archivos]
        salida = {'data': listado}
        return(json.dumps(salida))

    def guardar_diario(self):
        """ Guardar JSON """
        return(self.guardar(
            self.crear_diario_ruta(),
            self.crear_diario_contenido(),
        ))

    def crear_reporte_ruta(self, sufijo):
        """ Crear la ruta al archivo JSON para el reporte """
        if self.config.fecha == '':
            if sufijo == '':
                nombre = f'reporte.json'
            else:
                nombre = f'reporte-{sufijo}.json'
        else:
            if sufijo == '':
                nombre = f'reporte-{self.config.fecha}.json'
            else:
                nombre = f'reporte-{self.config.fecha}-{sufijo}.json'
        return(Path(
            self.config.servidor_json_ruta,
            nombre,
        ))

    def crear_reporte_contenido(self):
        """ Crear el contenido JSON para el reporte """
        if self.ya_rastreado is False:
            self.rastrear()
        listado = []
        if self.config.fecha == '':
            # Sin fecha
            for distrito in self.distritos:
                for autoridad in distrito.autoridades:
                    listado.append({
                        'distrito': distrito.nombre,
                        'autoridad': autoridad.nombre,
                    })
        else:
            # Con fecha
            for distrito in self.distritos:
                for autoridad in distrito.autoridades:
                    if len(autoridad.archivos) == 0:
                        listado.append({
                            'distrito': distrito.nombre,
                            'autoridad': autoridad.nombre,
                            'entrega': 'Pendiente',
                            'cuando': 'ND',
                            'archivo': 'ND',
                            'descargar': 'ND',
                        })
                    else:
                        for archivo in autoridad.archivos:
                            ts = datetime.fromtimestamp(archivo.stat().st_mtime)
                            listado.append({
                                'distrito': distrito.nombre,
                                'autoridad': autoridad.nombre,
                                'entrega': 'Entregado',
                                'cuando': ts.strftime('%Y-%m-%d %H:%M'),
                                'archivo': archivo.name,
                                'descargar': self.crear_google_storage_url(archivo),
                            })
        return(json.dumps({'data': listado}))

    def guardar_reporte(self, sufijo):
        """ Guardar JSON para el reporte """
        return(self.guardar(
            self.crear_reporte_ruta(sufijo),
            self.crear_reporte_contenido(),
        ))

    def __repr__(self):
        distritos_repr = '\n  '.join([repr(distrito) for distrito in self.distritos])
        if self.ya_rastreado:
            return('<Deposito> {}\n  {}'.format(self.nombre, distritos_repr))
        else:
            return('<Deposito>')
