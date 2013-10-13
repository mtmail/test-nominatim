Simple functional tests for the Nominatim API.

The tests use the lettuce framework (http://lettuce.it/) and
nose (https://nose.readthedocs.org). They are meant to be run
against a Nominatim installation with a complete planet-wide
setup based on a fairly recent planet. If you only have an
excerpt, some of the tests may fail.

Usage
=====

 * get lettuce and nose

     [sudo] pip install lettuce nose pytidylib

 * run the tests

     NOMINATIM_SERVER=http://your.nominatim.instance/ lettuce features
