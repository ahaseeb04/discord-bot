import postgres

# This script can be used to reset the db from a provided csv
# It depends on a lot more than is obvious so run inside docker container
# You can enter the container running `docker-compose run bot bash`
# Warning, the previous DB is not recoverable if you try this

eng = postgres.connect()
postgres._csv_to_sql(eng)
df = postgres.sql_to_df(eng)
print(df)