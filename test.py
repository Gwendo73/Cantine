mois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
for i in range(0, len(mois),4) :
        for j in range(i,i+4):
                print(mois[j], end=" ")
                # if (i%4==2):
        print(end="\n")
