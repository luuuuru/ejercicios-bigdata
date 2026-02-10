# Paso 4: Resultados y Analisis

**Alumno:** [Nombre Apellido]
**Pregunta de investigacion:** [Tu pregunta]

---

## 3.1 Grafico 1: [Titulo descriptivo]

![Grafico 1](capturas/grafico1.png)

### Interpretacion

[Escribe un parrafo respondiendo estas preguntas:
- Que patron o tendencia se observa en el grafico?
- Hay diferencias entre los paises? Cuales?
- Hay algun punto de inflexion o cambio notable? En que anio?
- Como se relaciona esto con tu pregunta de investigacion?]

### Prompt que usaste para generar este grafico

**Herramienta:** [Gemini]

**Tu prompt exacto:**
```
Basate en esta estructura ejercicios-bigdata/ejercicios/01_bases_de_datos/1.1_introduccion_sqlite/eda_exploratorio.py at main · 
TodoEconometria/ejercicios-bigdata para desarrollar un pipeline de analisis exploratorio 
teniendo en cuenta que exploro la base de datos ADNI fase 3, y que las variables numericas de interes 
son MMSCORE, FAQTOTAL, Parahippocampal_Total', 'Entorhinal_Total, 'Hippocampus_Left',
'ST88CV': 'Hippocampus_Right', 
'ST10CV': 'ICV',  # Opción A
'ST99CV': 'ICV_Alt' y las variables DIAGNOSIS, VISCODE, 'PTID', 'PTGENDER', 'PTEDUCAT', 'APOE4', 'AGE'], 
En primer lugar se debe explorar de cada variable los datos NA y el tipo de variable, 
2º si los formatos de los valores de la variable es necesario transformar, 
y 3º graficos para ver los resultados descriptivos de las variables de interes. 
Ten en cuenta que este pipeline continuara con la limpieza de los datos pero de momento solo quiero EDA
```

**Que tuviste que ajustar:**
[Lo primero fue los nombres de las variables prompt 2 y 3, los siguientes prompt fueron para ajustar el gráfico]
En el apartado  generó  que es este gráfico ->  # 3.3 Matriz de Correlación (Solo numéricas de interés)
Tuve que ajustar ya que me daba este error:

