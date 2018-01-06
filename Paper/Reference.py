#!/usr/bin/python3
# -*- coding: UTF-8 -*-
with open("./references.txt", 'r') as f:
    refs = f.readlines()
    refs = sorted(refs)
with open("./references.txt", 'w') as w:
    w.write("\\begin{thebibliography}{1} \n")
    for k in range(len(refs)):
        string = "\\bibitem {" + str(k + 1) + "}\n" + str(refs[k]) + "\n"
        w.write(string)
    w.write("\\end{thebibliography} \n")
print("Finished")
