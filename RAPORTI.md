# Raporti i studentit: UrbanBike AI

Studenti: Ester Brazhdi
Grupi (nëse punohet në grup):
Data: 13.11.2026
GitHub-i im:
Figma:https://www.figma.com/design/rCxWhAFwjg3GiE4dRepbKr/UrbanBike-AI?node-id=0-1&t=R3JBmmyK2IjBtSFe-1 https://www.figma.com/design/mjXmYmKrhFr3A07BrBtrWC/UrbanBike-AI?node-id=0-1&t=Nqukfdflm0rBm3su-1

## Qëllimi

Problemi që zgjidhim:Parashikimi i numrit të biçikletave që do të merren me qira gjatë një dite.
Target-i y:Numri total i qirave ditore të biçikletave (rentals).
Predictorët X:Të dhënat e ditëve të mëparshme, temperatura, shiu, era, dita e javës, muaji dhe ditët e punës ose festat.
Koha kur parashikojmë dhe çfarë informacioni është i njohur:Parashikojmë një ditë përpara, duke përdorur informacionin që kemi nga ditët e kaluara.

## Pastrimi

Burimet reale dhe çelësi i bashkimit:Përdorëm të dhënat e UCI për qiratë e biçikletave dhe të dhënat e NASA-s për motin. I bashkuam sipas datës.
Dallimi mes origjinaleve dhe kopjes didaktike:Të dhënat origjinale ishin burimet fillestare. Në kopjen për ushtrim u shtuan qëllimisht disa gabime për të mësuar pastrimin.
Rreshtat para/pas:Para pastrimit: 743 rreshta. Pas pastrimit: 731 rreshta.
Dublimet:Kishim 12 rreshta të përsëritur, të cilët u hoqën.
Mungesat para/pas konvertimit:Para konvertimit kishte 30 vlera bosh. Pas konvertimit u identifikuan edhe 6 vlera të shkruara gabim, pra 36 vlera që mungonin gjithsej.
Arsyeja e imputimit vetëm me train:Që modeli të mos përdorë informacion nga të dhënat e testimit gjatë trajnimit.

## Grafikët

Vëzhgimi 1 dhe figura përkatëse:Te 01_demand.png shihet se numri i qirave ndryshon nga dita në ditë dhe ka periudha me kërkesë më të lartë.
Vëzhgimi 2 dhe figura përkatëse:Te 02_workingday.png krahasohet numri mesatar i qirave në ditët e punës me fundjavat dhe festat.
Pse një lidhje e dukshme nuk provon shkakësi:Sepse dy gjëra mund të ndryshojnë së bashku, por kjo nuk do të thotë që njëra shkakton tjetrën.

## Vlerësimi

| Modeli       | Validation MAE | Test MAE | Test RMSE | Test R² |
|--------------|---------------:|---------:|----------:|--------:|
| Yesterday    |Nga CSV         |  916.402 | 1330.386  |0.539    |
| DummyMean    |Nga CSV         | 2494.628 | 2790.064  | -1.027  |
| Ridge        |Nga CSV         | 893.251  | 893.251   | 0.591   |
| RandomForest |Nga CSV         | 1671.499 | 1671.499  | -0.087  |

Modeli i zgjedhur nga validation dhe arsyeja:Zgjodha Ridge sepse kishte gabimin më të vogël MAE në validim nga modelet që trajnuam.
Rezultati i provës me Random Forest: RandomForest pati gabim më të madh se Ridge, prandaj nuk u zgjodh si modeli përfundimtar.
Interpretimi i gabimit në qira për ditë:Ridge kishte një gabim mesatar prej rreth 893 qirash në ditë gjatë testimit.
Rezultati i klasifikimit, nëse u realizua:Përdora LogisticRegression për të dalluar ditët me kërkesë normale nga ato me kërkesë të lartë. Modeli arriti rreth 91.8% saktësi në test.

## Kufizimet

1.Projekti përdor të dhëna historike të një qyteti dhe nuk është testuar për qytete të tjera.
2.Të dhënat e motit nga NASA mund të mos tregojnë saktësisht motin në çdo pjesë të qytetit.
3.Parashikimi supozon që i kemi të dhënat e ditëve të mëparshme.

## Kontributet individuale

| Studenti    | Skedari/ekrani             | Puna dhe vendimi                       | Commit/prova         |
|Ester Brazhdi|01_clean.py, 02_visualize.py|Pastrova të dhënat dhe krijova grafikët |Grafikët te reports   |
|Ester Brazhdi|03_train.py, 04_classify.py |Trajnova modelet dhe zgjodha Ridge      | Rezultatet te reports|
|Ester Brazhdi|Figma, app.py               |Krijova dizajnin dhe aplikacionin       |Pamja në Chrome       |
| | | | |

## Burimet

UCI: https://doi.org/10.24432/C5W894
NASA: https://power.larc.nasa.gov/docs/services/api/temporal/daily/
Provenienca lokale: data/raw/provenance.json
