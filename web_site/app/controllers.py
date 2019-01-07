import datetime

from flask import Blueprint, make_response, jsonify, request, abort
from flask import render_template

from web_site.app.models import History, Product
from main import CrawlRunner

module = Blueprint('', __name__, url_prefix='/')


@module.route('/', methods=['GET'])
def index(**kwargs):
    return make_response(open('app/templates/index.html').read())


@module.route('/crawler', methods=['GET'])
def run(**kwargs):
    query = request.args.get('query')

    history = History(query=query, created_date=datetime.datetime.now())
    history.save()

    try:
        cr = CrawlRunner(query=query, history=history.id)
        cr.run_spider()

        pipeline = [
            {
                '$group': {
                    '_id': '$resource',
                    'products': {
                        '$push': {'name': '$name', 'url': '$url', 'price': '$price'}
                    },
                    # 'minPrice': {
                    #     '$min': '$price'
                    # }
                }
            },
            # {
            #     "$sort": {"products.price": 1}
            # }
        ]

        data = Product.objects(history=history).aggregate(*pipeline)

        return jsonify({'data': list(data)})
    except Exception:
        raise Exception("Error")
        # abort(500)


@module.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
