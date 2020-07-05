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
            for item in ruta.glob(patron):
                if item.is_dir():
                    distrito = Distrito(self.config, str(item))
                    distrito.rastrear()
                    self.distritos.append(distrito)
            self.nombre = ruta.parts[-1]
            self.ya_rastreado = True

    def __repr__(self):
        distritos_repr = '\n  '.join([repr(distrito) for distrito in self.distritos])
        if self.ya_rastreado:
            return('<Deposito> {}\n  {}'.format(self.nombre, distritos_repr))
        else:
            return('<Deposito>')
