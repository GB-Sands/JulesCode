import unittest
import os
import subprocess
import h5py

class TestConverter(unittest.TestCase):

    def setUp(self):
        self.input_file = 'tdms_to_biosignalml/tests/TestData.tdms'
        self.output_file = 'tdms_to_biosignalml/tests/TestData.h5'
        self.script = 'tdms_to_biosignalml.tdms_to_biosignalml'

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_conversion(self):
        result = subprocess.run(['python', '-m', self.script, self.input_file, self.output_file], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(self.output_file))

        with h5py.File(self.output_file, 'r') as f:
            self.assertEqual(f.attrs['version'], 'BSML 1.0')
            self.assertIn('uris', f)
            self.assertIn('recording', f)
            self.assertIn('signal', f['recording'])
            self.assertEqual(len(f['recording/signal']), 2)

    def test_data_selection(self):
        result = subprocess.run(['python', '-m', self.script, self.input_file, self.output_file, '--data', 'Devices/ECG'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(self.output_file))

        with h5py.File(self.output_file, 'r') as f:
            self.assertEqual(len(f['recording/signal']), 1)

if __name__ == '__main__':
    unittest.main()
