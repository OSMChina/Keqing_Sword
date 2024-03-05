import argparse
import os
import sys
import datetime
import zoneinfo

current_dir = os.path.dirname(os.path.realpath(__file__))
src_dir = os.path.join(current_dir, "..", "..", "..")
sys.path.append(src_dir)
from yuheng import Carto
from yuheng.basic import logger
from yuheng.component import Node, Way, Relation


LOCAL_TIMEZONE = "Asia/Shanghai"


def main(**kwargs):
    # if run in standalone cli, only support input a xml file and then parse it to Carto
    # if run by import, both parse xml or pass Carto object is acceptable.
    for k, v in kwargs.items():
        logger.debug(v)

        if isinstance(v, str):
            # parse mode
            if v[0:5] != "<?xml":
                # this is a file path
                logger.debug("this is a file path")
                logger.info(v)
                world = Carto()
                world.read(mode="file", file_path=v)
            else:
                logger.debug("this is a text")
                world = Carto()
                world.read(mode="memory", text=v)
        elif isinstance(v, type(Carto())):
            world = v
            world.meow()
        else:
            logger.info(f'Unrecognizable value from key "{k}"')
            pass

        # reverse
        metadata_frame_raw = []
        for id, element in world.node_dict.items():
            metadata_frame_raw.append(
                (
                    "n" + str(element.id),
                    element.timestamp,
                    element.uid,
                    element.changeset,
                )
            )
        for id, element in world.way_dict.items():
            metadata_frame_raw.append(
                (
                    "w" + str(element.id),
                    element.timestamp,
                    element.uid,
                    element.changeset,
                )
            )
        for id, element in world.relation_dict.items():
            metadata_frame_raw.append(
                (
                    "r" + str(element.id),
                    element.timestamp,
                    element.uid,
                    element.changeset,
                )
            )
        logger.debug(metadata_frame_raw[0])
        logger.debug(len(metadata_frame_raw))
        metadata_frame = []  # 因为暂时不引入pandas所以用字典做行，用了pandas就直接行数组插入了。
        for item in metadata_frame_raw:
            timezone_server = datetime.timezone.utc
            timezone_user = zoneinfo.ZoneInfo(LOCAL_TIMEZONE)
            time_utc_str = item[1]
            time_utc = datetime.datetime.strptime(
                time_utc_str, "%Y-%m-%dT%H:%M:%SZ"
            )
            time_utc = time_utc.replace(tzinfo=timezone_server)
            time_user = time_utc.astimezone(timezone_user)

            metadata_frame.append(
                {
                    "id": item[0],
                    "uid": item[2],
                    "changeset": item[3],
                    "time_year": time_user.year,
                    "time_month": time_user.month,
                    "time_day": time_user.day,
                    "time_hour": time_user.hour,
                    "time_minute": time_user.minute,
                    "time_second": time_user.second,
                }
            )
        logger.debug(metadata_frame[0])


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument("--file", type=str, default=True, dest="file")
    main(**argument_parser.parse_args().__dict__)
