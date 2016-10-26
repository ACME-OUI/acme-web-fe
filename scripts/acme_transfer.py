#!/usr/bin/env python

import os, sys, json
from optparse import OptionParser
from datetime import datetime, timedelta
import time
from globusonline.transfer import api_client
from globusonline.transfer.api_client import Transfer
from globusonline.transfer.api_client import TransferAPIClient
from globusonline.transfer.api_client import TransferAPIError
from globusonline.transfer.api_client import x509_proxy
from globusonline.transfer.api_client.goauth import get_access_token


config = None


def activate_endpoint(api_client, endpoint):
    code, reason, result = api_client.endpoint_autoactivate(endpoint, if_expires_in=2880)
    if result["code"] == "AutoActivationFailed":
        reqs = result
        myproxy_hostname = None
        for r in result['DATA']:
            if r['type'] == 'myproxy' and r['name'] == 'hostname':
                myproxy_hostname = r['value']
        reqs.set_requirement_value("myproxy", "hostname", myproxy_hostname)
        reqs.set_requirement_value("myproxy", "username", config['credential'][endpoint]['username'])
        reqs.set_requirement_value("myproxy", "passphrase", config['credential'][endpoint]['password'])
        reqs.set_requirement_value("myproxy", "lifetime_in_hours", "168")
        code, reason, result = api_client.endpoint_activate(endpoint, reqs)
        if code != 200:
            msg = "Could not activate the endpoint: %s. Error: %s - %s" % (endpoint, result["code"], result["message"])
            print msg


def get_destination_path(srcpath, dstpath, recursive):
    '''
    If destination path is a directory (ends with '/') adds source file name to the destination path.
    Otherwise, Globus will treat the destination path as a file in spite of it is a directory in fact.
    '''
    if srcpath:
        if not recursive:
            if dstpath.endswith('/'):
                basename = os.path.basename(srcpath)
                return dstpath + basename
    return dstpath


def transfer(options):

    # Map legacy endpoint names to UUIDs
    srcendpoint = options.srcendpoint
    dstendpoint = options.dstendpoint
    if '#' in srcendpoint:
        srcendpoint = config['endpoint'][srcendpoint]
    if '#' in dstendpoint:
        dstendpoint = config['endpoint'][dstendpoint]

    # Get access token (This method of getting an acces token is deprecated and should be replaced by OAuth2 calls).
    auth_result = get_access_token(config['globus']['username'], config['globus']['password'])

    # Create a transfer submission
    api_client = TransferAPIClient(config['globus']['username'], goauth=auth_result.token)
    activate_endpoint(api_client, srcendpoint)
    activate_endpoint(api_client, dstendpoint)

    code, message, data = api_client.transfer_submission_id()
    submission_id = data["value"]
    deadline = datetime.utcnow() + timedelta(days=10)
    transfer_task = Transfer(submission_id, srcendpoint, dstendpoint, deadline)

    # Add srcpath to the transfer task
    if options.srcpath:
        transfer_task.add_item(options.srcpath,
                get_destination_path(options.srcpath, options.dstpath, options.recursive),
                recursive=options.recursive)
    # Add srclist to the transfer task
    if options.srclist:
        with open(options.srclist) as f:
            srcpath = f.readline().rstrip('\n')
            transfer_task.add_item(srcpath,
                get_destination_path(srcpath, options.dstpath, options.recursive),
                recursive=options.recursive)

    # Start the transfer
    task_id = None
    try:
        code, reason, data = api_client.transfer(transfer_task)
        task_id = data["task_id"]
        print 'task_id %s' % task_id
    except Exception as e:
        msg = "Could not submit the transfer. Error: %s" % str(e)
        sys.exit(1)

    # Check a status of the transfer every minute (60 secs)
    while True:
        code, reason, data = api_client.task(task_id)
        if data['status'] == 'SUCCEEDED':
            print 'progress %d/%d' % (data['files_transferred'], data['files'])
            return ('success', '')
        elif data['status'] == 'FAILED':
            return ('error', data['nice_status_details'])
        elif data['status'] == 'ACTIVE':
            print 'progress %d/%d' % (data['files_transferred'], data['files'])
        time.sleep(10)


if __name__ == '__main__':

    parser = OptionParser()
    parser.add_option('--source-endpoint', dest='srcendpoint', help='Source endpoint. Source endpoint should be a UUID. If is it a legacy name, a mapping from the legacy name to a UUID should be in config.json. Path can point to a file or a directory.')
    parser.add_option('--source-path', dest='srcpath', help='Source path. Source path can point to a file or a directory.')
    parser.add_option('--source-list', dest='srclist', help='File with a list of all source paths.')
    parser.add_option('--destination-endpoint', dest='dstendpoint', help='Destination endpoint.')
    parser.add_option('--destination-path', dest='dstpath', help='Destination path')
    parser.add_option('-r', '--recursive', dest='recursive', action='store_true', default=False, help='Indicates that \'source\' is a directory')
    parser.add_option('-c', '--config', dest='config', default='config.json', help='Path to a configuration file with credentials and legacy endpoint names to UUID mappings. By default, config.json is used')

    (options, args) = parser.parse_args()
    if not options.srcendpoint or not (options.srcpath or options.srclist) or not options.dstendpoint or not options.dstpath:
        parser.print_help()
        sys.exit(1)

    cfg_file = open(options.config, 'r')
    config = json.load(cfg_file)

    status, msg = transfer(options)
    if status == 'success':
        sys.exit(0)
    print '%s %s' % (status, msg)
    sys.exit(1)

