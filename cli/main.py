#!/usr/bin/env python3

import psycopg2

def main(cur: bool):
    print('main')

if __name__ == '__main__':
    with psycopg2.connect(dbname='jeopardy', user='jeopardy',password='jeopardypassword') as conn:
        with conn.cursor() as cur:
            main(cur)
