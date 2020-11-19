from sqlalchemy.engine.url import URL

import database_tools
from bot import config

# This script can be used to reset the db from a provided csv
# It depends on a lot more than is obvious so run inside docker container
# You can run the script from inside the container using `docker exec <container pid> python3 reset_from_csv.py`
# Or enter the container using `docker-compose run bot bash` and then execute `python3 reset_from_csv.py`
# Warning, the previous DB is not recoverable if you try this

eng = database_tools.engine(config.postgres_url or URL(**config.postgres_params))
database_tools._csv_to_sql('aliases', eng, 'alias')
df = database_tools.sql_to_df('aliases', eng, 'alias')
print(df)