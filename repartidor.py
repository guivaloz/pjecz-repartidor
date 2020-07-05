import click
import sys
from comunes.config import pass_config
from comunes.funciones import validar_autoridad, validar_distrito, validar_fecha, validar_rama
from depositos.deposito import Deposito


@click.group()
@click.option('--rama', default='', type=str, help='Acuerdos, Edictos, EdictosJuzgados o Sentencias')
@click.option('--distrito', default='', type=str, help='Filtro por Distrito')
@click.option('--autoridad', default='', type=str, help='Filtro por Autoridad')
@click.option('--fecha', default='', type=str, help='Filtro por Fecha')
@pass_config
def cli(config, rama, distrito, autoridad, fecha):
    """ Repartir los documentos van a ser públicos """
    click.echo('Hola, ¡soy Repartidor!')
    try:
        config.rama = validar_rama(rama)
        config.distrito = validar_distrito(distrito)
        config.autoridad = validar_autoridad(autoridad)
        config.fecha = validar_fecha(fecha)
        config.cargar_configuraciones()
    except Exception as e:
        click.echo(str(e))
        sys.exit(1)


@cli.command()
@pass_config
def rastrear(config):
    """ Rastrear """
    click.echo('Voy a rastrear...')
    deposito = Deposito(config, config.deposito_ruta)
    deposito.rastrear()
    click.echo(repr(deposito))
    sys.exit(0)


cli.add_command(rastrear)
