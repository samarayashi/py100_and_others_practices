from flask import Flask, jsonify, request
import constants
import parse_utils
import filter_utils

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route("/all")
def get_all_data():
    pass


@app.route("/search")
def search_data():

    field_search_dict = request.args.to_dict()
    files_iter = parse_utils.iter_combined_files(constants.fpaths, constants.land_class_name)
    filter_iter = filter_utils.fields_filter(files_iter, **field_search_dict)

    land_list = []
    for land in filter_iter:
        land_list.append(land._asdict())
    response = jsonify({"conditions": field_search_dict,
                       "lands": land_list})
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
