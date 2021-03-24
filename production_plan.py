import heapq

powerplant_to_fuel = {"gasfired": "gas(euro/MWh)", "turbojet":
    "kerosine(euro/MWh)", "windturbine": "wind(%)"} #mapping of powerplant types to their respective fuel costs


def pwr_plt_pq(payload): #adds available powerplants to a priority queue (heap) sorted ascending by cost.
    result = []
    for pwr_plt in payload["powerplants"]:
        name = pwr_plt["name"]
        type = pwr_plt["type"]
        eff = payload["fuels"][powerplant_to_fuel[type]] * 0.01 if type == "windturbine" else pwr_plt["efficiency"]
        cost = 0 if type == "windturbine" else payload["fuels"][powerplant_to_fuel[type]] / pwr_plt["efficiency"]
        heapq.heappush(result, (cost, name, eff, pwr_plt["pmin"], pwr_plt["pmax"]))
    return result


def generate_production_plan(payload):
    load = payload["load"]
    pq = pwr_plt_pq(payload)
    result = []

    while len(pq) != 0:
        pwr_plt = heapq.heappop(pq)
        name = pwr_plt[1]
        pwr_efficiency = pwr_plt[2]
        min_pwr = pwr_plt[3] * pwr_efficiency
        max_pwr = pwr_plt[4] * pwr_efficiency

        if min_pwr <= load:
            if max_pwr <= load:  # add full power to load
                result.append({"name": name, "p": round(max_pwr, 4)})
                load = load - max_pwr
            else:  # add remaining required load to top off load
                result.append({"name": name, "p": round(load, 4)})
                load = 0
        else:  # skip
            result.append({"name": name, "p": 0})
    if load > 0:
        raise RuntimeError("Not enough available power to service required load. Available: " + str(
            round(payload["load"] - load)) + "/" + str(payload["load"]) + "MW")
    return result
