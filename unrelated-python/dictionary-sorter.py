noah = {
  "role" : "child",
  "position" : 2,
  "relations" : ["brother", "son"],
  "name / age" : ["noah", 19],
  } 
micah = {
  "role" : "child",
  "position" : 3,
  "relations" : ["brother", "son"],
  "name / age" : ["micah", 17],
  } 
luke = {
  "role" : "child",
  "position" : 4,
  "relations" : ["brother", "son"],
  "name / age" : ["luke", 15],
  } 
grace = {
  "role" : "child",
  "position" : 5,
  "relations" : ["sister", "daughter"],
  "name / age" : ["grace", 14],
  } 
jermaine = {
  "role" : "child",
  "position" : 0,
  "relations" : ["dad", "husband"],
  "name / age" : ["jermaine", 48],
  } 
zola = {
  "role" : "child",
  "position" : 1,
  "relations" : ["mum", "wife"],
  "name / age" : ["zola", 44],
  } 


#campbells = [noah['name / age'][0] , micah['name / age'][0] , #luke['name / age'][0] , grace['name / age'][0] , #jermaine['name / age'][0] , zola['name / age'][0]]

family = [zola,jermaine,grace,micah,noah,luke]
familyPositions = [zola['position'],jermaine['position'],grace['position'],micah['position'],noah['position'],luke['position']]
familyPositions.sort()

for i in range(len(family) - 1) :
  unordFamilyPos = family[i]['position']
  ordFamilyPos = familyPositions[i]

  if unordFamilyPos != ordFamilyPos:
    family[unordFamilyPos], family[ordFamilyPos] = family[ordFamilyPos], family[unordFamilyPos]

[print(i['name / age']) for i in family]

#i[b], i[a] = i[a], i[b]


