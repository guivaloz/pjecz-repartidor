import os


class Autoridad(object):
    """ Autoridad """

    def __init__(self, config, ruta):
        self.config = config
        self.ruta = ruta
        self.nombre = ''
        self.archivos = []
        self.ya_rastreado = False

    def rastrear_archivos(self, ruta):
        """ Rastrear archivos """
        if not os.path.exists(ruta) or not os.path.isdir(ruta):
            raise Exception('No existe el directorio dado a rastrear_archivos.')
        for item in os.scandir(ruta):
            if item.is_dir(follow_symlinks=False):
                yield from self.rastrear_archivos(item.path)
            else:
                yield item

    def rastrear(self):
        """ Rastrear """
        if self.ya_rastreado is False:
            self.ya_rastreado = True
            for item in self.rastrear_archivos(self.ruta):
                self.archivos.append(item.path)

    def __repr__(self):
        archivos_repr = '\n      '.join([archivo for archivo in self.archivos])
        if self.ya_rastreado:
            return('<Autoridad> {}\n      {}'.format(self.nombre, archivos_repr))
        else:
            return('<Autoridad>')
