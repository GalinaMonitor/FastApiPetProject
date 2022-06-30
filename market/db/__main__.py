"""
Утилита для управления состоянием базы данных, обертка над alembic.
Можно вызывать из любой директории, а также указать произвольный DSN для базы
данных, отличный от указанного в файле alembic.ini.
"""
import argparse
import logging
import os

from alembic.config import CommandLine

from market.utils.pg import make_alembic_config
from market.settings import settings


def main():
	logging.basicConfig(level=logging.DEBUG)

	alembic = CommandLine()
	alembic.parser.formatter_class = argparse.ArgumentDefaultsHelpFormatter
	alembic.parser.add_argument(
		'--pg-url', default=os.getenv('DATABASE_URL', settings.database_url),
		help='Database URL [env var: DATABASE_URL]'
	)

	options = alembic.parser.parse_args()
	if 'cmd' not in options:
		alembic.parser.error('too few arguments')
		exit(128)
	else:
		config = make_alembic_config(options)
		exit(alembic.run_cmd(config, options))


if __name__ == '__main__':
	main()
