#!/usr/bin/env python3

import psycopg2
from psycopg2.extras import RealDictCursor
from colors import color


def group_dicts_by(xs, k):
    result = {}
    for x in xs:
        val = x[k]
        if val not in result:
            result[val] = [x]
        else:
            result[val].append(x)
    return result


def ask_clue(conn, cur, game_id, clue):
    value = clue["normalized_value"]
    print(f"\n${value}: {clue['clue']}")
    response = input("Answer? ")
    print(f"Actual answer: {clue['answer']}")
    correct = (response.lower() == clue["answer"].lower()) or (
        (response.strip() != '' and input("Correct? [y/N] ").strip().lower() == "y")
    )
    cur.execute(
        """INSERT INTO clue_responses(clue_id, answer_given, was_correct) VALUES (%s, %s, %s)""",
        (clue["clue_id"], response, correct),
    )
    conn.commit()
    if correct:
        return 1
    elif response.strip() != "":
        return -1
    else:
        return 0


def play_game(conn, cur, game_id):
    cur.execute(
        """INSERT INTO game_attempts(game_id) VALUES (%s) RETURNING id""",
        (game_id,),
    )
    conn.commit()
    attempt_id = cur.fetchone()["id"]
    # Load clues and categories
    cur.execute(
        """
        SELECT category, clues.id AS clue_id, round, normalized_value, clue, answer
        FROM clues LEFT JOIN categories ON clues.category_id = categories.id
        WHERE clues.game_id = %s""",
        (game_id,),
    )
    clues_by_round = group_dicts_by(cur.fetchall(), "round")
    total = 0
    for round in [1, 2]:
        print(color(f"\nStarting round {round}:", fg='blue'))
        for category, clues in group_dicts_by(
            clues_by_round[round], "category"
        ).items():
            print(color(f"\nStarting category {category}", fg='red'))
            for clue in sorted(clues, key=lambda x: x["normalized_value"]):
                total += clue["normalized_value"] * ask_clue(conn, cur, game_id, clue)
                print(f"Total: ${total}")

    print(color("FINAL JEOPARDY!!!!", fg='red', style='underline'))
    final_correct = ask_clue(conn, cur, game_id, clues_by_round[3][0])
    cur.execute(
        "UPDATE game_attempts SET total=%s, final_correct=%s WHERE id=%s",
        (total, final_correct, attempt_id),
    )


def main(conn, cur):
    cur.execute(
        """
            SELECT games.id AS id, airdate
            FROM games LEFT JOIN game_attempts ON games.id = game_attempts.game_id
            WHERE game_attempts.id IS NULL AND game_type='normal' AND airdate >= '1998'
            ORDER BY airdate
            LIMIT 1"""
    )
    game = cur.fetchone()
    print(
        color(f"\nPlaying game {game['id']} ({game['airdate']})", fg='red')
    )
    play_game(conn, cur, game["id"])


if __name__ == "__main__":
    with psycopg2.connect(
        dbname="jeopardy",
        user="jeopardy",
        password="jeopardypassword",
        cursor_factory=RealDictCursor,
    ) as conn:
        with conn.cursor() as cur:
            main(conn, cur)
