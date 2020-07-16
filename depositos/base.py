from datetime import datetime
from pathlib import Path
from urllib.parse import quote


class Base(object):
    """ Base """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta

    def crear_google_storage_url(self, archivo):
        """ Crear URL a Google Starage """
        archivo_relativa_ruta = str(archivo)[len(self.config.deposito_ruta):]
        url = quote(self.config.google_storage_url + archivo_relativa_ruta, safe=':/')
        return(url)

    def separar_fecha_descripcion(self, archivo, distrito=None, autoridad=None):
        """ Separar fecha y descripción, entrega diccionario con el renglón """
        separados = archivo.stem.split('-')
        # Fecha
        if len(separados) >= 3:
            try:
                ano = int(separados[0][0:4])
                mes = int(separados[1][0:2])
                dia = int(separados[2][0:2])
                fecha = '{}-{}-{}'.format(str(ano).zfill(4), str(mes).zfill(2), str(dia).zfill(2))
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                fecha = self.config.fecha_por_defecto
        else:
            fecha = self.config.fecha_por_defecto
        # Descripción
        if len(separados) >= 4:
            descripcion = ' '.join(separados[3:]).title()
        else:
            descripcion = ''
        # Renglón
        renglon = {
            'fecha': fecha,
            'descripcion': descripcion,
            'archivo': self.crear_google_storage_url(archivo),
        }
        if distrito is not None:
            renglon['distrito'] = distrito.nombre
        if autoridad is not None:
            renglon['autoridad'] = autoridad.nombre
        return(renglon)

    def separar_fecha_expediente_descripcion(self, archivo, distrito=None, autoridad=None):
        """ Separar fecha, expediente y descripción, entrega diccionario con el renglón """
        separados = archivo.stem.split('-')
        # Fecha
        if len(separados) >= 3:
            try:
                ano = int(separados[0][0:4])
                mes = int(separados[1][0:2])
                dia = int(separados[2][0:2])
                fecha = '{}-{}-{}'.format(str(ano).zfill(4), str(mes).zfill(2), str(dia).zfill(2))
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                fecha = self.config.fecha_por_defecto
        else:
            fecha = self.config.fecha_por_defecto
        # Expediente
        if len(separados) >= 5:
            expediente = f'{separados[3]}-{separados[4]}'
        else:
            expediente = ''
        # Descripción
        if len(separados) >= 6:
            descripcion = ' '.join(separados[5:]).title()
        else:
            descripcion = ''
        # Renglón
        renglon = {
            'fecha': fecha,
            'expediente': expediente,
            'descripcion': descripcion,
            'archivo': self.crear_google_storage_url(archivo),
        }
        if distrito is not None:
            renglon['distrito'] = distrito.nombre
        if autoridad is not None:
            renglon['autoridad'] = autoridad.nombre
        return(renglon)

    def separar_fecha_sentencia_expediente_genero_descripcion(self, archivo, distrito=None, autoridad=None):
        """ Separar fecha, sentencia, expediente y género, entrega diccionario con el renglón """
        separados = archivo.stem.split('-')
        # Fecha
        if len(separados) >= 3:
            try:
                ano = int(separados[0][0:4])
                mes = int(separados[1][0:2])
                dia = int(separados[2][0:2])
                fecha = '{}-{}-{}'.format(str(ano).zfill(4), str(mes).zfill(2), str(dia).zfill(2))
                datetime.strptime(fecha, '%Y-%m-%d')
            except ValueError:
                fecha = self.config.fecha_por_defecto
        else:
            fecha = self.config.fecha_por_defecto
        # Sentencia
        if len(separados) >= 5:
            sentencia = f'{separados[3]}-{separados[4]}'
        else:
            sentencia = ''
        # Expediente
        if len(separados) >= 7:
            expediente = f'{separados[5]}-{separados[6]}'
        else:
            expediente = ''
        # Género
        if len(separados) >= 8 and separados[7].lower() == 'g':
            p_genero = 'Sí'
        else:
            p_genero = 'No'
        # Renglón
        renglon = {
            'fecha': fecha,
            'sentencia': sentencia,
            'expediente': expediente,
            'genero': p_genero,
            'archivo': self.crear_google_storage_url(archivo),
        }
        if distrito is not None:
            renglon['distrito'] = distrito.nombre
        if autoridad is not None:
            renglon['autoridad'] = autoridad.nombre
        return(renglon)

    def guardar(self, ruta, contenido):
        """ Guardar archivo JSON, requiere la ruta como Path y el contenido como texto, entrega la ruta como texto """
        if not isinstance(ruta, Path):
            raise Exception('ERROR: Al guardar la ruta no es instancia de Path.')
        if not isinstance(contenido, str):
            raise Exception('ERROR: Al guardar el contenido no es texto.')
        padre_dir = ruta.parent
        if not padre_dir.exists():
            padre_dir.mkdir(parents=True)
        with open(ruta, 'w') as puntero:
            puntero.write(contenido)
        return(str(ruta))
