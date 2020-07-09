from datetime import datetime


class Base(object):
    """ Base """

    def separar_fecha_descripcion(self, archivo, distrito=None, autoridad=None):
        separados = archivo.name.split('-')
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
        if len(separados) >= 4:
            descripcion = ' '.join(separados[3:])
        else:
            descripcion = ''
        renglon = {'fecha': fecha, 'descripcion': descripcion, 'archivo': archivo.name}
        if distrito is not None:
            renglon['distrito'] = distrito.nombre
        if autoridad is not None:
            renglon['autoridad'] = autoridad.nombre
        return(renglon)

    def separar_fecha_expediente_descripcion(self, archivo, distrito=None, autoridad=None):
        separados = archivo.name.split('-')
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
        if len(separados) >= 5:
            expediente = f'{separados[3]}-{separados[4]}'
        else:
            expediente = ''
        if len(separados) >= 6:
            descripcion = ' '.join(separados[5:])
        else:
            descripcion = ''
        renglon = {'fecha': fecha, 'expediente': expediente, 'descripcion': descripcion, 'archivo': archivo.name}
        if distrito is not None:
            renglon['distrito'] = distrito.nombre
        if autoridad is not None:
            renglon['autoridad'] = autoridad.nombre
        return(renglon)

    def separar_fecha_sentencia_expediente_genero_descripcion(self, archivo, distrito=None, autoridad=None):
        separados = archivo.name.split('-')
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
        if len(separados) >= 5:
            sentencia = f'{separados[3]}-{separados[4]}'
        else:
            sentencia = ''
        if len(separados) >= 7:
            expediente = f'{separados[5]}-{separados[6]}'
        else:
            expediente = ''
        if len(separados) >= 8 and separados[7].lower() == 'g':
            p_genero = 'Sí'
        else:
            p_genero = 'No'
        renglon = {'fecha': fecha, 'sentencia': sentencia, 'expediente': expediente, 'genero': p_genero, 'archivo': archivo.name}
        if distrito is not None:
            renglon['distrito'] = distrito.nombre
        if autoridad is not None:
            renglon['autoridad'] = autoridad.nombre
        return(renglon)

    def guardar_json(self):
        ruta = self.crear_ruta_json()
        padre_dir = ruta.parent
        if not padre_dir.exists():
            padre_dir.mkdir(parents=True)
        with open(ruta, 'w') as puntero:
            puntero.write(self.crear_contenido_json())
        return(str(ruta))
