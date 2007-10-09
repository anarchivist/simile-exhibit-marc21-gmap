import pymarc, simplejson, sys
from geopy import geocoders as gc
from unicodedata import normalize as uninorm

g_api_key = 'ABQIAAAAO4inKKBbkm8WiigSm3owFhTvlhzuh3Ln98gA1ajQWp4aDQ9CJxTeDBhs-YGBMXGNtO5xWGF2HWVQ1w'
y_api_key = 'gYeLNE3V34FScM89Mn1D1sA2FwNBwGnU2iF2WEr14d1g1LqhFh4BosxznBhxkU00huQPpcTo'
default_name = u'American Institute of Physics. Center for History of Physics. Niels Bohr Library'
default_address = u'One Physics Ellipse, College Park, MD 20740, USA'

types = { 'repository': { 'pluralLabel': 'repositories' } }
repos_list = []
repos_counter = 1
engines = (gc.Google(g_api_key), gc.Yahoo(y_api_key))
marc_in = pymarc.MARCReader(file(sys.argv[1]))
json_out = open(sys.argv[2], 'w')

class Break(Exception): pass

def normalize_address(address):
  return uninorm('NFD', address.strip('.:,;/ ')).encode('ascii', 'ignore')

def utf8_join(in_list):
  out = ' '.join(in_list)
  out = pymarc.marc8_to_unicode(out)
  return out.strip('.:,;/ ')

try:
  for record in marc_in:
    repos_name = repos_address = repos_country = gc_address = normalized_address = address_source = u''
    repos = {}
    repos_detail = {}
    if record['852'] is not None:
      repos_name = utf8_join(record['852'].getSubfields('a', 'b'))
      repos_address = utf8_join(record['852'].getSubfields('e'))
    else:
      (repos_name, repos_address) = (default_name, default_address)
    repos = { 'label': repos_name, 'type': 'repository' }
    repos_detail['id'] = repos_name
    try:
      repos_country = pymarc.marc8_to_unicode(record['904']['a']).strip('.:,;/ ')
      repos_detail['country'] = repos_country
    except:
      pass
    if repos not in repos_list:
      repos_detail['address'] = repos_address
      for engine in engines:
        normalized_address = normalize_address(repos_address)
        try:
          canonical_address, (lat, lng) = engine.geocode(normalized_address)
          address_source = engine.__class__.__name__
          repos_detail['normalized_address'] = normalized_address
          repos_detail['canonical_address'] = canonical_address
          repos_detail['address_source'] = address_source
          repos_detail['addressLatLng'] = '%f,%f' % (lat, lng)
          raise Break
        except Break:
          break
        except:
          if repos_country.upper() not in repos_address.upper():
            normalized_address = normalize_address('%s %s' % (repos_address, repos_country.upper()))
            try:
              canonical_address, (lat, lng) = engine.geocode(normalized_address)
              address_source = engine.__class__.__name__
              repos_detail['normalized_address'] = normalized_address
              repos_detail['canonical_address'] = canonical_address
              repos_detail['address_source'] = address_source
              repos_detail['addressLatLng'] = '%f,%f' % (lat, lng)
              raise Break
            except Break:
              break
            except: pass
          pass
      else:
        repos_detail['address_source'] = 'None'
      repos_list.extend([repos, repos_detail])
      repos_counter += 1
finally:
  simplejson.dump({'items': repos_list, 'types': types}, json_out, indent=2)
  json_out.close()
#