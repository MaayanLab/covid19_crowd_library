import uuid
import datetime
import sys
import ast
from app import models
from app.database import Session, object_as_dict

def _get_models():
  return [
    models.Gene,
    models.Geneset,
    models.GenesetGene,
    models.Drug,
    models.Drugset,
    models.DrugsetDrug,
  ]

def _dump_value(value):
  if isinstance(value, datetime.datetime):
    return { '@type': 'datetime', 'value': value.toordinal() }
  elif isinstance(value, uuid.UUID):
    return { '@type': 'uuid', 'value': value.hex() }
  elif type(value) in {str, bytes, int, float, tuple, list, dict, set, bool, type(None)}:
    return value
  else:
    raise Exception(f'Unhandled type {value}')

def _load_value(value):
  if isinstance(value, dict) and '@type' in value:
    if value['@type'] == 'datetime':
      return datetime.datetime.fromordinal(value['value'])
    elif value['@type'] == 'uuid':
      return uuid.UUID(value['value'])
    else:
      raise Exception(f'Unhandled type {value["@type"]}')
  else:
    return value

def _dump_item(item):
  return dict(
    **{
      k: _dump_value(v)
      for k, v in object_as_dict(item).items()
    },
    **{'@type': item.__class__.__name__},
  )

def _load_item(item):
  value = ast.literal_eval(item)
  return getattr(models, value['@type'])(
    **{
      k: _load_value(v)
      for k, v in value.items()
      if k != '@type'
    }
  )

def dump():
  sess = Session()
  for Model in _get_models():
    for item in sess.query(Model):
      print(_dump_item(item), file=sys.stdout)
  sess.close()

def load():
  sess = Session()
  cur_type = None
  for item in map(_load_item, filter(None, sys.stdin)):
    if item.__class__ != cur_type and cur_type != None:
      sess.commit()
    cur_type = item.__class__
    sess.add(item)
  sess.commit()
  sess.close()

if __name__ == '__main__':
  import sys
  eval(sys.argv[1])(*sys.argv[2:])
