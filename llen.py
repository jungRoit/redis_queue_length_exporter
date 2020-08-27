from prometheus_client import make_wsgi_app, Gauge
from wsgiref.simple_server import make_server
import redis,sys,json

with open('queue.json', 'r') as data_file:
        json_data = data_file.read()

data = json.loads(json_data)

host = data['hosts']
g = Gauge('redis_List_length', 'Length of List', ['host','list'])

def generate():
    for h, q_type in host.items():
        s = h.split(':')
        r = redis.Redis(host=s[0], port=s[1])
        print(g)
        print(r)
        try:
            r.ping()            
        except redis.ConnectionError:
            print("Cannot make connection to " +s[0]+":"+s[1])
            continue

        for q in q_type:
            print("q is ")
            print(q)
            # qlist = data['queue_type'][q]
            a = r.llen(q)
            print(a)
            g.labels(h,q).set(a)
            print('stats')
            print(g)
            # for qname in qlist:
            #     print("qname is ")
            #     print(qname)
            #     a = r.llen(qname)
            #     g.labels(h,qname,q).set(a)
            #     print(g)


metrics_app = make_wsgi_app()

def my_app(environ, start_fn):
    print('started')
    if environ['PATH_INFO'] == '/metrics':
        print('started')
        generate()
        print('generate complete')
        return metrics_app(environ, start_fn)

httpd = make_server('', 8000, my_app)
httpd.serve_forever()
