import click
from main import main as run_scraper
from ingestion import ingest
from analysis import main as run_analysis

@click.group()
def cli(): pass

@cli.command()
def scrape():
    """Captura raw JSONL"""
    run_scraper()

@cli.command()
@click.option('--raw-file','-r', default='raw_365scores.jsonl')
@click.option('--db-url','-d', default='sqlite:///bets.db')
def ingest_cmd(raw_file, db_url):
    """Ingesta raw a la DB"""
    ingest(raw_file=raw_file, db_url=db_url)

@cli.command()
def analyze():
    """Ejecuta análisis de value bets"""
    run_analysis()

@cli.command()
def run_pipeline():
    """Scrape → Ingest → Analyze"""
    run_scraper()
    ingest(raw_file='raw_365scores.jsonl', db_url='sqlite:///bets.db')
    run_analysis()

if __name__=='__main__':
    cli()