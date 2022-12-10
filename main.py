import matplotlib.style
import numpy
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
matplotlib.style.use("seaborn-v0_8-colorblind")

df = pd.read_csv("C:/Users/jwade/OneDrive/Desktop/R obesity data/Data/CNMCObesityQI_DATA_2022-11-14_1851.csv")
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y")

baselineDate = dt.datetime(2021, 2, 28)
threeMonths = dt.datetime(2021, 5, 31)
sixMonths = dt.datetime(2021, 8, 31)
nineMonths = dt.datetime(2021, 11, 30)
eighteenMonths = dt.datetime(2022, 8, 31)


def sort_dates(row):
    if row["date"] <= baselineDate:
        return 0
    if row["date"] <= threeMonths:
        return 3
    if row["date"] <= sixMonths:
        return 6
    if row["date"] <= nineMonths:
        return 9
    if row["date"] <= eighteenMonths:
        return 18


def get_site(row):
    if row["site"] == 2:
        return "Anacostia"
    return "THEARC"


def get_age_group(row):
    if row["age"] <= 8:
        return "2_8"
    return "9_18"


def get_both_codes(row):
    if row["zcode"] == 1 and row["ecode"] == 1:
        return 1
    return 0


def get_z_only(row):
    if row["zcode"] == 1 and row["ecode"] == 0:
        return 1
    return 0


def get_e_only(row):
    if row["zcode"] == 0 and row["ecode"] == 1:
        return 1
    return 0


def get_no_codes(row):
    if row["zcode"] == 0 and row["ecode"] == 0:
        return 1
    return 0


def get_age_group(row):
    if row["age"] <= 8:
        return "young"
    return "old"


def get_stigmatizing(row):
    if row["stigmatizing___0"] == 1:
        return 0
    return 1


df["months"] = df.apply(sort_dates, axis=1)
df["both_codes"] = df.apply(get_both_codes, axis=1)
df["z_only"] = df.apply(get_z_only, axis=1)
df["e_only"] = df.apply(get_e_only, axis=1)
df["no_codes"]= df.apply(get_no_codes, axis=1)
df["stigmatizing_language"] = df.apply(get_stigmatizing, axis=1)
df["location"] = df.apply(get_site, axis=1)
df["age_group"] = df.apply(get_age_group, axis=1)

df = df.rename(columns={"extra___0": "no_extra", "extra___1": "AST", "extra___2": "Glucose",
                        "extra___3": "CMP", "extra___4": "TSH", "extra___5": "Free_T4", "extra___6": "T4",
                        "extra___7": "insulin", "extra___8": "OGTT", "extra___9": "Vitamin_D", "extra___10": "LH",
                        "extra___11": "FSH", "extra___12": "Serum_Testosterone", "extra___13": "Free_Testosterone",
                        "extra___14": "Beta_hCG", "extra___15": "DHEAS", "extra___16": "17_hydroxyprogesterone",
                        "extra___18": "independent_HDL", "extra___19": "independent_LDL",
                        "extra___20": "independent_triglycerides", "extra___21": "BMP",
                        "extra___22": "independent_cholesterol", "extra___23": "Hepatic_panel"})


df = df.rename(columns={"stigmatizing___0": "none", "stigmatizing___1": "morbid_extreme_obesity",
                        "stigmatizing___2": "patient_language","stigmatizing___3": "weight_check",
                        "stigmatizing___4": "buffalo_hump", "stigmatizing___5": "general_appearance",
                        "stigmatizing___6": "other"})


labels = ["Baseline, 3, 6, 9, 18"]
eAndZCodes = ["both_codes", "z_only", "e_only", "no_codes"]
stigmatizingYesNo = ["none"]
stigmatizingBreakdown = ["morbid_extreme_obesity", "patient_language", "weight_check", "buffalo_hump",
                         "general_appearance", "other"]
extraLabsYesNo = ["no_extra"]
extraLabsBreakdown = ["AST", "Glucose", "CMP", "TSH", "Free_T4", "T4", "insulin", "OGTT", "Vitamin_D", "LH", "FSH",
                      "Serum_Testosterone", "Free_Testosterone", "Beta_hCG", "DHEAS", "17_hydroxyprogesterone",
                      "independent_HDL", "independent_LDL", "independent_triglycerides", "BMP",
                      "independent_cholesterol", "Hepatic_panel"]

