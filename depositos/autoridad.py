import json
from pathlib import Path
from comunes.funciones import cambiar_texto_a_identificador


class Autoridad(object):
    """ Autoridad """

    def __init__(self, config, ruta, distrito_nombre):
        self.config = config
        self.ruta = ruta
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
                patron = '**/*'
            else:
                patron = f'**/{self.config.fecha}*'
            self.nombre = ruta.parts[-1]
            for item in ruta.glob(patron):
                if item.is_file():
                    self.archivos.append(item)
            self.ya_rastreado = True

    def separar_fecha_descripcion(self, archivo):
        separados = archivo.name.split('-')
        if len(separados) >= 3:
            fecha = f'{separados[0]}-{separados[1]}-{separados[2]}'
        else:
            fecha = self.config.fecha_por_defecto
        if len(separados) >= 4:
            descripcion = ' '.join(separados[3:])
        else:
            descripcion = ''
        return({'fecha': fecha, 'descripcion': descripcion, 'archivo': archivo.name})

    def separar_fecha_expediente_descripcion(self, archivo):
        return({})

    def separar_fecha_sentencia_expediente_genero_descripcion(self, archivo):
        return({})

    def crear_ruta_json(self):
        """ Crear la ruta al archivo JSON /var/www/html/consultas/v2.0/<RAMA>/<DISTRITO>/<AUTORIDAD>.json """
        return(Path(
            self.config.servidor_json_ruta,
            cambiar_texto_a_identificador(self.distrito_nombre),
            cambiar_texto_a_identificador(self.nombre) + '.json',
        ))

    def crear_contenido_json(self):
        """ Crear el contenido JSON """
        if self.ya_rastreado is False:
            self.rastrear()
        if len(self.archivos) == 0:
            raise Exception('AVISO: No se encontraron archivos.')
        if self.config.metadatos_partes == 'fecha_descripcion':
            funcion = self.separar_fecha_descripcion
        elif self.config.metadatos_partes == 'fecha_expediente_descripcion':
            funcion = self.separar_fecha_expediente_descripcion
        elif self.config.metadatos_partes == 'fecha_sentencia_expediente_genero_descripcion':
            funcion = self.separar_fecha_sentencia_expediente_genero_descripcion
        else:
            raise Exception(f'AVISO: Mal configurado, no está programado {self.config.metadatos_partes}')
        listado = [funcion(archivo) for archivo in self.archivos]
        salida = {'data': listado}
        return(json.dumps(salida))

    def guardar_json(self):
        ruta = self.crear_ruta_json()
        padre_dir = ruta.parent
        if not padre_dir.exists():
            padre_dir.mkdir(parents=True)
        with open(ruta, 'w') as puntero:
            puntero.write(self.crear_contenido_json())
        return(str(ruta))

    def __repr__(self):
        archivos_repr = '\n      '.join([archivo.name for archivo in self.archivos])
        if self.ya_rastreado:
            return('<Autoridad> {}\n      {}'.format(self.nombre, archivos_repr))
        else:
            return('<Autoridad>')
