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
import yaml
from git import Repo, GitCommandError
import os
from sets import Set

__author__ = 'lto,ogo'

log = logging.getLogger(__name__)
logging_dir = '/var/log/openbaton/'
# the environmental variable SCRIPTS_PATH is set everytime the script-path was contained in the json message, you can use after you cloned or saved the script
scripts_path = "/opt/openbaton/scripts"
ob_parameters_file_name = "ob_parameters"

def save_scripts(dict_msg):
    log.info("Recevied save scripts command")
    payload = dict_msg.get('payload')
    path = dict_msg.get('script-path')
    try:
        script = base64.b64decode(payload)

        if path is None:
            log.info("No path provided, saving into default directory")
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
        log.error("Incorrect script encoding")
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
    payload = dict_msg.get('payload')
    path = dict_msg.get('script-path')
    os.environ['SCRIPTS_PATH'] = path
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


def save_vnf_parameters(parameters_file_path_bash, vnf_parameters):
    log.info("Reading VNF Parameters")
    with open(parameters_file_path_bash, 'a+') as f:
        f.write("# VNF Parameters\n")

        for vnf_type in vnf_parameters.keys():
            log.debug("Reading VNF Parameters of VNF type: " + vnf_type)
            vnf_param_str = "export OB_" + vnf_type + "_VNF_"
            internal_parameters = vnf_parameters.get(vnf_type).get('parameters')

            for vnf_parameter_key in internal_parameters.keys():
                vnf_param_str += vnf_parameter_key + "=" + internal_parameters.get(vnf_parameter_key) + "\n"
                log.debug(vnf_param_str)
                f.write(vnf_param_str)

        f.flush()
        os.fsync(f.fileno())


def save_vnfc_parameters(parameters_file_path_bash, vnfc_parameters):
    log.info("Reading VNFC Parameters")
    with open(parameters_file_path_bash, 'a+') as f:
        f.write("\n# VNFC Parameters\n")

        # create a list of vnfc parameters existing in at least one vnfc of the same vnf_type
        all_vnfc_parameter_keys_for_vnf_type = {}
        for vnf_type in vnfc_parameters.keys():
            all_vnfc_parameter_keys_for_vnf_type[vnf_type] = Set([])
            for vnfc_id_for_vnf_type, vnfc_content_for_vnf_type in vnfc_parameters.get(vnf_type).get(
                    'parameters').iteritems():
                parameters = vnfc_content_for_vnf_type.get('parameters')
                for parameter_key in parameters.keys():
                    all_vnfc_parameter_keys_for_vnf_type[vnf_type].add(parameter_key)

        all_vnfc_parameters = {}
        for vnf_type in vnfc_parameters.keys():
            log.debug("Reading VNFC parameters of VNF type: " + vnf_type + " which keys are:")
            log.debug(all_vnfc_parameter_keys_for_vnf_type[vnf_type])

            all_vnfc_parameters_for_vnf_type = {}
            for parameter_key in all_vnfc_parameter_keys_for_vnf_type[vnf_type]:
                log.debug("Reading values for VNFC parameter key: " + parameter_key)
                vnfc_param_str = "export OB_" + vnf_type + "_VNFC_" + parameter_key + "="

                # initialise list for values of a vnfc parameter key
                if all_vnfc_parameters_for_vnf_type.get(parameter_key) is None:
                    all_vnfc_parameters_for_vnf_type.setdefault(parameter_key, [])

                # read the values of each vnfc parameter of each vnf_type ...
                for vnfc_content_for_vnf_type in vnfc_parameters.get(vnf_type).get('parameters').values():
                    parameters = vnfc_content_for_vnf_type.get('parameters')

                    # ... and for each parameter_key adds:
                    #  - the vnfc parameter value, if this vnfc has this parameter
                    #  - a "NA" value, otherwise
                    if parameter_key in parameters.keys():
                        vnfc_parameter_value = parameters.get(parameter_key)
                    else:
                        vnfc_parameter_value = "NA"
                    all_vnfc_parameters_for_vnf_type.get(parameter_key).append(vnfc_parameter_value)
                    vnfc_param_str += vnfc_parameter_value + ":"

                # remove last ':'
                vnfc_param_str = vnfc_param_str[:-1] + "\n"
                log.debug(vnfc_param_str)
                f.write(vnfc_param_str)

            all_vnfc_parameters[vnf_type] = all_vnfc_parameters_for_vnf_type

        f.flush()
        os.fsync(f.fileno())



def save_vnfr_dependency(dict_msg):
    log.info("Saving VNFR configuration and dependency parameters")
    # get the base path where to save the file
    parameters_file_path_base_dir = dict_msg.get('script-path')
    parameters_file_path_base = parameters_file_path_base_dir + "/" + ob_parameters_file_name

    # create file path for yaml, json and bash
    parameters_file_path_json = parameters_file_path_base + ".json"
    parameters_file_path_yaml = parameters_file_path_base + ".yaml"
    parameters_file_path_bash = parameters_file_path_base + ".sh"

    # get vnfr_dependency json (as string)
    vnfr_dependency = dict_msg.get('payload')

    # save to file as ob_parameters.json
    f = open(parameters_file_path_json, "w")
    f.write(vnfr_dependency)
    f.close()
    log.info("Saved file %s" % parameters_file_path_json)

    # convert the json to yaml and write to the file ob_parameters.yaml
    # get vnfr_dependency json (as json object)
    vnfr_dependency = json.loads(vnfr_dependency)
    f = open(parameters_file_path_yaml, "w")
    yaml.safe_dump(vnfr_dependency, f, allow_unicode=True, default_flow_style=False)
    f.close()
    log.info("Saved file %s" % parameters_file_path_yaml)

    # read json vnfr_dependency and save the parameters to the file ob_parameters.sh (to be sourced)
    vnf_parameters = vnfr_dependency.get('parameters')
    vnfc_parameters = vnfr_dependency.get('vnfcParameters')
    save_vnf_parameters(parameters_file_path_bash, vnf_parameters)
    save_vnfc_parameters(parameters_file_path_bash, vnfc_parameters)
    log.info("Saved file %s" % parameters_file_path_bash)

    out = str(os.listdir(parameters_file_path_base_dir))
    err = ""
    status = 0

    # return response
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
        log.info("Received a non-json object")
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
    elif action == "SAVE_VNFR_DEPENDENCY":
       return save_vnfr_dependency(dict_msg);

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
