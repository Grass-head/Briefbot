Brief
=====

Description
-----------

User 1 (executor) uploads his questions and following answers to the bot. After he receives a link to his questionnaire and gives it to user 2 (customer). Using the questions previously set by user 1, the bot clarifies the real needs of user 2 in content production, and cutting off unnecessary information. A text report (technical task) is sent to the user 1 by e-mail.

Functional
--------------------

Installing
----------

Create a virtual environment and activate it. From an activated virtual environment, do:

.. code-block:: text
	
	pip install -r requirements.txt

Customization & Start
---------------------

Create file settings.py and add the following information there:

.. code-block:: python


	PROXY = {'proxy_url': 'socks5://your_SOCKS5_PROXI:1080','urllib3_proxy_kwargs': {'username': 'your login', 'password': 'your password'}}

	API_KEY = "API - key, which ypu received from Godfather bot"


Contacts
--------

For any questions please contact:
kseniyabagnyuk@gmail.com

По всем вопросам пишите на:
kseniyabagnyuk@gmail.com