from pathlib import Path
from depositos.base import Base
from depositos.autoridad import Autoridad


class Distrito(Base):
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

    def __repr__(self):
        autoridades_repr = '\n    '.join([repr(autoridad) for autoridad in self.autoridades])
        if self.ya_rastreado:
            return('<Distrito> {}\n    {}'.format(self.nombre, autoridades_repr))
        else:
            return('<Distrito>')
