# coding: utf-8
#
# This file is part of Supysonic.
# Supysonic is a Python implementation of the Subsonic server API.
#
# Copyright (C) 2017-2018 Alban 'spl0k' Féron
#
# Distributed under terms of the GNU AGPLv3 license.

import inspect
import os
import shutil
import unittest
import tempfile

from pony.orm import db_session

from supysonic.db import init_database, release_database
from supysonic.config import DefaultConfig
from supysonic.managers.user import UserManager
from supysonic.scanner_master import ScannerClient
from supysonic.web import create_application, shutdown_scanner

class TestConfig(DefaultConfig):
    TESTING = True
    LOGGER_HANDLER_POLICY = 'never'
    MIMETYPES = {
        'mp3': 'audio/mpeg',
        'weirdextension': 'application/octet-stream'
    }
    TRANSCODING = {
        'transcoder_mp3_mp3': 'echo -n %srcpath %outrate',
        'decoder_mp3': 'echo -n Pushing out some mp3 data...',
        'encoder_cat': 'cat -',
        'encoder_md5': 'md5sum'
    }

    def __init__(self, with_webui, with_api):
        super(TestConfig, self).__init__()

        for cls in reversed(inspect.getmro(self.__class__)):
            for attr, value in cls.__dict__.items():
                if attr.startswith('_') or attr != attr.upper():
                    continue

                if isinstance(value, dict):
                    setattr(self, attr, value.copy())
                else:
                    setattr(self, attr, value)

        self.WEBAPP.update({
            'mount_webui': with_webui,
            'mount_api': with_api
        })

class MockResponse(object):
    def __init__(self, response):
        self.__status_code = response.status_code
        self.__data = response.get_data(as_text = True)
        self.__mimetype = response.mimetype

    @property
    def status_code(self):
        return self.__status_code

    @property
    def data(self):
        return self.__data

    @property
    def mimetype(self):
        return self.__mimetype

def patch_method(f):
    original = f
    def patched(*args, **kwargs):
        rv = original(*args, **kwargs)
        return MockResponse(rv)

    return patched

class TestBase(unittest.TestCase):
    __with_webui__ = False
    __with_api__ = False

    def setUp(self):
        self.__dbfile = tempfile.mkstemp()[1]
        self.__dir = tempfile.mkdtemp()
        config = TestConfig(self.__with_webui__, self.__with_api__)
        config.BASE['database_uri'] = 'sqlite:///' + self.__dbfile
        config.WEBAPP['cache_dir'] = self.__dir

        init_database(config.BASE['database_uri'])
        release_database()

        self.__app = create_application(config)
        self.client = self.__app.test_client()

        with db_session:
            UserManager.add('alice', 'Alic3', 'test@example.com', True)
            UserManager.add('bob', 'B0b', 'bob@example.com', False)

    def _patch_client(self):
        self.client.get = patch_method(self.client.get)
        self.client.post = patch_method(self.client.post)

    def request_context(self, *args, **kwargs):
        return self.__app.test_request_context(*args, **kwargs)

    def tearDown(self):
        shutdown_scanner()
        release_database()
        shutil.rmtree(self.__dir)
        os.remove(self.__dbfile)

