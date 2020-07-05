import os
from depositos.autoridad import Autoridad


class Distrito(object):
    """ Distrito """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta
        self.nombre = ''
        self.autoridades = []
        self.ya_rastreado = False

    def rastrear(self):
        """ Rastrear """
        if self.ya_rastreado is False:
            if not os.path.exists(self.ruta) or not os.path.isdir(self.ruta):
                raise Exception(f'AVISO: No existe el directorio {self.ruta}')
            for item in os.scandir(self.ruta):
                if item.is_dir(follow_symlinks=False):
                    autoridad = Autoridad(self.config, os.path.join(self.ruta, item.path))
                    autoridad.rastrear()
                    self.autoridades.append(autoridad)
            self.nombre = os.path.split(self.ruta)[1]  # Nombre del directorio
            self.ya_rastreado = True

    def __repr__(self):
        autoridades_repr = '\n    '.join([repr(autoridad) for autoridad in self.autoridades])
        if self.ya_rastreado:
            return('<Distrito> {}\n    {}'.format(self.nombre, autoridades_repr))
        else:
            return('<Distrito>')
