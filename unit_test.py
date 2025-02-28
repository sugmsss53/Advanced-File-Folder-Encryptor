import unittest
from unittest.mock import patch, MagicMock
import tempfile
import os
import shutil
import pyzipper
from encryptor import EncryptorApp  # Adjust based on your main file name

class TestEncryptorApp(unittest.TestCase):
    def setUp(self):
        """Set up the EncryptorApp instance and hide the GUI window."""
        self.app = EncryptorApp()
        self.app.withdraw()  # Prevent GUI from appearing during tests

    @patch('tkinter.filedialog.askopenfilename')
    @patch('tkinter.filedialog.askdirectory')
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_encrypt_file(self, mock_showerror, mock_showinfo, mock_askstring, mock_askdirectory, mock_askopenfilename):
        """Test encrypting a single file."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test file
            test_file = os.path.join(temp_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('Hello, world!')
            
            output_dir = os.path.join(temp_dir, 'output')
            os.makedirs(output_dir)
            
            # Configure mocks
            mock_askopenfilename.return_value = test_file
            mock_askdirectory.return_value = output_dir
            mock_askstring.return_value = 'password'
            
            # Run the method
            self.app.encrypt_file()
            
            # Verify original file is deleted
            self.assertFalse(os.path.exists(test_file))
            # Verify encrypted ZIP is created
            zip_path = os.path.join(output_dir, 'test.txt.enc.zip')
            self.assertTrue(os.path.exists(zip_path))
            
            # Verify ZIP contents by decrypting
            with pyzipper.AESZipFile(zip_path) as zf:
                zf.setpassword(b'password')
                zf.extractall(path=output_dir)
                extracted_file = os.path.join(output_dir, 'test.txt')
                with open(extracted_file, 'r') as f:
                    content = f.read()
                self.assertEqual(content, 'Hello, world!')
            
            # Verify success message
            mock_showinfo.assert_called_once()
            self.assertFalse(mock_showerror.called)

    @patch('tkinter.filedialog.askdirectory')
    @patch('tkinter.simpledialog.askstring')
    @patch('tkinter.messagebox.showinfo')
    @patch('tkinter.messagebox.showerror')
    def test_encrypt_folder(self, mock_showerror, mock_showinfo, mock_askstring, mock_askdirectory):
        """Test encrypting a folder with files and empty subdirectories."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test folder with files and an empty subdirectory
            test_folder = os.path.join(temp_dir, 'test_folder')
            os.makedirs(test_folder)
            sub_folder = os.path.join(test_folder, 'sub')
            os.makedirs(sub_folder)  # Empty subdirectory
            test_file1 = os.path.join(test_folder, 'file1.txt')
            with open(test_file1, 'w') as f:
                f.write('File 1')
            test_file2 = os.path.join(sub_folder, 'file2.txt')
            with open(test_file2, 'w') as f:
                f.write('File 2')
            
            output_dir = os.path.join(temp_dir, 'output')
            os.makedirs(output_dir)
            
            # Configure mocks
            mock_askdirectory.side_effect = [test_folder, output_dir]
            mock_askstring.return_value = 'password'
            
            # Run the method
            self.app.encrypt_folder()
            
            # Verify original folder is deleted
            self.assertFalse(os.path.exists(test_folder))
            # Verify encrypted ZIP is created
            zip_path = os.path.join(output_dir, 'test_folder.enc.zip')
            self.assertTrue(os.path.exists(zip_path))
            
            # Verify ZIP contents by decrypting
            with pyzipper.AESZipFile(zip_path) as zf:
                zf.setpassword(b'password')
                zf.extractall(path=output_dir)
                extracted_folder = os.path.join(output_dir, 'test_folder')
                self.assertTrue(os.path.exists(extracted_folder))
                self.assertTrue(os.path.exists(os.path.join(extracted_folder, 'file1.txt')))
                self.assertTrue(os.path.exists(os.path.join(extracted_folder, 'sub')))
                self.assertTrue(os.path.exists(os.path.join(extracted_folder, 'sub', 'file2.txt')))
                with open(os.path.join(extracted_folder, 'file1.txt'), 'r') as f:
                    self.assertEqual(f.read(), 'File 1')
                with open(os.path.join(extracted_folder, 'sub', 'file2.txt'), 'r') as f:
                    self.assertEqual(f.read(), 'File 2')
            
            # Verify success message
            mock_showinfo.assert_called_once()
            self.assertFalse(mock_showerror.called)

if __name__ == '__main__':
    unittest.main()