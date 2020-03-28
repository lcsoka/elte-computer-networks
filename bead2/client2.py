import sys
import json

def find_link(links,start,end):
    for link in links:
        if ((link["points"][0] == start and link["points"][1] == end) or (link["points"][0] == end and link["points"][1] == start)):
            return link
    return None

def get_circuits(data,start,end):
    circuits = []
    for circuit in data:
        if(circuit[0] == start and circuit[len(circuit) - 1 ] == end):
            circuits.append(circuit)
    return circuits

def get_remaining_bandwidth(link):
    remaining = link["capacity"]
    if "demands" in link:
        for demand in link["demands"]:
            remaining = remaining - demand["demand"]
    return remaining

def allocate_route(route, links, demand, test=False):
    valid = True
    for i, _ in enumerate(route):
        if not i == 0:
            link = find_link(links,route[i - 1], route[i])
            remaining_bandwidth = get_remaining_bandwidth(link)
            if(remaining_bandwidth - demand["demand"] < 0):
                valid = False
            else:
                if not test:
                    if not "demands" in link:
                        link["demands"] = []
                    link["demands"].append(demand)
    return valid

def start_demand(demand,start,end):
    routes = get_circuits(data["possible-circuits"],start, end)
    if routes:
        success = False
        for route in routes:
            if not success:
                if allocate_route(route,data["links"],demand,True):
                    allocate_route(route,data["links"],demand)
                    print("igény foglalás: {}<->{} st:{} - sikeres".format(start,end,i+1))
                    success = True
        if not success:
            print("igény foglalás: {}<->{} st:{} - sikertelen".format(start,end,i+1))

def close_demad(demand,start,end):
    succcess = False
    for link in data["links"]:
        if "demands" in link and demand in link["demands"]:
            link["demands"].remove(demand)
            if not link["demands"]:
                del link["demands"]
            succcess = True
    if succcess:
        print("igény felszabadítás: {}<->{} st:{}".format(start,end,i+1))

def iterate(i):
    for demand in data["simulation"]["demands"]:
        start = demand["end-points"][0]
        end = demand["end-points"][1]
        if demand["start-time"] == i+1:
            start_demand(demand,start,end)
        if demand["end-time"] == i+1:
            close_demad(demand,start,end)

with open(sys.argv[1], "r") as file:
    data = json.load(file)
    for i in range(data["simulation"]["duration"]):
        iterate(i)