852gmap: Mashing up MARC location data with Google Maps

852gmap takes MARC location data from the 852 field of MARC records, geocodes
it, and displays the data onto a Google Map using Python and Exhibit from the
MIT Simile project <http://simile.mit.edu/exhibit/>.

Requirements:
- Python, with the following modules: 
  - geopy - http://exogen.case.edu/projects/geopy/
  - pymarc (>= 1.0)
  - simplejson
- Google Maps and Yahoo Maps API keys

Files:
- 852tojson.py        MARC parsing, geocoding, and conversion to JSON
- repositories.html   Presentation for Exhibit
- repositories.json   Sample repository data

References:
- Simile Exhibit:
  - http://simile.mit.edu/exhibit/
  - http://simile.mit.edu/wiki/Exhibit/For_Authors
  - Exhibit Map View:
    - http://simile.mit.edu/wiki/Exhibit/2.0/Map_View
    - http://simile.mit.edu/wiki/Exhibit/2.0/Map_View_Tutorial
- Google Maps API Key:
  - http://www.google.com/apis/maps/signup.html
- Yahoo Maps API Key:
  - https://developer.yahoo.com/wsregapp/index.php

The Process:
- Insert your API keys into 852tojson.py and in repositories.html
- 852tojson.py takes a MARC file as input and outputs JSON:
  - $ python 852tojson.py [filename.mrc] [filename.json]
- Edit repositories.html to your desired layout

Notes:
- Exhibit does not work well in Safari
- Expects 852 data as 852$a[Institution]$b[Subordinate body]$e[Address] and
  country in 904$a, but will handle exception properly if 904$a is not there