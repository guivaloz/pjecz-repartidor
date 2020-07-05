import os
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
            if not os.path.exists(self.ruta) or not os.path.isdir(self.ruta):
                raise Exception(f'AVISO: No existe el directorio {self.ruta}')
            for item in os.scandir(self.ruta):
                if item.is_dir(follow_symlinks=False):
                    distrito = Distrito(self.config, os.path.join(self.ruta, item.path))
                    distrito.rastrear()
                    self.distritos.append(distrito)
            self.nombre = os.path.split(self.ruta)[1]  # Nombre del directorio
            self.ya_rastreado = True

    def __repr__(self):
        distritos_repr = '\n  '.join([repr(distrito) for distrito in self.distritos])
        if self.ya_rastreado:
            return('<Deposito> {}\n  {}'.format(self.nombre, distritos_repr))
        else:
            return('<Deposito>')
