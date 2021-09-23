from app import app


@app.route('/test')
def test():
    return '<h1>Hello test</h1>'
