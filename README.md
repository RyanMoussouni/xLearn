# xLearn
# -- Job matcher

I made a job matching algorithm for xLearn. 
This algorithm uses a database they developed (data_clean.json).
An entry looks like something like this: \\
'''
{
  "key_shared_job": 0,
  "Secteur": "Numérique",
  "Famille": "Mise en production / Exploitation Probatoire",
  "Métier": "Administrateur bases de données",
  "Description": "L'Administrateur bases de données conçoit, gère et administre les systèmes de gestion de données de l'entreprise, en assure la cohérence, la qualité et la sécurité. Concevoir et spécifier les paramètres et l'architecture de la base de données en lien avec l'architecte SI (structure, paramètres, modélisation)\nAdministrer la base de données (suivi de la qualité des données, suivi du niveau de service, gestion des accès utilisateurs et de la sécurité)\nGérer les évolutions, migrations et back up dont la recette.\nMettre à jour les documents d'exploitation\nAssurer un support technique aux utilisateurs et aux équipes de développement\nGarantir auprès des utilisateurs internes et externes la confidentialité, l'intégrité et la disponibilité des donnéesAssurer une veille technique .",
  "Compétence": "Architecture technique SI",
  "Sous-compétences": "Analyser les acteurs et outils (matériel ou logiciel) du marché",
  "key_competency": "0",
  "key_sub-competency": "1"
}
'''
As you can notice, a job has some competencies and some sub-competencies.
To match jobs we relied on the following assumption: "two jobs are close to each other if they have a lot of competencies and sub-competencies in common".
It allowed us to create a metric that tells how close is one job to another. I thought using AI techniques for this problem would have been overkill, since this metric provides very good results.

## -- Example of result

Entry : 'Toxicologue industriel' \\
Results : \\
Best : ('Écotoxicologue', 1.0)\\
List of Bests: [('Écotoxicologue', 1.0, ('competency_match: ', 5), ('subcompetency_match:', 6)), ('Spécialiste en cosmétovigilance', 1.0, ('competency_match: ', 5), ('subcompetency_match:', 3)), \\
("Chargé d'études statistiques", 0.7975815245288584, ('competency_match: ', 4), ('subcompetency_match:', 0)), ('Ergonome logiciel', 0.7975815245288584, ('competency_match: ', 4), ('subcompetency_match:', 0)), \\
('Chef de projet', 0.7781211446285499, ('competency_match: ', 4), ('subcompetency_match:', 0))], 0.0)]

# -- Machine Learning Techniques : skills_ml

We studied the question during my internship. What AI could do, for instance, is trying to find some skills in a resume:  I was hired to work on this topic and I had to base my work on 
this white paper 		

			http://dataatwork.org/skills-ml/SkillsMLWhitepaper.pdf 

If you read it carefully, you find that the mean number of skills they can extract from one resume is of maximum 2 (depending on the ontology).
Their method doesn't work well : if you retrieve only two skills from a resume, it is very likely to be general skills that won't distinguish one resume from another. 
Therefore it is useless for what we aimed at doing: I discussed it with my supervisor and we decided not to go further.
