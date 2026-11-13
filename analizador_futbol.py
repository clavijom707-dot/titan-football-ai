def obtener_partidos_liga(slug_liga):
    url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{slug_liga}/scoreboard?limit=100"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            partidos = []
            meses = {1: "Ene", 2: "Feb", 3: "Mar", 4: "Abr", 5: "May", 6: "Jun", 7: "Jul", 8: "Ago", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dic"}
            
            # Calculamos la hora exacta de "ahora"
            ahora = datetime.datetime.now().timestamp()
            
            for ev in data.get("events", []):
                competencias = ev.get("competitions", [])
                if competencias:
                    competidores = competencias[0].get("competitors", [])
                    if len(competencias[0].get("competitors", [])) == 2:
                        eq1 = competencias[0].get("competitors", [])[0].get("team", {}).get("displayName", "TBD")
                        eq2 = competencias[0].get("competitors", [])[1].get("team", {}).get("displayName", "TBD")
                        fecha_str = ev.get("date", "")
                        hora_formateada = "Hora TBD"
                        timestamp = 0
                        
                        if fecha_str:
                            try:
                                dt = datetime.datetime.fromisoformat(fecha_str.replace("Z", "+00:00"))
                                dt_ec = dt - datetime.timedelta(hours=5)
                                hora_formateada = f"{dt_ec.day} {meses[dt_ec.month]} - {dt_ec.strftime('%H:%M')}"
                                timestamp = dt.timestamp()
                            except: pass
                        
                        # AQUÍ ESTÁ EL TRUCO: Solo agregamos el partido si su hora es mayor a la de ahora
                        if timestamp > ahora:
                            partidos.append({"local": eq1, "visitante": eq2, "fecha_hora": hora_formateada, "timestamp": timestamp})
            
            partidos.sort(key=lambda x: x['timestamp'])
            return partidos
    except Exception: return None
