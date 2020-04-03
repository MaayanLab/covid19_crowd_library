import functools
from app.database import Session

def serve_datatable(qs, cols, search_filter):
  def route(qs, draw=0, start=0, length=100, order=[], search={}, **kwargs):
    sess = Session()

    draw = int(draw)
    start = int(start)
    length = int(length)
    
    qs = qs(sess)

    if type(search) == dict and 'value' in search:
      filtered_qs = qs.filter(
        search_filter(search['value'])
      )
    else:
      filtered_qs = qs
    
    if type(order) == list:
      ordered_qs = filtered_qs.order_by(*[
        cols[int(o['column'])][0] if o['dir'] == 'asc' else cols[int(o['column'])][0].desc()
        for o in order
      ])
    else:
      ordered_qs = filtered_qs
    
    if length > 0:
      limited_qs = ordered_qs.offset(start).limit(length)
    else:
      limited_qs = ordered_qs.offset(start)

    result = {
      'draw': draw,
      'recordsTotal': qs.count(),
      'recordsFiltered': filtered_qs.count(),
      'data': [
        {
          cols[ind][1]: cell
          for ind, cell in enumerate(record)
        }
        for record in limited_qs
      ],
    }
    sess.close()
    return result

  return functools.partial(route, qs)
