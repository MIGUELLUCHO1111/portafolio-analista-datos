"""Construye y ejecuta analisis.ipynb. Uso: python construir_notebook.py"""
from pathlib import Path

import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor

AQUI = Path(__file__).parent
(AQUI / "graficos").mkdir(exist_ok=True)
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celdas = [
    md("# Producción y valor de los campos petroleros de Noruega\n"
       "**Pregunta de negocio:** ¿cómo evoluciona la producción de petróleo de la plataforma continental noruega, "
       "qué campos maduros sostienen el valor remanente y cuánto vale su producción futura según el precio del Brent?\n\n"
       "**Datos:** datos oficiales y abiertos de Sodir (producción mensual por campo desde 1971 y reservas) "
       "y precio mensual del Brent (FRED). Ver `datos/FUENTES.md`.\n\n"
       "**Herramientas:** Python, pandas, numpy y matplotlib. Las funciones están en `petro.py`."),

    md("## 1. Cargar y limpiar\n"
       "`petro.py` renombra las columnas, convierte metros cúbicos estándar a barriles (1 Sm³ = 6,2898 bbl), "
       "pasa los volúmenes mensuales a **miles de barriles por día (kbd)** y calcula el **corte de agua**."),
    code("import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport petro as P\n\n"
         "prod = P.cargar_produccion()\nreservas = P.cargar_reservas()\ncampos = P.cargar_campos()\nbrent = P.cargar_brent()\n"
         "ULTIMO = prod['fecha'].max()\n"
         "print('Datos hasta:', ULTIMO.strftime('%m/%Y'), '| campos:', prod['campo'].nunique(), '| filas:', len(prod))\n"
         "prod[['campo', 'fecha', 'petroleo_kbd', 'agua_kbd', 'corte_agua']].tail()"),

    md("## 2. Revisar calidad\nVacíos, duplicados (un campo no puede tener dos registros del mismo mes) y valores negativos. "
       "Los negativos son correcciones que Sodir publica sobre meses anteriores: se conservan en los totales y la curva de declinación los ignora."),
    code("print('Vacíos:', int(prod[['petroleo_msm3', 'gas_bsm3', 'agua_msm3']].isna().sum().sum()))\n"
         "print('Duplicados campo-mes:', int(prod.duplicated(['campo', 'fecha']).sum()))\n"
         "print('Valores negativos:', int((prod[['petroleo_msm3', 'gas_bsm3', 'agua_msm3']] < 0).sum().sum()))\n"
         "print('Campos con reservas oficiales:', reservas['campo'].isin(prod['campo']).sum(), 'de', prod['campo'].nunique())"),

    md("## 3. La producción del país: pico, caída y recuperación"),
    code("nac = prod.groupby('fecha').agg(petroleo=('petroleo_kbd', 'sum'), agua=('agua_kbd', 'sum'))\n"
         "anual = nac['petroleo'].groupby(nac.index.year).mean()\n"
         "pico = anual.idxmax()\n"
         "print(f'Pico: {pico} con {anual[pico]:,.0f} kbd')\n"
         "print(f'Mínimo después del pico: {anual.loc[pico:].idxmin()} con {anual.loc[pico:].min():,.0f} kbd '\n"
         "      f'({anual.loc[pico:].min() / anual[pico] - 1:.0%})')\n"
         "print(f'Promedio 2026 (ene–{ULTIMO:%m}): {anual[ULTIMO.year]:,.0f} kbd')\n\n"
         "fig, ax = plt.subplots(figsize=(10, 4))\n"
         "ax.fill_between(nac.index, nac['petroleo'], color='#1E5BFF', alpha=.35)\n"
         "ax.plot(nac.index, nac['petroleo'], color='#1E5BFF', lw=1)\n"
         "ax2 = ax.twinx(); b = brent.set_index('fecha')['brent']; ax2.plot(b.index, b, color='#E3A400', lw=1)\n"
         "ax.set_ylabel('Petróleo (kbd)'); ax2.set_ylabel('Brent (USD/bbl)', color='#E3A400')\n"
         "ax.set_title('La producción tocó techo en 2001 y volvió a subir con los campos nuevos')\n"
         "plt.tight_layout(); plt.savefig('graficos/produccion_nacional.png', dpi=120); plt.show()"),

    md("## 4. ¿Qué campos producen hoy? Concentración del riesgo"),
    code("u12 = prod[prod['fecha'] > ULTIMO - pd.DateOffset(months=12)]\n"
         "hoy = u12.groupby('campo')['petroleo_kbd'].mean().sort_values(ascending=False)\n"
         "part = hoy / hoy.sum()\n"
         "print(f'Producción media últimos 12 meses: {hoy.sum():,.0f} kbd en {(hoy > 0).sum()} campos')\n"
         "print(f'El campo principal aporta {part.iloc[0]:.0%}; los 2 primeros, {part.iloc[:2].sum():.0%}; los 10 primeros, {part.iloc[:10].sum():.0%}')\n"
         "ax = hoy.head(10).sort_values().plot(kind='barh', color='#11A64B', figsize=(8, 4),\n"
         "    title='Dos campos nuevos concentran casi la mitad de la producción')\n"
         "ax.set_xlabel('kbd (promedio 12 meses)'); plt.tight_layout(); plt.savefig('graficos/top_campos.png', dpi=120); plt.show()\n"
         "hoy.head(10).round(1)"),

    md("## 5. Madurez: el agua producida\nEl **corte de agua** es la fracción de agua en el líquido producido. "
       "Cuanto más alto, más madura la cuenca y más caro producir cada barril."),
    code("corte = (nac['agua'] / (nac['agua'] + nac['petroleo'])).groupby(nac.index.year).mean()\n"
         "print(corte.loc[[1990, 2000, 2010, 2020, ULTIMO.year]].map('{:.0%}'.format))\n"
         "agua_por_bbl = corte[ULTIMO.year] / (1 - corte[ULTIMO.year])\n"
         "print(f'Hoy, por cada barril de petróleo salen {agua_por_bbl:.1f} barriles de agua')\n"
         "ax = (corte * 100).plot(color='#E3122F', figsize=(8, 3.5), title='Más de la mitad del líquido producido ya es agua')\n"
         "ax.set_ylabel('% de agua'); plt.tight_layout(); plt.savefig('graficos/corte_agua.png', dpi=120); plt.show()"),

    md("## 6. Reservas: ¿dónde queda el petróleo?\nFactor de avance = producido / recuperable total (estimación oficial)."),
    code("tabla = (reservas.merge(campos, on='campo', how='left')\n"
         "         .assign(avance=lambda d: 1 - d['remanente_mmbbl'] / d['recuperable_mmbbl'])\n"
         "         .query('recuperable_mmbbl > 0')\n"
         "         .sort_values('remanente_mmbbl', ascending=False))\n"
         "total_rem = tabla['remanente_mmbbl'].sum()\n"
         "print(f'Reservas remanentes de petróleo: {total_rem:,.0f} millones de barriles (MMbbl)')\n"
         "print(f'A {brent.tail(12)[\"brent\"].mean():.0f} USD/bbl (Brent 12 meses) eso equivale a ~{total_rem * brent.tail(12)[\"brent\"].mean() / 1000:,.0f} mil millones de USD de ingreso bruto')\n"
         "tabla[['campo', 'operador', 'estado', 'recuperable_mmbbl', 'remanente_mmbbl', 'avance']].head(10).round(2)"),

    md("## 7. Curvas de declinación (Arps)\n"
       "Para campos que ya pasaron su pico se ajusta $q(t) = q_i / (1 + b\\,D_i\\,t)^{1/b}$ desde el pico hasta hoy "
       "y se pronostica hasta un límite económico de 0,5 kbd o 25 años. Ejemplo: **Gullfaks**, campo petrolero operado por Equinor desde 1986."),
    code("def ajustar_campo(nombre):\n"
         "    g = prod[prod['campo'] == nombre]\n"
         "    tramo = P.ventana_declinacion(g)\n"
         "    if tramo is None:\n"
         "        return None\n"
         "    t = (tramo['fecha'] - tramo['fecha'].iloc[0]).dt.days / 365.25\n"
         "    a = P.ajustar_arps(t, tramo['petroleo_kbd'])\n"
         "    q = P.pronostico(a, t.iloc[-1])\n"
         "    return tramo, t, a, q\n\n"
         "tramo, t, a, q = ajustar_campo('GULLFAKS')\n"
         "print({k: round(v, 3) for k, v in a.items()}, '| calidad:', P.calidad(a['r2']))\n"
         "fechas = pd.date_range(tramo['fecha'].iloc[-1], periods=len(q) + 1, freq='MS')[1:]\n"
         "g = prod[prod['campo'] == 'GULLFAKS']\n"
         "fig, ax = plt.subplots(figsize=(10, 4))\n"
         "ax.plot(g['fecha'], g['petroleo_kbd'], color='#9EAAD0', lw=1, label='Real')\n"
         "ax.plot(tramo['fecha'], P.arps(t, a['qi'], a['di'], a['b']), color='#1E5BFF', lw=2, label='Ajuste')\n"
         "ax.plot(fechas, q, color='#E3122F', lw=2, ls='--', label='Pronóstico')\n"
         "ax.set_ylabel('kbd'); ax.legend(); ax.set_title('Gullfaks: la curva de Arps sigue bien su declinación natural')\n"
         "plt.tight_layout(); plt.savefig('graficos/declinacion_gullfaks.png', dpi=120); plt.show()\n"
         "print(f'Petróleo remanente según la curva: {q.sum() * 30.4375 / 1000:.1f} MMbbl | según Sodir: '\n"
         "      f'{reservas.set_index(\"campo\").loc[\"GULLFAKS\", \"remanente_mmbbl\"]:.1f} MMbbl')"),

    md("### ¿Qué tan confiable es la curva en cada campo?\nSe compara el remanente de la curva con la reserva oficial. "
       "Una diferencia grande no siempre es un error: la reserva oficial incluye pozos y proyectos nuevos que la curva no ve."),
    code("filas = []\n"
         "for nombre in hoy[hoy >= 5].index:\n"
         "    r = ajustar_campo(nombre)\n"
         "    if r is None:\n"
         "        filas.append({'campo': nombre, 'calidad': 'meseta: aún no aplica'}); continue\n"
         "    _, _, ak, qk = r\n"
         "    filas.append({'campo': nombre, 'di': ak['di'], 'b': ak['b'], 'r2': ak['r2'], 'calidad': P.calidad(ak['r2']),\n"
         "                  'rem_curva': qk.sum() * 30.4375 / 1000})\n"
         "dca = pd.DataFrame(filas).merge(reservas[['campo', 'remanente_mmbbl']], on='campo', how='left')\n"
         "print(dca['calidad'].value_counts())\n"
         "buenos = dca[dca['calidad'] == 'confiable']\n"
         "dif = (buenos['rem_curva'] / buenos['remanente_mmbbl'] - 1).abs().median()\n"
         "print(f'En los campos con ajuste confiable, la diferencia mediana con la reserva oficial es {dif:.0%}')\n"
         "dca.round(2).sort_values('r2', ascending=False)"),

    md("## 8. ¿Cuánto vale la producción futura?\n"
       "Valor presente neto (VPN) del pronóstico de Gullfaks: flujo = barriles × (Brent − costo operativo) × (1 − impuesto). "
       "Impuesto 78 % (régimen petrolero noruego: 22 % general + 56 % especial), costo operativo 15 USD/bbl y tasa de descuento 10 %. "
       "**Es una estimación simplificada con fines de aprendizaje:** no incluye inversiones, gas ni costos de abandono."),
    code("escenarios = pd.DataFrame([\n"
         "    {'escenario': nombre, 'brent': precio, 'vpn_musd': P.vpn(q, precio, opex=15, impuesto=.78, tasa=.10)}\n"
         "    for nombre, precio in [('Bajo', 55), ('Base (12 meses)', round(brent.tail(12)['brent'].mean())), ('Alto', 95)]])\n"
         "escenarios['vpn_musd'] = escenarios['vpn_musd'].round(0)\n"
         "escenarios"),
    code("precios = np.arange(30, 121, 5)\n"
         "ax = pd.Series([P.vpn(q, p, 15, .78, .10) for p in precios], index=precios).plot(\n"
         "    marker='o', color='#11A64B', figsize=(8, 3.5), title='El valor de Gullfaks crece en línea recta con el Brent')\n"
         "ax.set_xlabel('Brent (USD/bbl)'); ax.set_ylabel('VPN (millones USD)'); ax.axhline(0, color='#999', lw=.8)\n"
         "plt.tight_layout(); plt.savefig('graficos/vpn_gullfaks.png', dpi=120); plt.show()"),

    md("## 9. Conclusiones\n"
       "Los números exactos están en las celdas de arriba y se recalculan al actualizar los datos.\n\n"
       "1. **Cuenca madura que se reinventa:** la producción tocó techo en 2001, cayó a más de la mitad en 2019 "
       "y se recuperó con campos nuevos como Johan Sverdrup y Johan Castberg.\n"
       "2. **Riesgo concentrado:** dos campos aportan casi la mitad del petróleo; una falla en uno de ellos mueve la producción del país.\n"
       "3. **Más agua que petróleo:** el corte de agua pasa del 60 %, así que manejar el agua es parte central del costo.\n"
       "4. **La curva de declinación sirve, con criterio:** funciona bien en campos que declinan de forma natural, pero no "
       "en los que siguen en meseta o reciben pozos nuevos. Incluso en los ajustes confiables la diferencia con la reserva oficial es grande, "
       "porque la curva no sabe cuándo el operador cerrará el campo: el **límite económico** pesa tanto como el ajuste.\n"
       "5. **El valor depende del precio:** con la misma producción, el VPN cambia en proporción al Brent menos el costo operativo.\n\n"
       "**Limitaciones:** solo se evalúa el petróleo (no el gas); el modelo económico no incluye inversiones; "
       "la curva no prevé perforaciones nuevas ni proyectos de recuperación mejorada."),
]

nb = nbf.v4.new_notebook(cells=celdas, metadata={"language_info": {"name": "python"}})
ExecutePreprocessor(timeout=600, kernel_name="python3").preprocess(nb, {"metadata": {"path": str(AQUI)}})
nbf.write(nb, AQUI / "analisis.ipynb")
print("analisis.ipynb listo")
