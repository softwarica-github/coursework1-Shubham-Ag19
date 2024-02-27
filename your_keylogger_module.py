import unittest
from unittest.mock import patch
from your_keylogger_module import Keylogger, GUI, DataStorage

class TestIntegration(unittest.TestCase):

    def setUp(self):
        # Initialize necessary objects for testing
        self.keylogger = Keylogger()
        self.gui = GUI()
        self.data_storage = DataStorage()

    def tearDown(self):
        # Clean up resources after each test if needed
        pass

    def test_keylogger_integration_with_gui(self):
        # Test integration between keylogger and GUI
        with patch('builtins.print') as mock_print:
            # Start keylogger using GUI
            self.gui.start_keylogger()
            self.assertTrue(self.keylogger.flag)  # Check if the keylogger flag is set
            mock_print.assert_called_with("[+] Keylogger is running!\n[!] Saving the keys in 'keylogger.txt'")

            # Stop keylogger using GUI
            self.gui.stop_keylogger()
            self.assertFalse(self.keylogger.flag)  # Check if the keylogger flag is reset
            mock_print.assert_called_with("Keylogger stopped.")

    def test_keylogger_integration_with_data_storage(self):
        # Test integration between keylogger and data storage
        self.keylogger.keys_used = [{'Pressed': 'a'}, {'Released': 'a'}]
        with patch('builtins.print') as mock_print:
            # Save keylog data using data storage
            self.data_storage.save_to_text()
            mock_print.assert_called_with("[!] Keylog data saved to 'key_log.txt'")

            # Save keylog data using data storage in JSON format
            self.data_storage.save_to_json()
            mock_print.assert_called_with("[!] Keylog data saved to 'key_log.json'")

    # Add more integration test cases as needed

if __name__ == '__main__':
    unittest.main()
