import unittest
import os
import subprocess
import biosignalml.model as v1
import biosignalml.rdf as rdf
from biosignalml.model.ontology import BSML

class TestConverter(unittest.TestCase):

    def setUp(self):
        self.input_file = 'TestData.tdms'
        self.output_file = 'test_output.bsml'
        self.script = 'tdms_to_biosignalml.tdms_to_biosignalml'
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    def test_list_channels(self):
        result = subprocess.run(['python', '-m', self.script, self.input_file, '--list'], capture_output=True, text=True, cwd=self.base_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "Devices/Spirometer\nDevices/ECG")

    def test_dry_run(self):
        result = subprocess.run(['python', '-m', self.script, self.input_file, self.output_file, '--dry-run'], capture_output=True, text=True, cwd=self.base_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Dry run enabled.", result.stdout)

    def test_conversion(self):
        result = subprocess.run(['python', '-m', self.script, self.input_file, self.output_file], capture_output=True, text=True, cwd=self.base_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(self.output_file))

        # Verify the contents of the output file
        uri = 'file://' + os.path.abspath(self.output_file)
        graph = rdf.Graph.create_from_resource(uri, format=rdf.Format.TURTLE)
        signals = list(graph.subjects(rdf.RDF.type, BSML.Signal))
        self.assertEqual(len(signals), 2)

    def test_data_selection(self):
        result = subprocess.run(['python', '-m', self.script, self.input_file, self.output_file, '--data', 'Devices/ECG'], capture_output=True, text=True, cwd=self.base_dir)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(os.path.exists(self.output_file))

        # Verify the contents of the output file
        uri = 'file://' + os.path.abspath(self.output_file)
        graph = rdf.Graph.create_from_resource(uri, format=rdf.Format.TURTLE)
        signals = list(graph.subjects(rdf.RDF.type, BSML.Signal))
        self.assertEqual(len(signals), 1)

if __name__ == '__main__':
    unittest.main()
