#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from bs4 import BeautifulSoup
from glob import glob

import argparse
import os
import re
import psycopg2
from psycopg2.extras import RealDictCursor
import sys


def main_parser(args):
    """Loop thru all the games and parse them."""
    if not os.path.isdir(args.dir):
        print("The specified folder is not a directory.")
        sys.exit(1)
    NUMBER_OF_FILES = args.num_of_files or len(os.listdir(args.dir))
    print("Parsing", NUMBER_OF_FILES, "files")
    with psycopg2.connect(
        dbname="jeopardy",
        user="jeopardy",
        password="jeopardypassword",
        cursor_factory=RealDictCursor,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM games")
            already_loaded = set(f["id"] for f in cur.fetchall())
            for i, file_name in enumerate(glob(os.path.join(args.dir, "*.html")), 1):
                gid = os.path.splitext(os.path.basename(file_name))[0]
                if int(gid) in already_loaded:
                    continue

                with open(os.path.abspath(file_name)) as f:
                    percentage_done = "{:.1}".format(float(i) / float(NUMBER_OF_FILES))
                    sys.stdout.write(
                        f"\r {percentage_done}% done (processing {file_name})"
                    )
                    sys.stdout.flush()
                    parse_game(f, cur, int(gid))
                    conn.commit()
    print("\nAll done")


def parse_game(f, cur, gid):
    """Parses an entire Jeopardy! game and extract individual clues."""
    bsoup = BeautifulSoup(f, "lxml")
    # The title is in the format: `J! Archive - Show #XXXX, aired 2004-09-16`,
    # where the last part is all that is required
    airdate = bsoup.title.get_text().split()[-1]

    game_comments = bsoup.find("div", id="game_comments")
    game_comments = game_comments.get_text() if game_comments else ""
    if "Teen Tournament" in game_comments:
        game_type = "teen_tournament"
    elif "Battle of the Decades" in game_comments:
        game_type = "battle_of_the_decades"
    elif "Tournament of Champions" in game_comments:
        game_type = "tournament_of_champions"
    elif "College Championship" in game_comments:
        game_type = "college_championship"
    elif "Teachers Tournament" in game_comments:
        game_type = "teachers_tournament"
    elif "Kids Week" in game_comments:
        game_type = "kids_week"
    elif "Power Players Week" in game_comments:
        game_type = "power_players_week"
    elif "The IBM Challenge" in game_comments:
        game_type = "ibm_challenge"
    elif "Million Dollar Celebrity Invitational" in game_comments:
        game_type = "million_dollar_celebrity_invitational"
    else:
        game_type = "normal"
    if not parse_round(
        bsoup, cur, 1, gid, airdate, game_comments, game_type
    ) or not parse_round(bsoup, cur, 2, gid, airdate, game_comments, game_type):
        # One of the rounds does not exist
        pass
    # The final Jeopardy! round
    r = bsoup.find("table", class_="final_round")
    if not r:
        # This game does not have a final clue
        return
    category = r.find("td", class_="category_name").get_text()
    text = r.find("td", class_="clue_text").get_text()
    answer = BeautifulSoup(r.find("div", onmouseover=True).get("onmouseover"), "lxml")
    answer = answer.find("em").get_text()
    # False indicates no preset value for a clue
    insert(cur, gid, airdate, game_comments, game_type, 3, category, 0, text, answer)


def parse_round(bsoup, cur, rnd, gid, airdate, game_comments, game_type):
    """Parses and inserts the list of clues from a whole round."""
    round_id = "jeopardy_round" if rnd == 1 else "double_jeopardy_round"
    r = bsoup.find(id=round_id)
    # The game may not have all the rounds
    if not r:
        return False
    # The list of categories for this round
    categories = [c.get_text() for c in r.find_all("td", class_="category_name")]
    # The x_coord determines which category a clue is in
    # because the categories come before the clues, we will
    # have to match them up with the clues later on.
    x = 0
    for a in r.find_all("td", class_="clue"):
        is_missing = True if not a.get_text().strip() else False
        if not is_missing:
            value = (
                a.find("td", class_=re.compile("clue_value"))
                .get_text()
                .lstrip("D: $")
                .replace(",", "")
            )
            text = a.find("td", class_="clue_text").get_text()
            answer = BeautifulSoup(
                a.find("div", onmouseover=True).get("onmouseover"), "lxml"
            )
            answer = answer.find("em", class_="correct_response").get_text()
            insert(
                cur,
                gid,
                airdate,
                game_comments,
                game_type,
                rnd,
                categories[x],
                value,
                text,
                answer,
            )
        # Always update x, even if we skip
        # a clue, as this keeps things in order. there
        # are 6 categories, so once we reach the end,
        # loop back to the beginning category.
        x = (x + 1) % 6
    return True


def insert(
    cur, gid, airdate, game_comments, game_type, rnd, category, value, text, answer
):
    """Inserts the given clue into the database."""
    cur.execute(
        "INSERT INTO games(id, airdate, game_comments, game_type) VALUES(%s, %s, %s, %s) ON CONFLICT DO NOTHING",
        (gid, airdate, game_comments, game_type),
    )
    cur.execute(
        "INSERT INTO categories(category) VALUES(%s) ON CONFLICT DO NOTHING",
        (category,),
    )

    cur.execute("SELECT id FROM categories WHERE category=%s", (category,))
    category_id = cur.fetchone()["id"]
    cur.execute(
        "INSERT INTO clues(game_id, round, value, category_id, clue, answer) VALUES(%s, %s, %s, %s, %s, %s)",
        (gid, rnd, value, category_id, text, answer),
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse games from the J! Archive website.",
        add_help=False,
        usage="%(prog)s [options]",
    )
    parser.add_argument(
        "-d",
        "--dir",
        dest="dir",
        metavar="<folder>",
        help="the directory containing the game files",
        default="data/j-archive",
    )
    parser.add_argument(
        "-n",
        "--number-of-files",
        dest="num_of_files",
        metavar="<number>",
        help="the number of files to parse",
        type=int,
    )
    parser.add_argument("--help", action="help", help="show this help message and exit")
    parser.add_argument("--version", action="version", version="2022.01.04")
    main_parser(parser.parse_args())
