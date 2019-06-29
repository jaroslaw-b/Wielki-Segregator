import pandas
from config import *

status = " "
choicesList_special = ["pierwszy wybór", "drugi wybór", "trzeci wybór", "czwarty wybór", "piąty wybór", "szósty wybór"]

choicesList = ["drugi wybór", "trzeci wybór", "czwarty wybór", "piąty wybór", "szósty wybór"]
classCount = liczba_osob_przyjetych
#every class requires polish, math and two selected subjects
classRequirements = {"a1": "język obcy",
                     "a2": "historia",
                     "b1": "biologia",
                     "b2": "geografia",
                     "c1": "biologia",
                     "c2": "chemia",
                     "d1": "język obcy",
                     "d2": "biologia",
                     "e1": "język obcy",
                     "e2": "fizyka",
                     "f1": "język obcy",
                     "f2": "geografia",
                     }
classes = ["A", "B", "C", "D", "E", "F"]


subjects = ["język polski","język obcy","historia","wos","matematyka","fizyka","chemia","biologia","geografia"]
marksToPoints_gimnazjum = {
    6: 18,
    5: 17,
    4: 14,
    3: 8,
    2: 2,
}
marksToPoints_podstawowka = {
    6: 18,
    5: 17,
    4: 14,
    3: 8,
    2: 2,
}

# namesWithScores = pandas.DataFrame()
# namesWithScores = pandas.DataFrame(columns=["Imię i nazwisko", "PunktyA", "PunktyB", "PunktyC", "PunktyD",
#                                             "PunktyE", "PunktyF"])

df = pandas.read_csv('data.csv', encoding = "windows-1250", sep=separator)
df = df.fillna(0)

for sub in subjects:
    if not df[sub].lt(7).all(axis = 0):
        print("UWAGA: ZNALEZIONO OCENĘ POZA ZAKRESEM 2 do 6!!!!!!!!!! w " + sub)
        print(df[df[sub] > 6]["Nazwisko i imię"])
        status = status + "UWAGA: ZNALEZIONO OCENĘ POZA ZAKRESEM 2 do 6!!!!!!!!!! w " + sub + '\n'
        status = status + str(df[df[sub] > 6]["Nazwisko i imię"]) + '\n'
    elif not df[sub].gt(1).all(axis = 0):
        print("UWAGA: ZNALEZIONO OCENĘ POZA ZAKRESEM 2 do 6!!!!!!!!!! w " + sub)
        print(df[df[sub] < 2]["Nazwisko i imię"])
        status = status + "UWAGA: ZNALEZIONO OCENĘ POZA ZAKRESEM 2 do 6!!!!!!!!!! w " + sub + '\n'
        status = status + str(df[df[sub] < 2]["Nazwisko i imię"]) + '\n'
    else:
        print("OCENY POPRAWNE dla " + sub)
        status = status + "OCENY POPRAWNE dla " + sub +'\n'

if "egzamin historia" in df.columns:
    print("WYKRYTO TYP SZKOLY: GIMNAZJUM")
    status = status + "WYKRYTO TYP SZKOLY: GIMNAZJUM" + '\n'
    for sub in subjects:
        df[sub] = df[sub].replace(marksToPoints_gimnazjum)

    namesWithScores = df.assign(points_a = df['język polski'] + df["matematyka"]
                                               + df[classRequirements["a1"]] + df[classRequirements["a2"]] +
                           .2*(df["egzamin polski"] + df["egzamin historia"] + df["egzamin matematyka"] +
                               df["egzamin przyroda"] + df["egzamin język"]) + df["wyróżnienie"] + \
                            df["punkty dodatkowe"],
                                points_b=df['język polski'] + df["matematyka"]
                                             + df[classRequirements["b1"]] + df[classRequirements["b2"]] +
                             .2 * (df["egzamin polski"] + df["egzamin historia"] + df["egzamin matematyka"] +
                               df["egzamin przyroda"] + df["egzamin język"]) + df["wyróżnienie"] + \
                            df["punkty dodatkowe"],
                                points_c=df['język polski'] + df["matematyka"]
                                            + df[classRequirements["c1"]] + df[classRequirements["c2"]] +
                             .2 * (df["egzamin polski"] + df["egzamin historia"] + df["egzamin matematyka"] +
                               df["egzamin przyroda"] + df["egzamin język"]) + df["wyróżnienie"] + \
                             df["punkty dodatkowe"],
                                points_d=df['język polski'] + df["matematyka"]
                                    + df[classRequirements["d1"]] + df[classRequirements["d2"]] +
                             .2 * (df["egzamin polski"] + df["egzamin historia"] + df["egzamin matematyka"] +
                               df["egzamin przyroda"] + df["egzamin język"]) + df["wyróżnienie"] + \
                             df["punkty dodatkowe"],
                                points_e=df['język polski'] + df["matematyka"]
                                            + df[classRequirements["e1"]] + df[classRequirements["e2"]] +
                             .2 * (df["egzamin polski"] + df["egzamin historia"] + df["egzamin matematyka"] +
                               df["egzamin przyroda"] + df["egzamin język"]) + df["wyróżnienie"] + \
                             df["punkty dodatkowe"],
                                points_f=df['język polski'] + df["matematyka"]
                                            + df[classRequirements["f1"]] + df[classRequirements["f2"]] +
                             .2 * (df["egzamin polski"] + df["egzamin historia"] + df["egzamin matematyka"] +
                               df["egzamin przyroda"] + df["egzamin język"]) + df["wyróżnienie"] + \
                             df["punkty dodatkowe"])
    exams = ["egzamin polski", "egzamin historia", "egzamin matematyka", "egzamin przyroda","egzamin język","wyróżnienie","punkty dodatkowe"]
