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


@cli.command()
@pass_config
def guardar_json_por_autoridad(config):
    """ Guardar archivos JSON por autoridad """
    click.echo('Voy a guardar archivos JSON por autoridad...')
    deposito = Deposito(config, config.deposito_ruta)
    deposito.rastrear()
    for distrito in deposito.distritos:
        distrito.rastrear()
        for autoridad in distrito.autoridades:
            autoridad.rastrear()
            click.echo(autoridad.guardar_json())
    sys.exit(0)


@cli.command()
@pass_config
def guardar_json_por_fecha(config):
    """ Guardar archivos JSON para la fecha dada """
    click.echo('Voy a guardar archivos JSON por fecha...')
    deposito = Deposito(config, config.deposito_ruta)
    deposito.rastrear()
    click.echo(deposito.guardar_json())
    sys.exit(0)


@cli.command()
@pass_config
def guardar_json_reporte_distritos(config):
    """ Guardar archivos JSON con reportes de los distritos """
    click.echo('Voy a guardar archivos JSON con reportes de los distritos...')
    deposito = Deposito(config, config.deposito_ruta)
    deposito.rastrear()
    click.echo(deposito.guardar_json_reporte_distritos())
    sys.exit(0)


@cli.command()
@pass_config
def guardar_json_reporte_autoridades(config):
    """ Guardar archivos JSON con reportes de las autoridades """
    click.echo('Voy a guardar archivos JSON con reportes de las autoridades...')
    deposito = Deposito(config, config.deposito_ruta)
    deposito.rastrear()
    for distrito in deposito.distritos:
        distrito.rastrear()
        click.echo(distrito.guardar_json_reporte_autoridades())
    sys.exit(0)


cli.add_command(rastrear)
cli.add_command(guardar_json_por_autoridad)
cli.add_command(guardar_json_por_fecha)
cli.add_command(guardar_json_reporte_distritos)
cli.add_command(guardar_json_reporte_autoridades)
