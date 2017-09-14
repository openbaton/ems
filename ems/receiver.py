# Copyright (c) 2015 Fraunhofer FOKUS. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#





import base64
import json
import logging
import subprocess
import traceback
from git import Repo, GitCommandError
import os

__author__ = 'lto,ogo'

log = logging.getLogger(__name__)
logging_dir = '/var/log/openbaton/'
# the environmental variable SCRIPTS_PATH is set everytime the script-path was contained in the json message, you can use after you cloned or saved the script
scripts_path = "/opt/openbaton/scripts"

def save_scripts(dict_msg):
    log.info("Recevied save scripts command")
    payload = dict_msg.get('payload')
    path = dict_msg.get('script-path')
    try:
        script = base64.b64decode(payload)

        if path is None:
            log.info("No path provided, saving into default directory")
            print "No path provided, saving into default directory"
            path = scripts_path
        if not os.path.exists(path):
            os.makedirs(path)
        name = dict_msg.get('name')
        if path[-1] == "/":
            path_name = path + name
        else:
            path_name = path + "/" + name
        os.environ['SCRIPTS_PATH'] = path
        f = open(path_name, "w")
        f.write(script)
        # log.info("Written %s into %s" % (script, path_name))
        out = str(os.listdir(path))
        err = ""
        status = 0
        st = os.stat(path)
        os.chmod(path, st.st_mode | 0111)
        st = os.stat(path_name)
        os.chmod(path_name, st.st_mode | 0111)
    except TypeError:  # catches typeerror in case of the message not being properly encoded
        print "Incorrect script encoding"
        action = None
        out = None
        err = "Incorrect script encoding"
        status = "1"
    return generate_response(out=out, err=err, status=status)


def clone_scripts(dict_msg):
    payload = dict_msg.get('payload')
    path = dict_msg.get('script-path')
    if path is None:
        path = scripts_path
    url = payload
    os.environ['SCRIPTS_PATH'] = path
    log.info("Cloning from: %s into %s" % (url, path))
    try:
        Repo.clone_from(url, path)
        print 'Cloned'
        log.info('Cloned')
        for file in os.listdir(path):
            st = os.stat(path + "/" + file)
            os.chmod(path + "/" + file, st.st_mode | 0111)
        out = str(os.listdir(path))
        err = ""
        status = 0
    except GitCommandError as e:
        log.info("Encountered error while cloning")
        print 'Encountered error'
        err = traceback.format_exc()
        status = e.status
        out = None
    return generate_response(out=out, err=err, status=status)


def execute(dict_msg):
    log.info("Received execute command")
    payload = dict_msg.get('payload')
    if payload[-1] == "/":
        payload = scripts_path + payload
    else:
        payload = scripts_path + "/" + payload
    env = dict_msg.get('env')
    log.info("Executing: %s with env %s" % (payload, env))
    if env is None or len(env) == 0:
        env = None
    else:
        env.update(os.environ)
    ems_out_log = open('/var/log/openbaton/ems-out.log', "w+")
    ems_err_log = open('/var/log/openbaton/ems-err.log', "w+")
    if '.py' in payload:
        proc = subprocess.Popen(payload.split(), stdout=ems_out_log, stderr=ems_err_log, env=env)
    else:
        proc = subprocess.Popen(["/bin/bash"] + payload.split(), stdout=ems_out_log, stderr=ems_err_log, env=env)

    status = proc.wait()
    ems_out_log.seek(0)
    ems_err_log.seek(0)
    out = ems_out_log.read()
    err = ems_err_log.read()

    ems_out_log.close()
    ems_err_log.close()
    log.info("Executed: ERR: %s OUT: %s", err, out)
    return generate_response(out=out, err=err, status=status)


def repos_scripts_update(dict_msg):
    log.info("Updating scripts")
    payload = dict_msg.get('payload')
    url = payload
    try:
        Repo.pull(url, "/opt/openbaton/scripts/")
        log.info("Updated")
    except GitCommandError as e:
        log.info("Encountered error while updatign scripts")
        err = traceback.format_exc()
        status = e.status
        out = None
        return generate_response(out=out, err=err, status=status)
    else:
        out = str(os.listdir(scripts_path))
        err = ""
        status = 0
    return generate_response(out=out, err=err, status=status)


def scripts_update(dict_msg):
    log.info("Updating scripts")
    script_name = dict_msg.get('name')
    script_payload = base64.b64decode(payload)
    try:
        f = open(scripts_path + "/" + script_name, "w")
        f.write(script_payload)
        f.close()
        log.info("Updated file %s" % script_name)
    except GitCommandError as e:
        log.info("Encountered error while updating scripts")
        err = traceback.format_exc()
        status = e.status
        out = None
        return generate_response(out=out, err=err, status=status)
    else:
        out = str(os.listdir(scripts_path))
        err = ""
        status = 0
        return generate_response(out=out, err=err, status=status)


def on_message(message):
    logging.basicConfig(filename=logging_dir + '/ems-receiver.log', level=logging.INFO)
    # log.info('received a message: %s' % message)
    try:
        dict_msg = json.loads(message)
        try:
            log.info("Received message:")
            log.info(str(message))
        except:
            log.info("Error while logging")
        action = dict_msg.get('action')

        payload = dict_msg.get('payload')
    except ValueError:  # this section deals with the case when the message is not a json message and as a result cannot be processed. Considering that the messages are generated by the NFVO this is not supposed to happen
        log.info("Received an non json object")
        print "Not a json object"
        action = None
        out = None
        err = "Not a json message"
        status = "1"
    if action == 'SAVE_SCRIPTS':
       return save_scripts(dict_msg=dict_msg)
    if action == 'CLONE_SCRIPTS':
        return clone_scripts(dict_msg)
    elif action == "EXECUTE":
        return execute(dict_msg)
    elif action == "REPO_SCRIPTS_UPDATE":
        return repos_scripts_update(dict_msg)
    elif action == "SCRIPTS_UPDATE":
       return scripts_update(dict_msg)


def generate_response(out, err, status):
    if out is None:
        out = ""
    if err is None:
        err = ""
    resp = {
        'output': out,
        'err': err,
        'status': status
    }
    json_str = json.dumps(resp)
    log.info("answer is: " + json_str)
    return json_str
