import json
import sys

def get_possible_circutis(circuits,start,end):
    result = []
    if (start in data["end-points"]) == False or (end in data["end-points"]) == False:
        # Invalid endpoint
        return []
    
    for circuit in circuits:
        if(circuit[0] == start and circuit[len(circuit) - 1 ] == end):
        # if(circuit[0] == start and circuit[len(circuit) - 1 ] == end) or (
        #     circuit[0] == end and circuit[len(circuit) - 1] == start):
            result.append(circuit)
    return result

def get_remaining_bandwidth(link):
    remaining = link["capacity"]

    if "demands" in link:
        for demand in link["demands"]:
            remaining = remaining - demand["demand"]
    return remaining

def find_link(links,start,end):
    for link in links:
        if (link["points"][0] == start and link["points"][1] == end) or (link["points"][0] == end and link["points"][1] == start):
            return link
    return None

def allocate_route(route, links, demand, check=False):
    valid = True
    for index, val in enumerate(route):
        if not index == 0:
            link = find_link(links,route[index - 1], route[index])
            remaining_bandwidth = get_remaining_bandwidth(link)
            # print(str(link))
            # print("remaining bandwidth: " + str(remaining_bandwidth))
            if(remaining_bandwidth - demand["demand"] < 0):
                # print("Not enough bandwidth" + str(link))
                valid = False
            else:
                if not check:
                    if not "demands" in link:
                        link["demands"] = []
                    link["demands"].append(demand)
    return valid

def step(i):
    # print("current step: "+str(i+1))

    for demand in data["simulation"]["demands"]:
        start = demand["end-points"][0]
        end = demand["end-points"][1]
        if demand["start-time"] == i+1:
            # start demand 

            routes = get_possible_circutis(data["possible-circuits"],start, end)
            
            if routes:
                allocated = False #Store if this demand has allocated bandwidth
                for route in routes:
                    # print("Checking route "+ str(route))
                    if not allocated:
                        if allocate_route(route,data["links"],demand,True):
                            allocate_route(route,data["links"],demand)
                            # print(str(route))
                            print("igény foglalás: {0}<->{1} st:{2} - sikeres".format(start,end,i+1))
                            allocated = True
                if not allocated:
                    print("igény foglalás: {0}<->{1} st:{2} - sikertelen".format(start,end,i+1))
        if demand["end-time"] == i+1:
            # try to close demand
            successful_deallocate = False
            for link in data["links"]:
                if "demands" in link and demand in link["demands"]:
                    link["demands"].remove(demand)
                    if not link["demands"]:
                        del link["demands"]
                    successful_deallocate = True
            if successful_deallocate:
                print("igény felszabadítás: {0}<->{1} st:{2}".format(start,end,i+1))
    # print(json.dumps(data["links"],indent=2))


with open(sys.argv[1], "r") as f:
    data = json.load(f)

    # print(get_possible_circutis(data["possible-circuits"],"A","C"))

    for i in range(data["simulation"]["duration"]):
        step(i)
    