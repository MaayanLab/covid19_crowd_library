import functools
from app.database import Session

def serve_datatable(qs, cols, search_filter, aggregator=None):
  ''' Create a server-side datatables route
  Example:
    myserved_datatable = serve_datatable(
      lambda sess: sess.query(Gene),
      [(Gene.symbol, 'symbol')],
      lambda search: Gene.symbol.like(val)
    )
    @app.route('/my_path', methods=['POST'])
    def my_path():
      return myserved_datatable(**json.loads(flask.request.values.get('body')))

  @param qs
    A function which returns a SQLAlchemy Queryset (superset)
     to base the response on given a SQLAlchemy session
  @param cols
    A list containing SQLAlchemy column to datatables name
     mappings in the order they appear on the frontend
  @param search_filter
    A function that accepts a search query and should return
     a SQLAlchemy filter clause

  @returns
    A function that prepares a response for the Datatables client-side table from the server.
     it requires a json representation of the body passed to its arguments.
  '''
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
      ] if aggregator is None else aggregator(limited_qs),
    }
    sess.close()
    return result

  return functools.partial(route, qs)
