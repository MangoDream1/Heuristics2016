# Wat moet er gebeuren?

SCORE = 0

# pseudeocode lokalen (aparte class?)

# lokaal_score = 0

# voor elk lokaal --> read jsonfile
# 	voor elke dictionary in file (dag)
# 		voor elke dictionary in dag-dictionary (timeslot)
# 			als timeslot-dictionary > 1 (als er dus meerdere vakken zijn)
# 				if "name" == "Lecture" || "WorkLecture"
# 					lokaal_score = lokaal_score - 20 (punten aftrek voor dingen in hetzelfde lokaal)
# 				totaal_stud = totaal vak2 + totaal vak2
# 				aanwezig_stud = totaal_stud - capiciteit_lokaal
# 				if aanwezig_stud > 0
# 					lokaal_score = lokaal_score - aanwezig_stud
# 		als dag-dictionary == 5 (als het van 17-19 is)
# 			lokaal_score = lokaal_score - 50

# return lokaal_score



# pseudeocode studenten

# student_score = 0

# voor elke student --> read jsonfile
# 	voor elke dictionary in file (dag)
# 		voor elke dictionary in dag-dictionary (timeslot)
# 			als time-slot dictionary > 1 (conflict)
# 				malus = dictionary-size - 1
# 				student_score = student_score - malus

# return student_score



# pseudocode zaalslot

# geldig_score = 0

# maak een lijst/dictionary met alle vakken en hoeveelheid activiteiten??

# voor elk lokaal --> read jsonfile van lokaal
# 	voor elke dictionary (dag)
# 		voor elke dictionary (timeslot)
# 			vak = "name"
# 			vergelijk met lijst (FUNCTIE)
# geldig_score = (kijk of geldigfunctie)
# return geldig_score

# vergelijk met lijst functie (krijgt naam mee)
# voor elk vak
# 	als vak == naam
# 		vak activiteiten = vak activiteiten - 1

# kijk of geldigfunctie
# voor elk vak
# 	als vak activiteiten != 0
# 	ongeldig --> return 0
# geldig --> return 1000



# pseudeocode vakkenverdeling

# vakken_score = 0

# maak lijst met vak + aantal activiteiten + dagen?
# v.b.
# {"heuristieken" : {"activiteiten" : 2, "ma" : 1, "di" : 0, "wo" : 0, "do" : 1, "vr" : 0}}

# voor elk vak
# 	als activiteiten = 2
# 		als ("ma" == 1 && "do" == 1)
# 			vakken_score + 20
# 		else if ("di" == 1 && "vr" == 1)
# 			vakken_score + 20
# 	als activiteiten = 3
# 		als ("ma" == 1 && "wo" == 1 && "vr" == 1)
# 			vakken_score + 20
# 	als activiteiten = 4
# 		als ("ma" == 1 && "di" == 1 && "do" == 1 && "vr" == 1)
# 			vakkenscore + 20

# return vakkenscore



# SCORE = vakkenscore + student_score + lokaal_score + geldig_score