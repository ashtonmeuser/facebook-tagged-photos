# Download Facebook Tagged Photos

Download all photos a user is tagged in on Facebook.

## Dependencies

Requires Python 3. The Python Software Foundation provides instructions for installing Python 3 on [Unix](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) and [Windows](https://docs.python.org/3/using/windows.html#installing-python).

Selenium is also required. It is a software testing framework that allows Python to take control of a web browser. You can install Selenium by running the following.

```
pip install selenium
```

If you have several versions of pip installed, you may need to run the follwing.

```
pip3 install selenium
```

Chrome is used to interact with Facebook via Selenium. As such, you will need to install a driver for Chrome. The driver can be found [here](https://sites.google.com/a/chromium.org/chromedriver/downloads). If using a Unix system, add the driver to `/usr/local/bin`.

Clone this repo and you're good to go!

### Running

First, find your Facebook user ID. At the time of writing, [this](https://findmyfbid.in) tool was functional.

Run the below command in the command line from within the project directory, replacing `<your_facebook_id>` with your Facebook ID.

```
python3 facebook_photos.py <your_facebook_id>
```

If you'd prefer to have the photos saved elsewhere, provide another argument of the desired output directory. This results in the following command.

```
python3 facebook_photos.py <your_facebook_id> <your_output_directory>
```
