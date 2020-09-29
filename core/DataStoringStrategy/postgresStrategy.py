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
        conn =  psycopg2.connect(**params)
        cur = conn.cursor()
        # cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # finally:
    #     if conn is not None:
    #         conn.close()
    return (conn, cur)

def init_datastructure():
    commands = (
        """
        DROP TABLE IF EXISTS summoners CASCADE;
        DROP TABLE IF EXISTS soloduo CASCADE;
        DROP TABLE IF EXISTS flex CASCADE;
        """,
        """
        CREATE TABLE summoners (
            puuid VARCHAR(100),
            summoner_name VARCHAR(255) NOT NULL,
            PRIMARY KEY(puuid)
        );
        """,
        """
        CREATE TABLE soloduo (
            solo_id SERIAL PRIMARY KEY,
            soloduo_tier VARCHAR(30) NOT NULL,
            soloduo_rank VARCHAR(10) NOT NULL,
            soloduo_lp INTEGER NOT NULL,
            puuid VARCHAR(100),
            CONSTRAINT puuid
                FOREIGN KEY(puuid)
                    REFERENCES summoners(puuid)
                    ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE flex (
            flex_id SERIAL PRIMARY KEY,
            flex_tier VARCHAR(30) NOT NULL,
            flex_rank VARCHAR(10) NOT NULL,
            flex_lp INTEGER NOT NULL,
            puuid VARCHAR(100),
            CONSTRAINT puuid
                FOREIGN KEY(puuid)
                    REFERENCES summoners(puuid)
                    ON DELETE CASCADE
        );
        """
    )
    
    conn, cur = connect()

    for command in commands:
        cur.execute(command)

    cur.close()
    conn.commit()
    conn.close()

def insert_new_summoner(puuid: str, summoner_name: str):
    conn, cur = connect()
    
    sql = """INSERT INTO summoners(puuid, summoner_name) VALUES{}"""
    cur.execute(sql.format((puuid, summoner_name)))
    
    cur.close()
    conn.commit()
    conn.close()

def insert_new_soloduo_stats(stats: list):
    conn, cur = connect()

    sql = """
    INSERT INTO soloduo(soloduo_tier, soloduo_rank, soloduo_lp, puuid)
    VALUES{}
    """
    cur.execute( sql.format(", ".join([str(stat) for stat in stats])) )


    cur.close()
    conn.commit()
    conn.close()

def insert_new_flex_stats(stats: list):
    conn, cur = connect()

    sql = """
    INSERT INTO flex(flex_tier, flex_rank, flex_lp, puuid)
    VALUES{}
    """

    cur.execute( sql.format(", ".join([str(stat) for stat in stats])) )

    cur.close()
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_datastructure()
    insert_new_summoner("123", "Bis")
    insert_new_soloduo_stats([("Gold", "IV", 32, "123")])
    insert_new_soloduo_stats([("Gold", "IV", 32, "123")])
    insert_new_soloduo_stats([("Gold", "IV", 32, "123")])
    insert_new_flex_stats([("Gold", "IV", 32, "123")])
    insert_new_flex_stats([("Gold", "IV", 32, "123")])
    insert_new_flex_stats([("Gold", "IV", 32, "123")])