-Prompt 2
''' 
--- Análisis de Variables Numéricas (Rangos) ---
Traceback (most recent call last):
  File "C:\DOCUMENTOS\BigData\ADNI_Project\EDA_definitivo.py", line 201, in <module>
    main()
    ~~~~^^
  File "C:\DOCUMENTOS\BigData\ADNI_Project\EDA_definitivo.py", line 192, in main
    paso_2_revision_formatos(df, cols_categoricas, cols_numericas)
    ~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\DOCUMENTOS\BigData\ADNI_Project\EDA_definitivo.py", line 101, in paso_2_revision_formatos
    print(df[cols_numericas].describe().T[['min', 'max', 'mean', 'std']])
          ~~^^^^^^^^^^^^^^^^
  File "C:\DOCUMENTOS\BigData\ADNI_Project\.venv\Lib\site-packages\pandas\core\frame.py", line 4384, in __getitem__
    indexer = self.columns._get_indexer_strict(key, "columns")[1]
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
  File "C:\DOCUMENTOS\BigData\ADNI_Project\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 6302, in _get_indexer_strict
    self._raise_if_missing(keyarr, indexer, axis_name)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\DOCUMENTOS\BigData\ADNI_Project\.venv\Lib\site-packages\pandas\core\indexes\base.py", line 6355, in _raise_if_missing
    raise KeyError(f"{not_found} not in index")
KeyError: "['Hippocampus_Right'] not in index"
Process finished with exit code 1

y esto:
Prompt 3

estudia biene sto y dime solo lo que tengo que cambiar para corregir el erro --- LISTA DE TODAS LAS COLUMNAS ---
0: PHASE
1: PTID
2: RID
3: VISCODE
4: VISCODE2
5: IMAGEUID
6: FIELD_STRENGTH
7: EXAMDATE
8: RUNDATE
9: STATUS
10: FSVER
11: ST101SV
12: ST102CV
13: ST102SA
14: ST102TA
15: ST102TS
16: Parahippocampal_Right
17: ST103SA
18: ST103TA
19: ST103TS
20: ST104CV
21: ST104SA
22: ST104TA
23: ST104TS
24: ST105CV
25: ST105SA
26: ST105TA
27: ST105TS
28: ST106CV
29: ST106SA
30: ST106TA
31: ST106TS
32: ST107CV
33: ST107SA
34: ST107TA
35: ST107TS
36: ST108CV
37: ST108SA
38: ST108TA
39: ST108TS
40: ST109CV
41: ST109SA
42: ST109TA
43: ST109TS
44: ICV
45: ST110CV
46: ST110SA
47: ST110TA
48: ST110TS
49: ST111CV
50: ST111SA
51: ST111TA
52: ST111TS
53: ST112SV
54: ST113CV
55: ST113SA
56: ST113TA
57: ST113TS
58: ST114CV
59: ST114SA
60: ST114TA
61: ST114TS
62: ST115CV
63: ST115SA
64: ST115TA
65: ST115TS
66: ST116CV
67: ST116SA
68: ST116TA
69: ST116TS
70: ST117CV
71: ST117SA
72: ST117TA
73: ST117TS
74: ST118CV
75: ST118SA
76: ST118TA
77: ST118TS
78: ST119CV
79: ST119SA
80: ST119TA
81: ST119TS
82: ST11SV
83: ST120SV
84: ST121CV
85: ST121SA
86: ST121TA
87: ST121TS
88: ST124SV
89: ST125SV
90: ST127SV
91: ST128SV
92: ST129CV
93: ST129SA
94: ST129TA
95: ST129TS
96: ST12SV
97: ST130CV
98: ST130SA
99: ST130TA
100: ST130TS
101: ST13CV
102: ST13SA
103: ST13TA
104: ST13TS
105: LatVentricle_Left
106: ST14SA
107: ST14TA
108: ST14TS
109: ST15CV
110: ST15SA
111: ST15TA
112: ST15TS
113: ST16SV
114: ST17SV
115: ST18SV
116: ST1SV
117: ST21SV
118: ST23CV
119: ST23SA
120: ST23TA
121: ST23TS
122: Entorhinal_Left
123: ST24SA
124: ST24TA
125: ST24TS
126: ST25CV
127: ST25SA
128: ST25TA
129: ST25TS
130: ST26CV
131: ST26SA
132: ST26TA
133: ST26TS
134: ST28SA
135: Hippocampus_Left
136: ST2SV
137: ST30SV
138: ST31CV
139: ST31SA
140: ST31TA
141: ST31TS
142: ST32CV
143: ST32SA
144: ST32TA
145: ST32TS
146: ST34CV
147: ST34SA
148: ST34TA
149: ST34TS
150: ST35CV
151: ST35SA
152: ST35TA
153: ST35TS
154: ST36CV
155: ST36SA
156: ST36TA
157: ST36TS
158: ST37SV
159: ST38CV
160: ST38SA
161: ST38TA
162: ST38TS
163: ST39CV
164: ST39SA
165: ST39TA
166: ST39TS
167: ST3SV
168: ST40CV
169: ST40SA
170: ST40TA
171: ST40TS
172: ST42SV
173: ST43CV
174: ST43SA
175: ST43TA
176: ST43TS
177: Parahippocampal_Left
178: ST44SA
179: ST44TA
180: ST44TS
181: ST45CV
182: ST45SA
183: ST45TA
184: ST45TS
185: ST46CV
186: ST46SA
187: ST46TA
188: ST46TS
189: ST47CV
190: ST47SA
191: ST47TA
192: ST47TS
193: ST48CV
194: ST48SA
195: ST48TA
196: ST48TS
197: ST49CV
198: ST49SA
199: ST49TA
200: ST49TS
201: ST4SV
202: ST50CV
203: ST50SA
204: ST50TA
205: ST50TS
206: ST51CV
207: ST51SA
208: ST51TA
209: ST51TS
210: ST52CV
211: ST52SA
212: ST52TA
213: ST52TS
214: ST53SV
215: ST54CV
216: ST54SA
217: ST54TA
218: ST54TS
219: ST55CV
220: ST55SA
221: ST55TA
222: ST55TS
223: ST56CV
224: ST56SA
225: ST56TA
226: ST56TS
227: ST57CV
228: ST57SA
229: ST57TA
230: ST57TS
231: ST58CV
232: ST58SA
233: ST58TA
234: ST58TS
235: ST59CV
236: ST59SA
237: ST59TA
238: ST59TS
239: ST5SV
240: ST60CV
241: ST60SA
242: ST60TA
243: ST60TS
244: ST61SV
245: ST62CV
246: ST62SA
247: ST62TA
248: ST62TS
249: ST65SV
250: ST66SV
251: ST68SV
252: ST69SV
253: ST6SV
254: ST70SV
255: ST71SV
256: ST72CV
257: ST72SA
258: ST72TA
259: ST72TS
260: LatVentricle_Right
261: ST73SA
262: ST73TA
263: ST73TS
264: ST74CV
265: ST74SA
266: ST74TA
267: ST74TS
268: ST75SV
269: ST76SV
270: ST77SV
271: ST7SV
272: ST80SV
273: ST82CV
274: ST82SA
275: ST82TA
276: ST82TS
277: Entorhinal_Right
278: ST83SA
279: ST83TA
280: ST83TS
281: ST84CV
282: ST84SA
283: ST84TA
284: ST84TS
285: ST85CV
286: ST85SA
287: ST85TA
288: ST85TS
289: ST87sa
290: ST88SV
291: ST89SV
292: ST8SV
293: ST90CV
294: ST90SA
295: ST90TA
296: ST90TS
297: ST91CV
298: ST91SA
299: ST91TA
300: ST91TS
301: ST93CV
302: ST93SA
303: ST93TA
304: ST93TS
305: ST94CV
306: ST94SA
307: ST94TA
308: ST94TS
309: ST95CV
310: ST95SA
311: ST95TA
312: ST95TS
313: ST96SV
314: ST97CV
315: ST97SA
316: ST97TA
317: ST97TS
318: ST98CV
319: ST98SA
320: ST98TA
321: ST98TS
322: ICV_Alt
323: ST99SA
324: ST99TA
325: ST99TS
326: ST9SV
327: ST147SV
328: ST148SV
329: ST149SV
330: ST150SV
331: ST151SV
332: ST152SV
333: ST153SV
334: ST154SV
335: ST155SV
336: update_stamp
337: DIAGNOSIS
338: MMSCORE
339: FAQTOTAL
340: NPISCORE
341: PTGENDER
342: PTEDUCAT
343: PTMARRY
344: APOE4
345: AGE
✅ Datos cargados correctamente. Dimensiones: (7889, 346)


---

## 3.2 Grafico 2: [Titulo descriptivo]

![Grafico 2](capturas/grafico2.png)

### Interpretacion

[Mismo formato que el Grafico 1. Explica que muestra y que significa.]

### Prompt que usaste para generar este grafico

**Herramienta:** [ChatGPT / Claude / Copilot / otra / ninguna]

**Tu prompt exacto:**
```
crear una nueva funcion dentro del pipeline teniendo en cuenta que la base de datos es longitudinal segun la variable VISCODE, que tiene los siguientes valores

sc      2234

y2      1770

y1      1500

init     887

y4       870

y3       495

y5       133

Name: count, dtype: int64 agrupar sc y init en y0 y desarrollar clustering teniendo en cuenta EL TIEMPO```
```

**Que tuviste que ajustar:**
[Tu respuesta]

---

## 3.3 Respuesta a mi pregunta de investigacion

[Basandote en tus graficos y datos, responde tu pregunta de investigacion
en 2-3 parrafos. Usa evidencia de tus graficos para respaldar tu respuesta.

Ejemplo: "Los datos muestran que la calidad institucional en el Cono Sur
mejoro consistentemente entre 2000-2015, especialmente en Uruguay (vdem_polyarchy
paso de 0.82 a 0.91). En contraste, el Sudeste Asiatico muestra trayectorias
divergentes: Tailandia sufrio un retroceso en 2014 (golpe de estado) mientras
que Indonesia mantuvo una mejora gradual..."]

---

## 3.4 Limitaciones

[Menciona al menos 1 limitacion de tu analisis. Ejemplo:
- "QoG no tiene datos completos para todos los anios en algunas variables"
- "5 paises no son suficientes para generalizar a toda una region"
- "El clustering con pocas variables puede no capturar toda la complejidad"]
-Variables NA:
- NPIQ
-ST68SV
Subcortical Volume (aseg.stats) of NonWMHypoIntensities
-Subcortical Volume (aseg.stats) of FifthVentricle

## 3.5 Referencias
https://diveintopython.org/es/learn/file-handling/csv