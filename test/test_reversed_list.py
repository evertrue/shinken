#!/usr/bin/env python

import unittest

import __import_shinken
from shinken.misc.regenerator import Regenerator
from shinken.brok import Brok
from shinken_test import ShinkenTest


class TestReversedList(ShinkenTest):
    def setUp(self):
        self.setup_with_file("etc/shinken_service_withhost_exclude.cfg")

    def test_reversed_list(self):
        """ Test to ensure new conf is properly merge with different servicegroup definition
        The first conf has all its servicegroup defined servicegroups.cfg and services.cfg
        The second conf has both, so that servicegroups defined ins services.cfg are genretaed by Shinken
        This lead to another generated id witch should be handled properly when regenerating reversed list / merging
        servicegroups definition
        """

        for service in self.sched.servicegroups:
            assert(service.servicegroup_name in self.sched.servicegroups.reversed_list.keys())
            assert(service.id == self.sched.servicegroups.reversed_list[service.servicegroup_name])

        prev_id = self.sched.servicegroups.reversed_list['servicegroup_01']

        reg = Regenerator()
        data = {"instance_id": 0}
        b = Brok('program_status', data)
        b.prepare()
        reg.manage_program_status_brok(b)
        reg.all_done_linking(0)


        self.setup_with_file("etc/shinken_reversed_list.cfg")

        reg.all_done_linking(0)

        for service in self.sched.servicegroups:
            assert(service.servicegroup_name in self.sched.servicegroups.reversed_list.keys())
            assert(service.id == self.sched.servicegroups.reversed_list[service.servicegroup_name])

        assert(prev_id != self.sched.servicegroups.reversed_list['servicegroup_01'])

        for sname in [u'servicegroup_01', u'ok', u'flap', u'unknown', u'random',
                      u'servicegroup_02', u'servicegroup_03', u'warning', u'critical',
                      u'servicegroup_04', u'servicegroup_05', u'pending', u'mynewgroup']:
            assert(sname in self.sched.servicegroups.reversed_list.keys())



if __name__ == '__main__':
    unittest.main()