graphs = [eAndZCodes, stigmatizingYesNo, stigmatizingBreakdown, extraLabsYesNo, extraLabsBreakdown]

dfAnacostia = df.loc[df["site"] == 2]
dfAnacostia = dfAnacostia.dropna(subset=["months"])
dfAnacostiaYoung = dfAnacostia.loc[dfAnacostia["age"] <= 8]
dfAnacostiaOld = dfAnacostia.loc[dfAnacostia["age"] > 8]


dfYoung = df.loc[df["age"] <= 8]
dfOld = df.loc[df["age"] > 8]

x = numpy.array([0, 3, 6, 9, 18])
ticks = ["Baseline", "3", "6", "9", "18"]

# dfYoung.groupby(["months", "location"])[stigmatizingYesNo].mean().unstack("location").plot(kind="line")
# plt.title("(2-8): Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xticks(x, ticks)
# plt.xlabel("Months")
# plt.show()
#
# dfOld.groupby(["months", "location"])[stigmatizingYesNo].mean().unstack("location").plot(kind="line")
# plt.title("(9-18): Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xticks(x, ticks)
# plt.xlabel("Months")
# plt.show()

# # E and Z Codes Anacostia
# dfAnacostia.groupby("months")[eAndZCodes].mean().plot(kind="bar")
# plt.title("Anacostia: Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfAnacostia.groupby("months")[eAndZCodes].mean().plot(kind="line")
# plt.title("Anacostia: Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaYoung.groupby("months")[eAndZCodes].mean().plot(kind="bar")
# plt.title("Anacostia (age 2-8): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.show()
# dfAnacostiaYoung.groupby("months")[eAndZCodes].mean().plot(kind="line")
# plt.title("Anacostia (age 2-8): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaOld.groupby("months")[eAndZCodes].mean().plot(kind="bar")
# plt.title("Anacostia (age 9-18): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfAnacostiaOld.groupby("months")[eAndZCodes].mean().plot(kind="line")
# plt.title("Anacostia (age 9-18): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# # Stigmatizing Language Anacostia Yes/No
# dfAnacostia.groupby("months")[stigmatizingYesNo].mean().plot(kind="line")
# plt.title("Anacostia: Use Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaYoung.groupby("months")[stigmatizingYesNo].mean().plot(kind="line")
# plt.title("Anacostia (age 2-8): Use of Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaOld.groupby("months")[stigmatizingYesNo].mean().plot(kind="line")
# plt.title("Anacostia (age 9-18): Use of Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# #Stigmatizing Breakdown Anacostia
# dfAnacostia.groupby("months")[stigmatizingBreakdown].mean().plot(kind="bar")
# plt.title("Anacostia: Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfAnacostia.groupby("months")[stigmatizingBreakdown].mean().plot(kind="line")
# plt.title("Anacostia: Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaYoung.groupby("months")[stigmatizingBreakdown].mean().plot(kind="bar")
# plt.title("Anacostia (age 2-8): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfAnacostiaYoung.groupby("months")[stigmatizingBreakdown].mean().plot(kind="line")
# plt.title("Anacostia (age 2-8): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaOld.groupby("months")[stigmatizingBreakdown].mean().plot(kind="bar")
# plt.title("Anacostia (age 9-18): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfAnacostiaOld.groupby("months")[stigmatizingBreakdown].mean().plot(kind="line")
# plt.title("Anacostia (age 9-18): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# # Extra labs yes no Anacostia
# dfAnacostia.groupby("months")[extraLabsYesNo].mean().plot(kind="line")
# plt.title("Anacostia: Extra Labs")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaYoung.groupby("months")[extraLabsYesNo].mean().plot(kind="line")
# plt.title("Anacostia (age 2-8):Extra Labs")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfAnacostiaOld.groupby("months")[extraLabsYesNo].mean().plot(kind="line")
# plt.title("Anacostia (age 9-18): Extra Labs")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# # Extra lab breakdown Anacostia
# dfAnacostia.groupby("months")[extraLabsBreakdown].mean().plot(kind="bar")
# plt.title("Anacostia: Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfAnacostia.groupby("months")[extraLabsBreakdown].mean().plot(kind="line")
# plt.title("Anacostia: Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
# #
# dfAnacostiaYoung.groupby("months")[extraLabsBreakdown].mean().plot(kind="bar")
# plt.title("Anacostia (age 2-8): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.show()
dfAnacostiaYoung.groupby("months")[extraLabsBreakdown].mean().plot(kind="line")
plt.title("Anacostia (age 2-8): Extra Labs Breakdown")
plt.ylabel("Percentage of Charts")
plt.xticks(x, ticks)
plt.show()
#
# dfAnacostiaOld.groupby("months")[extraLabsBreakdown].mean().plot(kind="bar")
# plt.title("Anacostia (age 9-18): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.show()
# dfAnacostiaOld.groupby("months")[extraLabsBreakdown].mean().plot(kind="line")
# plt.title("Anacostia (age 9-18): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xticks(x, ticks)
# plt.show()

