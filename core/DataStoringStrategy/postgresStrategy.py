import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()
params = {
    "host": os.getenv("POSTGRES_HOST"),
    "database": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PSW")
}


def connect():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error in connecting to Database\n")
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    return conn, cur


def init_datastructure():
    commands = (
        """
        DROP TABLE IF EXISTS summoners CASCADE;
        DROP TABLE IF EXISTS soloduo CASCADE;
        DROP TABLE IF EXISTS flex CASCADE;
        """,
        """
        CREATE TABLE summoners (
            summoner_name VARCHAR(255) NOT NULL,
            PRIMARY KEY(summoner_name)
        );
        """,
        """
        CREATE TABLE soloduo (
            solo_id SERIAL PRIMARY KEY,
            soloduo_tier VARCHAR(30) NOT NULL,
            soloduo_rank VARCHAR(10) NOT NULL,
            soloduo_lp INTEGER NOT NULL,
            summoner_name VARCHAR(100),
            CONSTRAINT summoner_name
                FOREIGN KEY(summoner_name)
                    REFERENCES summoners(summoner_name)
                    ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE flex (
            flex_id SERIAL PRIMARY KEY,
            flex_tier VARCHAR(30) NOT NULL,
            flex_rank VARCHAR(10) NOT NULL,
            flex_lp INTEGER NOT NULL,
            summoner_name VARCHAR(100),
            CONSTRAINT summoner_name
                FOREIGN KEY(summoner_name)
                    REFERENCES summoners(summoner_name)
                    ON DELETE CASCADE
        );
        """
    )

    conn, cur = connect()

    for command in commands:
        print(f"Running: {command}")
        cur.execute(command)

    cur.close()
    conn.commit()
    conn.close()


def insert_new_summoner(summoner_name: str):
    conn, cur = connect()

    sql = """INSERT INTO summoners VALUES ('{}');;"""
    cur.execute(sql.format(summoner_name))

    cur.close()
    conn.commit()
    conn.close()


def insert_new_soloduo_stats(stats: list):
    conn, cur = connect()

    sql = """
    INSERT INTO soloduo(soloduo_tier, soloduo_rank, soloduo_lp, summoner_name)
    VALUES{}
    """
    cur.execute(sql.format(", ".join([str(stat) for stat in stats])))

    cur.close()
    conn.commit()
    conn.close()


def insert_new_flex_stats(stats: list):
    conn, cur = connect()

    sql = """
    INSERT INTO flex(flex_tier, flex_rank, flex_lp, summoner_name)
    VALUES{}
    """

    print(stats)
    cur.execute(sql.format(", ".join([str(stat) for stat in stats])))

    cur.close()
    conn.commit()
    conn.close()


def get_recent_flex_stats() -> dict:
    conn, cur = connect()

    sql = """
    SELECT summoners.summoner_name, flex_tier, flex_rank, flex_lp FROM summoners
    JOIN (SELECT summoner_name, max(flex_id) as max_id FROM flex
	GROUP BY summoner_name) as pu
	ON summoners.summoner_name = pu.summoner_name
    JOIN flex ON flex.flex_id = pu.max_id; """

    cur.execute(sql)
    # print("The number of answers: " , cur.rowcount)

    row = cur.fetchall()
    cur.close()
    conn.close()

    return {x[0]: {
        "tier": x[1],
        "rank": x[2],
        "lp": x[3]}
        for x in row}


def get_recent_soloduo_stats() -> dict:
    conn, cur = connect()

    sql = """
    SELECT summoners.summoner_name, soloduo_tier, soloduo_rank, soloduo_lp FROM summoners
    JOIN (SELECT summoner_name, max(solo_id) as max_id FROM soloduo
	GROUP BY summoner_name) as pu
	ON summoners.summoner_name = pu.summoner_name
    JOIN soloduo ON soloduo.solo_id = pu.max_id;"""

    cur.execute(sql)
    # print("The number of answers: " , cur.rowcount)

    row = cur.fetchall()
    cur.close()
    conn.close()

    return {x[0]: {
        "tier": x[1],
        "rank": x[2],
        "lp": x[3]}
        for x in row}


def delete_summoner(summoner_name: str):
    conn, cur = connect()

    sql = """
    DELETE FROM summoners WHERE summoners.summoner_name = '{}';
    """
    cur.execute(sql.format(summoner_name))

    cur.close()
    conn.commit()
    conn.close()


def get_summoners() -> list:
    conn, cur = connect()

    sql = """
    SELECT * FROM summoners;
    """

    cur.execute(sql)
    summoners = cur.fetchall()

    cur.close()
    conn.close()

    return [x[0] for x in summoners]


if __name__ == "__main__":
    try:
        init_datastructure()
    except:
        print("Failed making tables")
    else:
        print("Made table")