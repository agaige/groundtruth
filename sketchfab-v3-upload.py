#!/usr/bin/env python

# -*- coding: utf-8 -*-

##
# Sample script for uploading to Sketchfab
# using the V3 API and the requests library
##
import json
import os
import shutil

from time import sleep

# import the requests library
# http://docs.python-requests.org/en/latest
# pip install requests
import requests

##
# Uploading a model to Sketchfab is a two step process
#
# 1. Upload a model. If the upload is successful, the API will return
#    the model's uid in the `Location` header, and the model will be placed in the processing queue
#
# 2. Poll for the processing status
#    You can use your model id (see 1.) to poll the model processing status
#    The processing status can be one of the following:
#    - PENDING: the model is in the processing queue
#    - PROCESSING: the model is being processed
#    - SUCCESSED: the model has being sucessfully processed and can be view on sketchfab.com
#    - FAILED: the processing has failed. An error message detailing the reason for the failure
#              will be returned with the response
#
# HINTS
# - limit the rate at which you poll for the status (once every few seconds is more than enough)
##

SKETCHFAB_DOMAIN = 'sketchfab.com'
SKETCHFAB_API_URL = 'https://api.{}/v3'.format(SKETCHFAB_DOMAIN)

YOUR_API_TOKEN = ''

MODEL_PATH = './webgl/spicy_group.zip'


def _get_request_payload(data={}, files={}, json_payload=False):
    """Helper method that returns the authentication token and proper content
    type depending on whether or not we use JSON payload."""
    headers = {'Authorization': 'Token {}'.format(YOUR_API_TOKEN)}

    if json_payload:
        headers.update({'Content-Type': 'application/json'})
        data = json.dumps(data)

    return {'data': data, 'files': files, 'headers': headers}


def upload(reupload=False, model_id=None):
    """POST a model to sketchfab.

    This endpoint only accepts formData as we upload a file.
    """
    model_endpoint = os.path.join(SKETCHFAB_API_URL, 'models')
    _method = "POST"

    # Mandatory parameters
    model_file = MODEL_PATH  # path to your model

    # Optional parameters
    name = 'AVH Spicy'
    description = 'AVH Spicy'
    isPublished = False, # Model will be on draft instead of published
    isInspectable = True, # Allow 2D view in model inspector

    data = {
        'name': name,
        'description': description,
        'isPublished': isPublished,
        'isInspectable': isInspectable
    }
    if model_id is not None:
        data['uid'] = model_id

    if reupload:
        _method = "PUT"
        model_endpoint = os.path.join(model_endpoint, model_id)
        print 'Re-Uploading ...'
    else:
        print 'Uploading ...'

    f = open(model_file, 'rb')

    files = {'modelFile': f}




    try:
        r = requests.request(_method,
            model_endpoint, **_get_request_payload(
                data, files=files))
    except requests.exceptions.RequestException as e:
        print u'An error occured: {}'.format(e)
        return
    finally:
        f.close()

    if (r.status_code != requests.codes.created and
            r.status_code != requests.codes.no_content):
        print u'Upload failed with error: {}'.format(r.json())
        return

    # Should be https://api.sketchfab.com/v3/models/XXXX
    model_url = None
    if model_id:
        model_url = "https://api.sketchfab.com/v3/models/{}".format(model_id)
    elif 'Location' in r.headers:
        model_url = r.headers['Location']

    print 'Upload successful. Your model is being processed.'
    print 'Once the processing is done, the model will be available at: {}'.format(
        model_url)

    return model_url


def poll_processing_status(model_url):
    """GET the model endpoint to check the processing status."""
    max_errors = 10
    errors = 0
    retry = 0
    max_retries = 50
    retry_timeout = 5  # seconds

    print 'Start polling processing status for model'

    while (retry < max_retries) and (errors < max_errors):
        print 'Try polling processing status (attempt #{}) ...'.format(retry)

        try:
            r = requests.get(model_url, **_get_request_payload())
        except requests.exceptions.RequestException as e:
            print 'Try failed with error {}'.format(e)
            errors += 1
            retry += 1
            continue

        result = r.json()

        if r.status_code != requests.codes.ok:
            print 'Upload failed with error: {}'.format(result['error'])
            errors += 1
            retry += 1
            continue

        processing_status = result['status']['processing']

        if processing_status == 'PENDING':
            print 'Your model is in the processing queue. Will retry in {} seconds'.format(
                retry_timeout)
            print 'Want to skip the line? Get a pro account! https://sketchfab.com/plans'
            retry += 1
            sleep(retry_timeout)
            continue
        elif processing_status == 'PROCESSING':
            print 'Your model is still being processed. Will retry in {} seconds'.format(
                retry_timeout)
            retry += 1
            sleep(retry_timeout)
            continue
        elif processing_status == 'FAILED':
            print 'Processing failed: {}'.format(result['error'])
            return False
        elif processing_status == 'SUCCEEDED':
            print 'Processing successful. Check your model here: {}'.format(
                model_url)
            return True

        retry += 1

    print 'Stopped polling after too many retries or too many errors'
    return False


def patch_model(model_url):
    """PATCH the model endpoint to update its name, description ...

    Important: The call uses a JSON payload.
    """

    data = {'name': 'AVH Spicy'}

    try:
        r = requests.patch(
            model_url, **_get_request_payload(
                data, json_payload=True))
    except requests.exceptions.RequestException as e:
        print u'An error occured: {}'.format(e)
    else:
        if r.status_code != 204:
            print u'PATCH model failed with error: {}'.format(r.content)
        else:
            print u'PATCH model successful.'


def patch_model_options(model_url):
    """PATCH the model options endpoint to update the model background, shading,
    orienration."""
    options_url = os.path.join(model_url, 'options')

    data = {
        'shading': 'shadeless',
        'background': '{"color": "#FFFFFF"}',
        # For axis/angle rotation:
        #'orientation': '{"axis": [1, 1, 0], "angle": 34}',
        # Or for 4x4 matrix rotation:
        # 'orientation': '{"matrix": [1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]}'
    }

    try:
        r = requests.patch(
            options_url, **_get_request_payload(
                data, json_payload=True))
    except requests.exceptions.RequestException as e:
        print u'An error occured: {}'.format(e)
    else:
        if r.status_code != 204:
            print u'PATCH options failed with error: {}'.format(r.content)
        else:
            print u'PATCH options successful.'


###################################
# Zips, Uploads, polls and patch a model
###################################

if __name__ == "__main__":
    basename = os.path.basename(MODEL_PATH)
    ret = shutil.make_archive(os.path.splitext(MODEL_PATH)[0],
                              'zip',
                              os.path.splitext(MODEL_PATH)[0])

    model_url = upload(reupload=True,
                       model_id='e458ffaef2ab4f369b12ac56702b283f')

    if model_url:
        if poll_processing_status(model_url):
            patch_model(model_url)
            #patch_model_options(model_url)