# sms-phone-verification-python

This is an application example implementing an SMS phone verification using
Python 3.12.2 and [Flask](http://flask.pocoo.org/) web framework.

Follow along [using this "How to Build a Basic Flask Website to Authenticate Users with Twilio Verify" tutorial](https://www.twilio.com/en-us/blog/basic-flask-python-twilio-verify).

## Local Development

This project is built using [Flask](http://flask.pocoo.org/) web framework.

1. First clone this repository and `cd` into it.

   ```bash
   $ git clone git@github.com:twilio-samples/sms-phone-verification-python.git
   $ cd sms-phone-verification-python

   ```

1. Create a new virtual environment.

    - If using vanilla [virtualenv](https://virtualenv.pypa.io/en/latest/):

        ```bash
        virtualenv venv
        source venv/bin/activate
        ```

    - If using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/):

        ```bash
        mkvirtualenv sms-phone-verification-python
        ```

1. Install the dependencies.

    ```bash
    pip install -r requirements.txt
    ```


1. Start the server.

    ```bash
    flask run
    ```

1. Expose the application to the wider Internet using [ngrok](https://ngrok.com/).

    ```bash
    ngrok http 5000 
    ```


## Meta

* No warranty expressed or implied. Software is as is. Diggity.
* [MIT License](http://www.opensource.org/licenses/mit-license.html)
* Lovingly crafted by Twilio Developer Education.