dfArc = df.loc[df["site"] == 1]
dfArcYoung = dfArc.loc[dfArc["age"] <= 8]
dfArcOld = dfArc.loc[dfArc["age"] > 8]


# THEARC e and z codes
# dfArc.groupby("months")[eAndZCodes].mean().plot(kind="bar")
# plt.title("THEARC: Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArc.groupby("months")[eAndZCodes].mean().plot(kind="line")
# plt.title("THEARC: Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcYoung.groupby("months")[eAndZCodes].mean().plot(kind="bar")
# plt.title("THEARC (age 2-8): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArcYoung.groupby("months")[eAndZCodes].mean().plot(kind="line")
# plt.title("THEARC (age 2-8): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcOld.groupby("months")[eAndZCodes].mean().plot(kind="bar")
# plt.title("THEARC (age 9-18): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArcOld.groupby("months")[eAndZCodes].mean().plot(kind="line")
# plt.title("THEARC (age 9-18): Use of E and Z codes")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()

# THEARC stigmatizing Language Yes/No
# dfArc.groupby("months")[stigmatizingYesNo].mean().plot(kind="line")
# plt.title("THEARC: Use Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcYoung.groupby("months")[stigmatizingYesNo].mean().plot(kind="line")
# plt.title("THEARC (age 2-8): Use of Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcOld.groupby("months")[stigmatizingYesNo].mean().plot(kind="line")
# plt.title("THEARC (age 9-18): Use of Stigmatizing Language")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#


# THEARC stigmatizing language Breakdown
# dfArc.groupby("months")[stigmatizingBreakdown].mean().plot(kind="bar")
# plt.title("THEARC: Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArc.groupby("months")[stigmatizingBreakdown].mean().plot(kind="line")
# plt.title("THEARC: Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcYoung.groupby("months")[stigmatizingBreakdown].mean().plot(kind="bar")
# plt.title("THEARC (age 2-8): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArcYoung.groupby("months")[stigmatizingBreakdown].mean().plot(kind="line")
# plt.title("THEARC (age 2-8): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcOld.groupby("months")[stigmatizingBreakdown].mean().plot(kind="bar")
# plt.title("THEARC (age 9-18): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArcOld.groupby("months")[stigmatizingBreakdown].mean().plot(kind="line")
# plt.title("THEARC (age 9-18): Stigmatizing Language Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# # Extra labs yes no Anacostia
# dfArc.groupby("months")[extraLabsYesNo].mean().plot(kind="line")
# plt.title("THEARC: Extra Labs")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcYoung.groupby("months")[extraLabsYesNo].mean().plot(kind="line")
# plt.title("THEARC (age 2-8):Extra Labs")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcOld.groupby("months")[extraLabsYesNo].mean().plot(kind="line")
# plt.title("THEARC (age 9-18): Extra Labs")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# # Extra lab breakdown THEARC
# dfArc.groupby("months")[extraLabsBreakdown].mean().plot(kind="bar")
# plt.title("THEARC: Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.show()
# dfArc.groupby("months")[extraLabsBreakdown].mean().plot(kind="line")
# plt.title("THEARC: Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xlabel("Months")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcYoung.groupby("months")[extraLabsBreakdown].mean().plot(kind="bar")
# plt.title("THEARC (age 2-8): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.show()
# dfArcYoung.groupby("months")[extraLabsBreakdown].mean().plot(kind="line")
# plt.title("THEARC (age 2-8): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xticks(x, ticks)
# plt.show()
#
# dfArcOld.groupby("months")[extraLabsBreakdown].mean().plot(kind="bar")
# plt.title("THEARC (age 9-18): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.show()
# dfArcOld.groupby("months")[extraLabsBreakdown].mean().plot(kind="line")
# plt.title("THEARC (age 9-18): Extra Labs Breakdown")
# plt.ylabel("Percentage of Charts")
# plt.xticks(x, ticks)
# plt.show()
