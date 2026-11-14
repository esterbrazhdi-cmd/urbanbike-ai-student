# Raporti i studentit: UrbanBike AI

Studenti: Ester Brazhdi
Grupi (nëse punohet në grup): Punë individuale
Data: 13.11.2026
GitHub-i im: https://github.com/esterbrazhdi-cmd/urbanbike-ai-student
Figma:
https://www.figma.com/design/rCxWhAFwjg3GiE4dRepbKr/UrbanBike-AI?node-id=0-1&t=R3JBmmyK2IjBtSFe-1
https://www.figma.com/design/mjXmYmKrhFr3A07BrBtrWC/UrbanBike-AI?node-id=0-1&t=Nqukfdflm0rBm3su-1

## Qëllimi

Problemi që zgjidhim: 
Të parashikojmë sa biçikleta do të merren me qira gjatë një dite, duke përdorur të dhëna historike dhe informacione për motin.

Target-i y: 
Numri total i qirave ditore të biçikletave (rentals).

Predictorët X:
 Të dhënat e ditëve të mëparshme, temperatura, reshjet, era, dita e javës, muaji dhe informacioni nëse dita është ditë pune apo festë.

Koha kur parashikojmë dhe çfarë informacioni është i njohur:
 Parashikimi bëhet për një ditë përpara. Përdorim informacionin që është i disponueshëm nga ditët e kaluara, pa marrë të dhëna nga e ardhmja.

## Pastrimi

Burimet reale dhe çelësi i bashkimit: 
Përdorëm të dhënat e UCI për qiratë e biçikletave dhe të dhënat e NASA-s për motin. Të dyja burimet u bashkuan sipas datës.

Dallimi mes origjinaleve dhe kopjes didaktike: 
Të dhënat origjinale janë burimet fillestare. Në kopjen e përdorur për ushtrim ishin shtuar qëllimisht disa gabime, në mënyrë që të praktikonim pastrimin.

Rreshtat para/pas: 
Para pastrimit kishte 743 rreshta; pas pastrimit mbetën 731.

Dublimet: 
U identifikuan dhe u hoqën 12 rreshta të përsëritur.

Mungesat para/pas konvertimit: 
Fillimisht kishte 30 vlera bosh. Pas konvertimit u identifikuan edhe 6 vlera të shkruara gabim, pra 36 vlera që mungonin gjithsej.

Arsyeja e imputimit vetëm me train:
 Vlerat që mungonin u trajtuan duke përdorur vetëm të dhënat e trajnimit, që modeli të mos marrë informacion nga validimi ose testi gjatë mësimit.

## Grafikët

Vëzhgimi 1 dhe figura përkatëse:
 Te reports/figures/01_demand.png shihet se numri i qirave ndryshon nga dita në ditë. Ka periudha kur kërkesa për biçikleta është më e lartë dhe periudha kur është më e ulët.

Vëzhgimi 2 dhe figura përkatëse: 
Te reports/figures/02_workingday.png krahasohet numri mesatar i qirave në ditët e punës me fundjavat dhe festat. Kjo na ndihmon të shohim nëse lloji i ditës lidhet me kërkesën.

Pse një lidhje e dukshme nuk provon shkakësi: 
Edhe nëse dy tregues ndryshojnë së bashku, kjo nuk do të thotë domosdoshmërisht që njëri shkakton tjetrin. Mund të ndikojnë edhe faktorë të tjerë.

## Vlerësimi


| Modeli | Validation MAE | Test MAE | Test RMSE | Test R² |
|---|---:|---:|---:|---:|
| Yesterday | 775.203 | 916.402 | 1330.386 | 0.539 |
| DummyMean | 2953.866 | 2494.628 | 2790.064 | -1.027 |
| Ridge | 687.558 | 893.251 | 1252.655 | 0.591 |
| RandomForest | 1821.528 | 1671.499 | 2042.654 | -0.087 |

Modeli i zgjedhur nga validation dhe arsyeja: Zgjodha Ridge, sepse kishte MAE më të ulët në validim nga modelet e krahasuara. Për Ridge, Validation MAE ishte 687.558.

Rezultati i provës me Random Forest:
 RandomForest nuk e përmirësoi rezultatin. Në test, MAE i tij ishte 1671.499, ndërsa për Ridge ishte 893.251. Prandaj mbajtëm Ridge si modelin përfundimtar.

Interpretimi i gabimit në qira për ditë: 
Ridge kishte MAE 893.251 në test. Kjo do të thotë se gabimi absolut mesatar i parashikimeve ishte rreth 893 qira në ditë.

Rezultati i klasifikimit, nëse u realizua: 
Përdora LogisticRegression për të dalluar ditët me kërkesë normale nga ato me kërkesë të lartë. Modeli arriti rreth 91.8% saktësi në test.

## Kufizimet

1.Projekti përdor të dhëna historike të një qyteti dhe nuk është testuar për qytete të tjera.

2.Të dhënat e motit nga NASA mund të mos tregojnë saktësisht motin në çdo pjesë të qytetit.

3.Parashikimi mbështetet në faktin që kemi në dispozicion të dhënat e ditëve të mëparshme.

## Kontributet individuale


| Studenti | Skedari/ekrani | Puna dhe vendimi | Commit/prova |
|---|---|---|---|
| Ester Brazhdi | `01_clean.py`, `02_visualize.py` | Pastrova të dhënat dhe krijova grafikët. | Grafikët në `reports/figures` |
| Ester Brazhdi | `03_train.py`, `04_classify.py` | Trajnova dhe krahasova modelet; zgjodha Ridge dhe realizova klasifikimin. | Rezultatet në `reports` |
| Ester Brazhdi | Figma, `app.py` | Përgatita dizajnin dhe aplikacionin për parashikimin sipas datës. | Aplikacioni në Chrome dhe commit-i në GitHub |
| Ester Brazhdi | `RAPORTI.md` | Dokumentova pastrimin, grafikët, vlerësimin dhe kufizimet e projektit. | Raporti në repository |

## Burimet

UCI: https://doi.org/10.24432/C5W894
NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Provenienca lokale: data/raw/provenance.json
