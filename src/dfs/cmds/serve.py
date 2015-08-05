from dfs.config import Config
from dfs.version import Version

from flask import Flask, Response, make_response, request
from werkzeug.routing import Rule
from functools import wraps

import os, json, sys, hashlib

class MyFlask(Flask):
    def __init__(self, *args, **kwargs):
        super(MyFlask, self).__init__(*args, **kwargs)
        self._values = {'target': "/tmp/dfs/volume1.dfs"}
        self._metadata = {}
        self._hl = hashlib.md5()
        self._offset = 0
        self._read_handle = None
        self._write_handle = None

    def set_target_value(self, value):
        self._values['target'] = value

    def get_target_value(self):
        return self._values['target']

    def set_metadata(self, file, content, content_length, offset):
        self._hl.update(content)
        h = self._hl.hexdigest()
        self._metadata[h] = {'filename': file.filename, 'size': content_length,
            'offset': offset, 'type': file.content_type}
        return h

    def get_metadata(self, hash_id):
        if hash_id in self._metadata:
            return self._metadata[hash_id]
        return None

    def get_offset(self):
        return self._offset

    def inc_offset(self, offset):
        self._offset += offset

    def get_write_handle(self):
        if self._write_handle == None:
            self._write_handle = open(self._values['target'], "r+b")
        return self._write_handle

    def get_read_handle(self):
        if self._read_handle == None:
            self._read_handle = open(self._values['target'], "rb")
        return self._read_handle


    # def get_metadata(self, hash):
    #     return

    # def set_metadata(self, filename, ):
    #     self._hl.update(metadata)
    #     return self._metadata[h] = metadata

# http server
application = MyFlask(__name__)
application.url_map.add(Rule('/file/append', endpoint="file#append"))
application.url_map.add(Rule('/file/read', endpoint="file#read"))
application.config['PROPAGATE_EXCEPTIONS'] = True



class Serve(object):

    def __init__(self):
        self._config = Config()
        self._errors = []
        # http endpoints


    def validate(self):
        self._opts = self._config.get_opts()[1:]
        if len(self._opts) != 1:
            self._errors.append("serve: no target provided (try -h)")
            return
        t = self._opts[0]
        application.set_target_value("/tmp/dfs/volume1.dfs")
        f = self._config.get_args().force
        # check if target does not exist
        if not os.path.isfile(t):
            self._errors.append("serve: target does not exist (try -h)")
            return
        # TODO: check integrity?

    def has_errors(self):
        return len(self._errors) > 0

    def get_errors_str(self):
        return ",".join(self._errors)

    def is_enabled(self):
        return True

    def get_help(self):
        return " serve <target> \t\trun local debug server"

    def run(self):
        # TODO: run server
        try:
            application.run(debug = True, host='0.0.0.0')
        except ValueError as e:
            print e
        pass

class Endpoints(object):

    headers = {'Content-Type': 'application/json; charset=utf-8',
        'Server': 'dfs/%s' % Version.VERSION}

    @application.endpoint('file#append')
    # @add_response_headers(headers)
    def _file_append(methods=["POST"]):
        resp = Response(json.dumps({}))
        resp.headers = Endpoints.headers
        # deny chunked uploads
        if 'Transfer-Encoding' in request.headers:
            if request.headers['Transfer-Encoding'] == "chunked":
                resp.status_code = 400
                resp.response = json.dumps({'error': {'code': 400, 'msg': "cannot handle chunked uploads"}})
                return resp
        t = application.get_target_value()
        # process each file in request
        ret = []
        for f in request.files.getlist('file[]'):
            with open(t, 'r+b') as h:
                offset = application.get_offset()
                h.seek(offset)
                content = f.stream.read()
                content_length = len(content)
                application.inc_offset(content_length)
                hash_id = application.set_metadata(f, content, content_length, offset)
                h.write(content)
                ret.append({"filename": f.filename, "hash_id": hash_id})
        resp.response = json.dumps({"files": ret})
        return resp

    @application.endpoint('file#read')
    # @add_response_headers(headers)
    def _file_read(methods=["GET"]):
        resp = Response(json.dumps({}))
        resp.headers = Endpoints.headers

        hash_id = request.args.get('hash_id', None)
        if hash_id == None:
            resp.status_code = 404
            resp.response = json.dumps({'error': {'code': 404, "msg": "not found"}})
            return resp
        metadata = application.get_metadata(hash_id)
        if metadata == None:
            resp.status_code = 500
            resp.response = json.dumps({'error': {'code': 500, "msg": "not found"}})
            return resp
        t = application.get_target_value()
        resp.headers['Content-Type'] = metadata['type']

        h = application.get_read_handle()
        h.seek(metadata['offset'])
        resp.response = h.read(metadata['size'])
        # h.close()
        return resp

