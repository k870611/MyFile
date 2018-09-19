import subprocess


def open_excel(file_name):
    cmd = "assoc .xlsm"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    assoc_xlsm = str(p.communicate()[0].splitlines()[0]).split("=")[1].replace("'", "")
    print(assoc_xlsm)

    cmd = "ftype " + assoc_xlsm
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ftype_xlsm = str(p.communicate()[0].decode("utf-8")).split("\"")[1]
    print(ftype_xlsm)

    cmd = "{} {}".format(ftype_xlsm, str(file_name))
    print(cmd)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    print(str(p.communicate()[0].decode("utf-8")))


open_excel("xlsm.xlsx")


