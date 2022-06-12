import io
import os

fake_file = os.path.join(os.getcwd(), 'setup_data')
with io.open(fake_file, 'w') as file_pointer:
    file_pointer.write('')