else:
    print("WYKRYTO TYP SZKOLY: SZKOLA PODSTAWOWA")
    status = status + "WYKRYTO TYP SZKOLY: SZKOLA PODSTAWOWA" + '\n'
    for sub in subjects:
        df[sub] = df[sub].replace(marksToPoints_podstawowka)

    namesWithScores = df.assign(points_a=df['język polski'] + df["matematyka"]
                                         + df[classRequirements["a1"]] + df[classRequirements["a2"]] +
                                         .35 * df["egzamin polski"] + .35*df[
                                    "egzamin matematyka"] + .3 * df["egzamin język"] + df["wyróżnienie"] + \
                                         df["punkty dodatkowe"],
                                points_b=df['język polski'] + df["matematyka"]
                                         + df[classRequirements["b1"]] + df[classRequirements["b2"]] +
                                         .35 * df["egzamin polski"] + .35 * df[
                                             "egzamin matematyka"] + .3 * df["egzamin język"] + df["wyróżnienie"] + \
                                         df["punkty dodatkowe"],
                                points_c=df['język polski'] + df["matematyka"]
                                         + df[classRequirements["c1"]] + df[classRequirements["c2"]] +
                                         .35 * df["egzamin polski"] + .35 * df[
                                             "egzamin matematyka"] + .3 * df["egzamin język"] + df["wyróżnienie"] + \
                                         df["punkty dodatkowe"],
                                points_d=df['język polski'] + df["matematyka"]
                                         + df[classRequirements["d1"]] + df[classRequirements["d2"]] +
                                         .35 * df["egzamin polski"] + .35 * df[
                                             "egzamin matematyka"] + .3 * df["egzamin język"] + df["wyróżnienie"] + \
                                         df["punkty dodatkowe"],
                                points_e=df['język polski'] + df["matematyka"]
                                         + df[classRequirements["e1"]] + df[classRequirements["e2"]] +
                                         .35 * df["egzamin polski"] + .35 * df[
                                             "egzamin matematyka"] + .3 * df["egzamin język"] + df["wyróżnienie"] + \
                                         df["punkty dodatkowe"],
                                points_f=df['język polski'] + df["matematyka"]
                                         + df[classRequirements["f1"]] + df[classRequirements["f2"]] +
                                         .35 * df["egzamin polski"] + .35 * df[
                                             "egzamin matematyka"] + .3 * df["egzamin język"] + df["wyróżnienie"] + \
                                         df["punkty dodatkowe"])
    exams = ["egzamin polski", "egzamin matematyka", "egzamin język",
             "wyróżnienie", "punkty dodatkowe"]

general_sheet = namesWithScores.sort_values(by=["Nazwisko i imię"])
general_sheet.drop(subjects, inplace=True, axis=1)
# general_sheet.drop(choicesList, inplace=True, axis=1)
general_sheet.drop(exams, inplace=True, axis=1)
general_sheet_classes = dict()


def checkRow(row, _cls):
    if _cls not in row[choicesList_special].values.tolist():
        # print(row["points_" + str(_cls).lower()])
        row["points_" + str(_cls).lower()] = None
    return row

for cls in classes:
    general_sheet = general_sheet.apply(checkRow, _cls=cls, axis=1)
    # if not general_sheet[choicesList].iloc[0].str.contains(cls).any():
    #     general_sheet["points_" + str(cls).lower()] = 0

general_sheet[choicesList_special] = general_sheet[choicesList_special].replace({0: None})

writer_general = pandas.ExcelWriter("general.xlsx", engine='openpyxl')

for cls in classes:
    general_sheet[general_sheet["pierwszy wybór"] == cls].to_excel(writer_general, sheet_name=cls)

