=====================
Setup and Maintenance
=====================

Misago is Python and Django application which means system requirements as well as setup process and way maintenace taks are performed may appear confusing and suprising to administrators that have no experience outside of running PHP solutions.


Installing Misago
=================

Misago installation is three step process. First you compare your server's specification to check if will be able to run Misago. Next you setup Misago and all extra services required for it to function like e-mails, database and automatic maintenance jobs. Finally you get your site running and accessible for your users.


Requirements
------------

Before you start make sure your hosting provider grants you:

- SSH access to server
- Python **2.7** (this is important, Python version 3 and older than 2.7 are not supported) and PIP
- Either MySQL or PostgreSQL database
- 60 megabytes of RAM for Misago process
- A way to direct HTTP traffic from your domain to Misago
- CronTabs or other task scheduler

This is not a problem on VPS or dedicated servers, but availability of shared servers that meet those requirements differs from country to country.

Speaking of shared servers, ability to download, compile and run software from internet may be needed, but different ISP's have different approach to this. Some options come with all dependencies preinstalled, others let you install them yourself and others require you to mail them every time you need something installed. Generally you should avoid offers coming from last group because this turns running Python apps into a hore.


Setup
-----



Deployment
----------

Deployment is a process in which you get your site running and reachable by your users.

Misago is de facto Django with extra features added. This means deployment of Misago should be largery same to deployment of other Django-based solutions. Django documentation `already covers <https://docs.djangoproject.com/en/1.6/howto/deployment/>`_ supported deployment methods, and while on dedicated and VPS options deployment method depends largery on your choice and employed software stack, shared servers may differ greatly by the way how Django should be deployed. If thats the case, make sure you consult your ISP documentation and/or ask its rep for details about supported deployment method.

.. note::
   If you are deploying Misago on your own dedicated or virtual server, you may want to take interest in `the Gunicorn <http://gunicorn.org/>`_ that makes it easier to maintain Python deployments.


Updating to new version
=======================

Lorem ipsum dolor met.


Growing up with your community
==============================

Lorem ipsum dolor met.