from app import start
from waitress import serve

app = start()


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=8080, threads=10)