general_sheet.to_excel(writer_general, sheet_name='general')
writer_general.save()

ranking_class = dict()
accepted_class = dict()
rejected_class = dict()
for cls in classes:
    ranking_class[cls] = namesWithScores[namesWithScores["pierwszy wybór"]
                                         == cls].sort_values("points_"+ str(cls).lower(), ascending=False)
    accepted_class[cls] = ranking_class[cls].head(classCount[cls])
    rejected_class[cls] = ranking_class[cls].tail(max(0, ranking_class[cls].shape[0]-classCount[cls]))

ranking_class_first_choice = ranking_class.copy()

for choice in choicesList:
    for cls in classes:
        for subcls in classes:
            if cls != subcls:
                ranking_class[cls] = ranking_class[cls].append(rejected_class[subcls][rejected_class[subcls][choice] == cls], ignore_index=True)
                ranking_class[cls] = ranking_class[cls].sort_values("points_" + str(cls).lower(), ascending=False)
                accepted_class[cls] = ranking_class[cls].head(classCount[cls])
                rejected_class[cls] = ranking_class[cls].tail(max(0, ranking_class[cls].shape[0]-classCount[cls]))
                # ranking_class[subcls] = ranking_class[subcls][ranking_class[subcls][choice] != cls ]
                # ranking_class[subcls].drop(rejected_class[subcls][rejected_class[subcls][choice] == cls]["Nazwisko i imię"], inplace=True)
                ranking_class[subcls].drop(ranking_class[subcls].tail(max(0, ranking_class[subcls].shape[0]-classCount[subcls]))[ranking_class[subcls][choice] == cls].index, inplace=True)
                # ranking_class[subcls] = ranking_class[subcls][:-max(0, ranking_class[subcls].shape[0]-classCount[subcls])][ranking_class[subcls][choice] != cls]
                ranking_class[subcls].sort_values("points_" + str(subcls).lower(), ascending=False, inplace = True)
                accepted_class[subcls] = ranking_class[subcls].head(classCount[subcls])
                rejected_class[subcls] = ranking_class[subcls].tail(max(0, ranking_class[subcls].shape[0] - classCount[subcls]))

                # rejected_class[subcls] = rejected_class[subcls][rejected_class[subcls][choice] != cls]



path = r"results_excel.xlsx"
path_rejected = r"results_rejected_excel.xlsx"
path_first_choice = r"first_choice_list_excel.xlsx"
writer = pandas.ExcelWriter(path, engine='openpyxl')
writer_rejected = pandas.ExcelWriter(path_rejected, engine='openpyxl')
writer_first_choice = pandas.ExcelWriter(path_first_choice, engine='openpyxl')

names_list_before = namesWithScores["Nazwisko i imię"]
names_list_after = pandas.Series()

for cls in classes:
    names_list_after = names_list_after.append(ranking_class[cls]["Nazwisko i imię"], ignore_index=True)
    accepted_class[cls][
        ["Nazwisko i imię", "points_" + str(cls).lower()]].to_excel(writer, sheet_name=cls)
    rejected_class[cls][
        ["Nazwisko i imię", "points_" + str(cls).lower()]].to_excel(writer_rejected, sheet_name=cls)
    ranking_class_first_choice[cls][["Nazwisko i imię", "points_" + str(cls).lower()]].to_excel(writer_first_choice, sheet_name=cls)

names_list_after = names_list_after.sort_values()
names_list_before = names_list_before.sort_values()
print(names_list_before)
print(names_list_after)
names_list_before = names_list_before.to_list()
names_list_after = names_list_after.to_list()

na = pandas.Series(names_list_after)
nb = pandas.Series(names_list_before)
comparison = pandas.concat([nb, na], axis=1, ignore_index=True, sort=True)
# comparison = pandas.DataFrame({'s1': names_list_before, 's2': names_list_after})
comparison.to_excel(writer_general, sheet_name='end-to-end')
writer_general.save()



# print(names_list_after.equals(names_list_before))
# print(names_list_before)
# print(names_list_after)
writer.save()
writer_rejected.save()
writer_first_choice.save()




print("Liczba uczniów na liście wejściowej: "+ str(namesWithScores.shape[0])+'\n')
sum = 0
for list in accepted_class:
    sum += accepted_class[list].shape[0]
for list in rejected_class:
    sum += rejected_class[list].shape[0]
print("Liczba uczniów na listach wyjściowych: "+ str(sum) +'\n')

status = status + "Liczba uczniów na liście wejściowej: "+ str(namesWithScores.shape[0])+'\n'
status = status + "Liczba uczniów na listach wyjściowych: "+ str(sum) +'\n'


print("________________________________________")
print(status)

file = open("status.txt", "w")
file.write(status)
file.close()