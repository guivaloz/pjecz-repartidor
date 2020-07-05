from pathlib import Path


class Autoridad(object):
    """ Autoridad """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta
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
            for item in ruta.glob(patron):
                if item.is_file():
                    self.archivos.append(item)
            self.nombre = ruta.parts[-1]
            self.ya_rastreado = True

    def __repr__(self):
        archivos_repr = '\n      '.join([archivo.name for archivo in self.archivos])
        if self.ya_rastreado:
            return('<Autoridad> {}\n      {}'.format(self.nombre, archivos_repr))
        else:
            return('<Autoridad>')
