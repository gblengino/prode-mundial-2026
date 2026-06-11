def calculate_group_table(matches, teams):
    table = {} # Inicializa una tabla (list dict)

    for team in teams: # Formatea cada equipo de la lista de equipos
        table[team.id] = {
            "team": team.fifa_code,
            "team_flag": team.flag_url,
            "pts": 0,
            "gf": 0,
            "ga": 0,
            "gd": 0,
            "played": 0,
        }
    
    for match in matches: # Asigna los resultados de los partidos a los equipos
        if match.home_score is None: # Si no esta cargado el resultado, pasa de largo
            continue

            # Matchea los equipos por su id en la tabla
        home = table[match.home_team.id]
        away = table[match.away_team.id]

            # Obtiene los valores de los goles de cada equipo en el partido
        hs = match.home_score
        as_ = match.away_score

            # Asigna los goles a favor y en contra del local
        home["gf"] += hs
        home["ga"] += as_

            # Asigna goles a favor y en contra del visitante
        away["gf"] += as_
        away["ga"] += hs

            # Agrega +1 a los partidos jugados
        home["played"] += 1
        away["played"] += 1

            # Distribuye los puntos segun el resultado del partido
        if hs > as_:
            home["pts"] += 3
        elif as_ > hs:
            away["pts"] += 3
        else:
            home["pts"] += 1
            away["pts"] += 1

        # Calcula la diferencia de goles
    for t in table.values():
        t["gd"] = t["gf"] - t["ga"]

    return sorted(
        table.values(),
        key=lambda x: (x["pts"], x["gd"], x["gf"]),
        reverse=True
    )