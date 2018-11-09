#!/usr/bin/env python3.6

import json
import os
import shutil
from shutil import copyfile
from tkinter import *

port_list = []
service_list = []

directory = os.getcwd()

service_manager_config_location = "/home/damien/service-manager-config/services.json"

#graph types
#dot
#neato
#twopi
#circo
#fdp
#sfdp
#patchwork
#osage

graph_type = "\"neato\";"

if os.path.isfile("graphviz.dot"):
    os.remove("graphviz.dot")

graphviz_file = open("graphviz.dot", "w+")

graphviz_file.write("digraph sample {" + "\n" + "")
graphviz_file.write(
    "graph [pad=\"0.5\", nodesep=\"20\", ranksep=\"4\"]; layout=" + graph_type + "splines=\"true\"; overlap=\"false\"; "
    "size=\"500000,500000\"" + "\n")

if os.path.exists('dependencyTreeTempDirectory'):
    shutil.rmtree('dependencyTreeTempDirectory')

os.mkdir('dependencyTreeTempDirectory')


def check_ports_exists(reponame, port):
    file_path = os.path.join(directory, reponame + "/conf/application.conf")
    with open(file_path) as f:
        for line in f:
            if str(port) in line:
                print(reponame)
                print(line)


def get_micro_service_files():
    for directory_name, directories, files in os.walk(directory):
        for file_name in files:
            if file_name == "MicroService.scala":
                service_name = directory_name.split("/")[-2]
                file_path = os.path.join(directory_name, file_name)
                directory_name.replace(directory, '').replace('/conf', '').replace('/', '')
                copyfile(file_path, './dependencyTreeTempDirectory/' + service_name + '-microservice.scala')


def get_services():
    for directory_name, directories, files in os.walk('./dependencyTreeTempDirectory'):
        for file_name in files:
            service_name = file_name.replace("-microservice.scala", "")
            fpath = os.path.join(directory_name, file_name)
            with open(fpath) as f:
                lines = f.readlines()
                for line in lines:
                    if "name =" in line:
                        file_name.replace("-microservice.scala.git", "")
                        check_ports_exists(service_name, check_outgoing_calls(line.split('"')[1::2][0]))
            if len(port_list) > 0:
                for x in service_list:
                    t = x.split("/")[1].replace(".git", "")
                    if len(sys.argv) > 1:
                        if str(sys.argv[1]) in t:
                            graphviz_file.write("\"" + file_name.replace("-microservice.scala",
                                                                    "") + "\"" + " -> " + "\"" + t + "\"" + "\n")
                    else:
                        graphviz_file.write(
                            "\"" + file_name.replace("-microservice.scala", "") + "\"" + " -> " + "\"" + t + "\"" + "\n")
            port_list.clear()
            service_list.clear()

    graphviz_file.write("}")
    graphviz_file.close()


def check_outgoing_calls(service_manager_name):
    with open(service_manager_config_location) as json_data:
        services_json = json.load(json_data)
        for x in services_json:
            if x.upper() == service_manager_name.upper():
                for y in services_json[x]:
                    if y.upper() == "DEFAULTPORT":
                        port_list.append(str(services_json[x][y]))
                    if y.upper() == "SOURCES":
                        for t in services_json[x][y]:
                            if t.upper() == "REPO":
                                service_list.append(str(services_json[x][y][t]))


get_micro_service_files()
get_services()

os.chdir(directory)
os.system("chmod +777 graphviz.dot")

if os.path.isfile("image.png"):
    os.remove("image.png")

os.system("sfdp -Tpng graphviz.dot -o image.png")
os.system("xdg-open image.png")