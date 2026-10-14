"""Construye y ejecuta analisis.ipynb (pandas + matplotlib). Uso: python construir_notebook.py"""
import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
from pathlib import Path

AQUI = Path(__file__).parent
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell

celdas = [
    md("# Análisis de ventas · enero–junio 2026\n"
       "**Pregunta de negocio:** ¿qué regiones, productos y vendedores explican los ingresos del semestre, y dónde hay oportunidades?\n\n"
       "**Datos:** 120 ventas de una distribuidora de tecnología y oficina (`../datos`).\n\n"
       "**Herramientas:** Python, pandas, matplotlib."),
    md("## 1. Cargar los datos"),
    code("import pandas as pd\nimport matplotlib.pyplot as plt\nfrom pathlib import Path\n\n"
         "DATOS = Path('..') / 'datos'\n"
         "ventas = pd.read_csv(DATOS / 'ventas.csv', parse_dates=['fecha'])\n"
         "productos = pd.read_csv(DATOS / 'productos.csv')\n"
         "vendedores = pd.read_csv(DATOS / 'vendedores.csv')\n"
         "ventas.head()"),
    md("## 2. Revisar calidad: tipos, vacíos y duplicados\nAntes de analizar, siempre se valida."),
    code("print(ventas.dtypes, '\\n')\n"
         "print('Filas:', len(ventas))\n"
         "print('Vacíos por columna:\\n', ventas.isna().sum())\n"
         "print('Duplicados:', ventas.duplicated().sum())"),
    md("## 3. Unir tablas y crear columnas de negocio\n`merge` es el JOIN de pandas."),
    code("df = (ventas\n"
         "      .merge(productos.rename(columns={'id': 'producto_id', 'nombre': 'producto'}), on='producto_id')\n"
         "      .merge(vendedores.rename(columns={'id': 'vendedor_id', 'nombre': 'vendedor', 'region': 'region_vendedor'}), on='vendedor_id'))\n"
         "df['ingreso'] = df['cantidad'] * df['precio_unit']\n"
         "df['margen'] = df['cantidad'] * (df['precio_unit'] - df['costo'])\n"
         "df['mes'] = df['fecha'].dt.to_period('M')\n"
         "df[['fecha', 'region', 'producto', 'vendedor', 'cantidad', 'ingreso', 'margen']].head()"),
    md("## 4. KPIs del semestre"),
    code("kpis = {\n"
         "    'Ingreso total': df['ingreso'].sum(),\n"
         "    'Margen total': df['margen'].sum(),\n"
         "    'Margen %': round(df['margen'].sum() / df['ingreso'].sum() * 100, 1),\n"
         "    'Ventas': len(df),\n"
         "    'Ticket promedio': round(df['ingreso'].mean(), 2),\n"
         "}\n"
         "pd.Series(kpis)"),
    md("## 5. Ingreso por región"),
    code("COLORES = ['#11A64B', '#E3122F', '#1E5BFF', '#F2C200']\n"
         "por_region = df.groupby('region')['ingreso'].sum().sort_values(ascending=False)\n"
         "ax = por_region.plot(kind='bar', color=COLORES, title='Ingreso por región', rot=0)\n"
         "ax.set_ylabel('USD'); plt.tight_layout(); plt.savefig('graficos/ingreso_region.png', dpi=120); plt.show()\n"
         "(por_region / por_region.sum() * 100).round(1)"),
    md("## 6. Evolución mensual"),
    code("mensual = df.groupby('mes')['ingreso'].sum()\n"
         "ax = mensual.plot(marker='o', color='#1E5BFF', title='Ingreso mensual')\n"
         "ax.set_ylabel('USD'); plt.tight_layout(); plt.savefig('graficos/ingreso_mensual.png', dpi=120); plt.show()\n"
         "mensual.pct_change().mul(100).round(1)"),
    md("## 7. Productos: volumen vs. margen"),
    code("prod = df.groupby('producto').agg(unidades=('cantidad', 'sum'), ingreso=('ingreso', 'sum'), margen=('margen', 'sum'))\n"
         "prod['margen_pct'] = (prod['margen'] / prod['ingreso'] * 100).round(1)\n"
         "prod = prod.sort_values('margen', ascending=False)\n"
         "ax = prod['margen'].plot(kind='barh', color='#11A64B', title='Margen por producto')\n"
         "ax.invert_yaxis(); plt.tight_layout(); plt.savefig('graficos/margen_producto.png', dpi=120); plt.show()\n"
         "prod"),
    md("## 8. Cumplimiento de metas por vendedor"),
    code("vend = df.groupby(['vendedor', 'meta'])['ingreso'].sum().reset_index()\n"
         "vend['cumplimiento_%'] = (vend['ingreso'] / vend['meta'] * 100).round(1)\n"
         "vend = vend.sort_values('cumplimiento_%', ascending=False)\n"
         "colores = ['#11A64B' if c >= 100 else '#E3122F' for c in vend['cumplimiento_%']]\n"
         "ax = vend.plot(x='vendedor', y='cumplimiento_%', kind='bar', color=colores, legend=False, rot=20, title='Cumplimiento de meta (%)')\n"
         "ax.axhline(100, color='#F2C200', linestyle='--'); plt.tight_layout(); plt.savefig('graficos/cumplimiento_meta.png', dpi=120); plt.show()\n"
         "vend"),
    md("## 9. Tabla dinámica: región × canal"),
    code("pd.pivot_table(df, index='region', columns='canal', values='ingreso', aggfunc='sum', margins=True, margins_name='Total')"),
    md("## 10. Exportar el resumen a Excel"),
    code("with pd.ExcelWriter('resumen_ventas.xlsx') as xls:\n"
         "    pd.Series(kpis, name='valor').to_frame().to_excel(xls, sheet_name='KPIs')\n"
         "    por_region.to_frame().to_excel(xls, sheet_name='Region')\n"
         "    prod.to_excel(xls, sheet_name='Productos')\n"
         "    vend.to_excel(xls, sheet_name='Vendedores', index=False)\n"
         "print('resumen_ventas.xlsx creado')"),
    md("## Conclusiones\n"
       "1. **Norte y Sur concentran el 77 % del ingreso.** Este y Oeste tienen espacio para crecer.\n"
       "2. **Junio cayó 38 % frente a mayo**: hay que revisar stock y actividad comercial del cierre del semestre.\n"
       "3. **Accesorios tiene el mejor margen % (44,5 %)** aunque menor ingreso: conviene impulsarlo en combos.\n"
       "4. **Solo 1 de 6 vendedores superó su meta.** Las metas de Ana Torres y Sofía Díaz parecen desalineadas con su región.\n\n"
       "**Recomendación:** priorizar campañas en Este/Oeste con productos de alto margen (Silla ergonómica, Webcam HD) y revisar las metas por región."),
]

nb = nbf.v4.new_notebook(); nb.cells = celdas
nb.metadata["kernelspec"] = {"name": "python3", "display_name": "Python 3", "language": "python"}
(AQUI / "graficos").mkdir(exist_ok=True)
ExecutePreprocessor(timeout=120, kernel_name="python3").preprocess(nb, {"metadata": {"path": str(AQUI)}})
nbf.write(nb, AQUI / "analisis.ipynb")
print("analisis.ipynb creado y ejecutado")
