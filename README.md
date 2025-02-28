Advanced File/Folder Encryptor
Secure your sensitive files and folders effortlessly with Advanced File/Folder Encryptor, a user-friendly Python tool designed to protect your data from unauthorized access. This tool lets you lock (encrypt) and unlock (decrypt) files and folders using passwords, making data security accessible to everyone—whether you’re a tech enthusiast, small business owner, or learner.

Key Features
Simple GUI: An intuitive screen built with Python’s tkinter features buttons, progress bars, and helpful tips, so anyone can use it without technical expertise.
Strong Security: Uses AES encryption via pyzipper to create password-protected .enc.zip files, ensuring robust protection for your data.
Folder Support: Employs a breadth-first search (BFS) algorithm with a custom queue to efficiently encrypt entire folders while maintaining their structure.
Real-Time Feedback: Displays progress bars and status updates (e.g., “Encrypting file…”) to keep you informed during operations.
Safe Deletion: Automatically removes original files after encryption to prevent exposure, enhancing security.
Error Handling: Gracefully manages issues like missing files or wrong passwords, with clear error messages and logging for tracking.
Why Use It?
In today’s digital world, data breaches are common, but complex encryption tools can be intimidating. This tool bridges that gap, offering a straightforward solution for personal use or learning Python, security programming, and GUI development. It’s perfect for protecting documents, photos, or work files securely and easily.

Getting Started
Prerequisites
Python 3.x: Ensure Python is installed (check with python --version or python3 --version in your terminal).
Required Libraries:
tkinter (usually included with Python, verify with python -m tkinter).
pyzipper (install with pip install pyzipper).


Clone this repository to your local machine:

git clone https://github.com/sugmsss53/Advanced-File-Folder-Encryptor.git
cd Advanced-File-Folder-Encryptor
Install the required dependency:

pip install pyzipper
Verify tkinter is installed by running python -m tkinter. If a small window appears, it’s ready; otherwise, install it with pip install tk.


Future Improvements
More Encryption Methods: Add support for other encryption algorithms like RSA or Triple DES.
Real-Time File Monitoring: Automatically lock files as they’re added or changed for enhanced security.
Password-Protected Formats: Handle encryption of files like .zip, .rar, or .pdf directly.
Advanced Reporting: Provide detailed logs or reports on encryption/decryption actions for troubleshooting.
Cross-Platform Compatibility: Ensure the tool works seamlessly on Windows, macOS, and Linux.
Performance Optimization: Improve speed and memory use for large folders or files, especially during BFS traversal.
Contributing
We welcome contributions! Fork this repository, make changes, and submit a pull request. Report issues or suggest features via GitHub Issues. Join us in making this tool even better for data security!



GitHub Link
https://github.com/sugmsss53/Advanced-File-Folder-Encryptor

