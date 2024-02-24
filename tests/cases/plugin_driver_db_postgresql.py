import os
import sys
import unittest

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "../../src")
sys.path.append(src_dir)

from yuheng import Waifu


class TestPluginDriverDbPostgresql(unittest.TestCase):
    def setUp(self) -> None:
        # NOTE: conduct this part of postgresql need you deploy a server.
        pass

    def test_plugin_driver_db_postgresql_full_1type(self):
        from yuheng.plugin.driver_db_postgresql.__main__ import get_data

        carto = get_data(
            connection_dbname="osm2pgsql",
            connection_user="postgres",
            connection_password="12345678",
            connection_host="localhost",
            connection_port="5432",
            query_mode="full",
            query_type=["line"],
        )
        print("len(carto.node_dict):", len(carto.node_dict))
        print("len(carto.way_dict):", len(carto.way_dict))
        assert isinstance(carto, type(yuheng.Waifu))

    def test_plugin_driver_db_postgresql_full_2type(self):
        from yuheng.plugin.driver_db_postgresql.__main__ import get_data

        carto = get_data(
            connection_dbname="osm2pgsql",
            connection_user="postgres",
            connection_password="12345678",
            connection_host="localhost",
            connection_port="5432",
            query_mode="full",
            query_type=["line", "point"],
        )
        print("len(carto.node_dict):", len(carto.node_dict))
        print("len(carto.way_dict):", len(carto.way_dict))

    def test_plugin_driver_db_postgresql_full_invalidtype(self):
        from yuheng.plugin.driver_db_postgresql.__main__ import get_data

        result = get_data(
            connection_dbname="osm2pgsql",
            connection_user="postgres",
            connection_password="12345678",
            connection_host="localhost",
            connection_port="5432",
            query_mode="full",
            query_type=["line", "point", "polygon"],
        )
        assert result == None


if __name__ == "__main__":
    unittest.main()
