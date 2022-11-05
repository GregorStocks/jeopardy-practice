#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import RealDictCursor

def main(cur):
    cur.execute('SELECT games.id AS game_id FROM games LEFT JOIN game_attempts ON games.id = game_attempts.game_id WHERE game_attempts.id IS NULL ORDER BY games.id LIMIT 1')
    game_id = cur.fetchone()['game_id']
    print(game_id)

if __name__ == '__main__':
    with psycopg2.connect(dbname='jeopardy', user='jeopardy',password='jeopardypassword', cursor_factory=RealDictCursor) as conn:
        with conn.cursor() as cur:
            main(cur)
