from typing import Optional

import psycopg
import os
import sys

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "..", "..")
sys.path.append(src_dir)
from yuheng import Waifu


def check():
    # migration if needed
    #
    pass


def get_data(
    connection_dbname="postgres",
    connection_user="postgres",
    connection_password="12345678",
    connection_host="localhost",
    connection_port="5432",
    query_mode="full",
    query_type=["line"],
    pg_schema="public",
    pg_pre_fix="planet_osm",
) -> Optional[Waifu]:
    """
    # full-全量查询
    # batch-批量查询
    # single-单条查询
    """
    config = {
        "dbname": connection_dbname,
        "user": connection_user,
        "password": connection_password,
        "host": connection_host,
        "port": connection_port,
    }
    result = []
    with psycopg.connect(
        " ".join([item + "=" + config.get(item) for item in config])
    ) as connection:
        with connection.cursor() as cursor:
            if query_mode == "full":
                if len(query_type) == 1 and (
                    "line" in query_type or "point" in query_type
                ):
                    sql = f"SELECT * FROM {pg_schema}.{pg_pre_fix}_{query_type[0]}"
                    cursor.execute(sql)
                    for record in cursor:
                        result.append((query_type[0], record))
                elif (
                    len(query_type) == 2
                    and "line" in query_type
                    and "point" in query_type
                ):
                    sql_a = f"SELECT * FROM {pg_schema}.{pg_pre_fix}_{query_type[0]}"
                    cursor.execute(sql_a)
                    for record in cursor:
                        result.append((query_type[0], record))
                    sql_b = f"SELECT * FROM {pg_schema}.{pg_pre_fix}_{query_type[1]}"
                    cursor.execute(sql_b)
                    for record in cursor:
                        result.append((query_type[1], record))
                else:
                    print("要么你就想查询line/point以外的表，要么你就输了太多项。目前无法支持。")
                    return None
    print("len(result)", "=", len(result))
    return result


def main():
    print("本数据驱动无法独立于Yuheng单独使用")


if __name__ == "__main__":
    get_data()
