'''
* Copyright (C) 2024 Intel Corporation.
*
* SPDX-License-Identifier: Apache-2.0
'''

import mock
import subprocess  # nosec B404
import unittest
import benchmark
import os


class Testing(unittest.TestCase):

    class MockPopen(object):
        def __init__(self):
            pass

        def communicate(self, input=None):
            pass

        @property
        def returncode(self):
            pass

    def test_docker_compose_containers_success(self):
        mock_popen = Testing.MockPopen()
        mock_popen.communicate = mock.Mock(
            return_value=('', '1Starting camera: rtsp://127.0.0.1:8554/' +
                          'camera_0 from *.mp4'))
        mock_returncode = mock.PropertyMock(return_value=0)
        type(mock_popen).returncode = mock_returncode

        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)
        res = benchmark.docker_compose_containers('up')

        self.assertEqual(res, ('',
                               '1Starting camera: rtsp://127.0.0.1:8554/' +
                               'camera_0 from *.mp4', 0))
        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called()

    def test_docker_compose_containers_fail(self):
        mock_popen = Testing.MockPopen()
        mock_popen.communicate = mock.Mock(return_value=('',
                                                         'an error occurred'))
        mock_returncode = mock.PropertyMock(return_value=1)
        type(mock_popen).returncode = mock_returncode

        setattr(subprocess, 'Popen', lambda *args, **kargs: mock_popen)
        res = benchmark.docker_compose_containers('up')

        self.assertEqual(res, ('', 'an error occurred', 1))
        mock_popen.communicate.assert_called_once_with()
        mock_returncode.assert_called()


    # class DirEntry:
    #     def __init__(self, path):
    #         self.path = path
    #         self.name = path

    #     def path(self):
    #         return self.path

    #     def name(self):
    #         return self.name

    #     def is_file(self):
    #         return True


    # @patch('os.scandir')
    # @patch('json.dumps')
    # def test_convert_csv_results_to_json(self, mock_scandir, mock_jsondumps):
    #     mock_dirEntry = Testing.DirEntry('device0.csv')
    #     mock_scandir.return_value = [mock_dirEntry]
    #     mock_jsondumps.return_value = '{\"key\":\"value\"}'
    #     benchmark.convert_csv_results_to_json('testdir','device')
    #     # self.assertEqual(res, 0)


    def test_convert_csv_results_to_json(self):
        csv_dir = './test_csv'
        found_json = False
        benchmark.convert_csv_results_to_json(csv_dir,'test')
        for entry in os.scandir(csv_dir):
            if  entry.is_file() and entry.name == 'test.json':
                found_json = True
                os.remove(os.path.join(csv_dir, 'test.json'))
        
        self.assertEqual(found_json, True, "json output successful")




if __name__ == '__main__':
    unittest.main()
