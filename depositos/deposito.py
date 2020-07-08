import json
from pathlib import Path
from depositos.distrito import Distrito


class Deposito(object):
    """ Depósito """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta
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

    def separar_fecha_descripcion(self, distrito, autoridad, archivo):
        separados = archivo.name.split('-')
        if len(separados) >= 3:
            fecha = f'{separados[0]}-{separados[1]}-{separados[2]}'
        else:
            fecha = self.config.fecha_por_defecto
        if len(separados) >= 4:
            descripcion = ' '.join(separados[3:])
        else:
            descripcion = ''
        return({'distrito': distrito.nombre, 'autoridad': autoridad.nombre, 'fecha:': fecha, 'descripcion:': descripcion, 'archivo': archivo.name})

    def separar_fecha_expediente_descripcion(self, distrito, autoridad, archivo):
        return({})

    def separar_fecha_sentencia_expediente_genero_descripcion(self, distrito, autoridad, archivo):
        return({})

    def crear_ruta_json(self):
        """ Crear la ruta al archivo JSON /var/www/html/consultas/v2.0/<RAMA>/<AAAA-MM-DD>.json """
        if self.config.fecha == '':
            raise Exception('AVISO: Falta la fecha para guardar el JSON como AAAA-MM-DD.json')
        return(Path(
            self.config.servidor_json_ruta,
            self.config.fecha + '.json',
        ))

    def crear_contenido_json(self):
        """ Crear el contenido JSON """
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
                listado += [funcion(distrito, autoridad, archivo) for archivo in autoridad.archivos]
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
        distritos_repr = '\n  '.join([repr(distrito) for distrito in self.distritos])
        if self.ya_rastreado:
            return('<Deposito> {}\n  {}'.format(self.nombre, distritos_repr))
        else:
            return('<Deposito>')
