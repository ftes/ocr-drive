ocr-drive
=========

Perform OCR locally on a Unix machine in combination with Google Drive for document storage.
While the python scripts are platform independent, for now `pdfsandwich` is used as a wrapper script
for performing OCR on PDF files and embedding the results back into the PDF, and is therefore only
available for Unix systems.


Dependencies
------------
The following software must be installed for the scripts to work:
* [pdfsandwich](http://www.tobias-elze.de/pdfsandwich/index.html)
* [python 2](http://wiki.ubuntuusers.de/Python)
* [Google Drive python SDK](https://developers.google.com/drive/quickstart-python)


Usage
-----

1. [Enable](https://developers.google.com/drive/quickstart-python#step_2_install_the_google_client_library) both the Drive SDK and Drive API in the Google API Console.
2. Save your API credentials in `client-secrets.json`, the syntax for which is shown in [authorize.py](authorize.py).
3. Run the `authorize.py` script, which will provide you with a URL to visit and access an authorization code.
4. Add the [process.sh](process.sh) and [download-for-ocr.py](download-for-ocr.py) scripts to your incron (run `incrontab -e`) and cron (run `crontab -e`) tables, so they run automatically.
Example configurations are included as comments at the beginning of both files.