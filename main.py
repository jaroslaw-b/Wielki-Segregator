import pandas
from config import *


choicesList_special = ["pierwszy wybór", "drugi wybór", "trzeci wybór", "czwarty wybór", "piąty wybór", "szósty wybór"]

choicesList = ["drugi wybór", "trzeci wybór", "czwarty wybór", "piąty wybór", "szósty wybór"]
classCount = liczba_osob_przyjetych
#every class requires polish, math and two selected subjects
classRequirements = {"a1": "język obcy",
                     "a2": "geografia",
                     "b1": "język obcy",
                     "b2": "fizyka",
                     "c1": "biologia",
                     "c2": "chemia",
                     "d1": "biologia",
                     "d2": "geografia",
                     "e1": "język obcy",
                     "e2": "historia",
                     "f1": "język obcy",
                     "f2": "biologia",
                     }
classes = ["A", "B", "C", "D", "E", "F"]


subjects = ["język polski","język obcy","historia","wos","matematyka","fizyka","chemia","biologia","geografia"]
marksToPoints = {
    6: 18,
    5: 17,
    4: 14,
    3: 8,
    2: 2,
}

# namesWithScores = pandas.DataFrame()
# namesWithScores = pandas.DataFrame(columns=["Imię i nazwisko", "PunktyA", "PunktyB", "PunktyC", "PunktyD",
#                                             "PunktyE", "PunktyF"])

df = pandas.read_csv('data1.csv', encoding = "windows-1250")
df = df.fillna(0)
for sub in subjects:
    df[sub] = df[sub].replace(marksToPoints)
#TODO: gimnazja - przeliczniea egzaminów, sprawdzenie wstępne ocen <2, 6>
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

general_sheet.to_excel(writer_general)
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
        ranking_class[cls] = ranking_class[cls].sort_values("points_" + str(cls).lower(), ascending=False)
        accepted_class[cls] = ranking_class[cls].head(classCount[cls])
        rejected_class[cls] = ranking_class[cls].tail(max(0, ranking_class[cls].shape[0]-classCount[cls]))
        for subcls in classes:
            if cls != subcls:
                ranking_class[cls] = ranking_class[cls].append(rejected_class[subcls][rejected_class[subcls][choice] == cls])
                ranking_class[subcls] = ranking_class[subcls].drop(ranking_class[subcls].tail(max(0, ranking_class[subcls].shape[0]-classCount[subcls]))[ranking_class[subcls][choice] == cls].index)
                # ranking_class[subcls] = ranking_class[subcls][:-max(0, ranking_class[subcls].shape[0]-classCount[subcls])][ranking_class[subcls][choice] != cls]
                ranking_class[subcls] = ranking_class[subcls].sort_values("points_" + str(subcls).lower(), ascending=False)
                accepted_class[subcls] = ranking_class[subcls].head(classCount[subcls])
                rejected_class[subcls] = ranking_class[subcls].tail(max(0, ranking_class[subcls].shape[0] - classCount[subcls]))
                # rejected_class[subcls] = rejected_class[subcls][rejected_class[subcls][choice] != cls]


path = r"results_excel.xlsx"
path_rejected = r"results_rejected_excel.xlsx"
path_first_choice = r"first_choice_list_excel.xlsx"
writer = pandas.ExcelWriter(path, engine='openpyxl')
writer_rejected = pandas.ExcelWriter(path_rejected, engine='openpyxl')
writer_first_choice = pandas.ExcelWriter(path_first_choice, engine='openpyxl')


for cls in classes:
    # save to csv
    # accepted_class[cls][["Nazwisko i imię", "points_"+ str(cls).lower(), "pierwszy wybór", "drugi wybór", "trzeci wybór", "czwarty wybór", "piąty wybór", "szósty wybór"]].to_csv("results/" + cls + ".csv")
    # rejected_class[cls][["Nazwisko i imię", "points_" + str(cls).lower(), "pierwszy wybór", "drugi wybór", "trzeci wybór",
    #      "czwarty wybór", "piąty wybór", "szósty wybór"]].to_csv("results_rejected/" + cls + ".csv")


    accepted_class[cls][
        ["Nazwisko i imię", "points_" + str(cls).lower()]].to_excel(writer, sheet_name=cls)
    rejected_class[cls][
        ["Nazwisko i imię", "points_" + str(cls).lower()]].to_excel(writer_rejected, sheet_name=cls)
    ranking_class_first_choice[cls][["Nazwisko i imię", "points_" + str(cls).lower()]].to_excel(writer_first_choice, sheet_name=cls)


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