# -*- coding: utf-8 -*-
"""
@authors: MF & RM
"""
import pdb
from collections import Counter
import numpy as np
import operator

class Skill(object):
    #Skill class, also used for subskills
    def __init__(self,name :str):
        self.name=name
        self.sub_skills=set()
    def addsub_skill(self,sub_skill):
        sub_skills=self.sub_skills
        sub_skills.add(sub_skill)
        return
    def getskill(self):
        return self.name
        
    
    def getsub_skills(self):
        return self.sub_skills
class Job(object):
    #class variable
    dictionnary_of_job_skills=dict()
    def __init__(self, name, sector = None, family = None, description = None):
        self.name = name
        self.description = description
        self.sector = sector
        self.family = family
        #if you've already found the job in the dict. you grasp its the dict. of skills otherwise you create a new one
        try:
            self.competences=Job.dictionnary_of_job_skills[self.name]
        except KeyError:
            self.competences=dict()
            Job.dictionnary_of_job_skills.update({self.name : self.competences}) # name of the job : pointer towards the dict of skills
    def setDescription(self, description):
        self.description = description
    def getCompetenceByName(self, name: str):
        for competence in self.competences:
            if competence.name == name:
                return competence
        return None        
    def addSkill(self,skill :str):
        self.competences.add(Skill(skill))
    def addSkills(self,skill :str,sub_skill :str):
        trouvé=False
        competences = self.competences
        for key in competences.keys():
            if key == skill:
                competences[key].addsub_skill(sub_skill) #skill found in the skills dict just add the subskill to it
                trouvé=True
                break
        if not(trouvé):
            skill_object = Skill(skill) #skill not found add the skill and the subskill
            skill_object.addsub_skill(sub_skill)
            competences.update({skill_object.name : skill_object}) #update skill dict
            self.competences=competences
    def getCompetence(self):
        return Job.dictionnary_of_job_skills[self.name]
    def getCompetenceName(self):
        competenceName=[]
        for value in Job.dictionnary_of_job_skills[self.name]:
            competenceName.append(value.name)
        return competenceName
    def distance(self, job_object, skill_count :dict):
        score = 0
        total = 0
        skills_current_job = self.getCompetence()
        skills_other_job = job_object.getCompetence()
        common_keys = set(skills_current_job.keys()).intersection(set(skills_other_job.keys())) #get the keys of the common skills
        #Clusterisation    
        if len(common_keys)>0:
            for key in common_keys:
                score += -np.log(1/skill_count[key])
                current_sub_skills = set(skills_current_job[key].getsub_skills()) 
                other_sub_skills = set(skills_other_job[key].getsub_skills())
                common_sub_skills = current_sub_skills.intersection(other_sub_skills) #get also its subskills in common
                if len(common_sub_skills)>0:
                    score*=len(common_sub_skills)**(3/2)  
        total = score
        symetrical_difference_keys = set(skills_current_job.keys()) ^ set(skills_other_job.keys()) #check also the skills not in common and add it to the total
        for key in symetrical_difference_keys:
            total += -np.log(1/skill_count[key])
            
        return score/total
        
        
    
class Job_Ontology():
    def __init__(self):
        self.path = 'data_clean.json'
        self.IO_generator = iter(self.stream_read_json(self.path))
        self.jobset= dict()
        self.skill_count = Counter()
        self.build()
    def build(self):
        IO_generator = self.IO_generator
        jobset = self.jobset
        skill_count = self.skill_count
        #Reading the job ontology from the json via a job stream
        while True:
            #the try except thing is useful to read the stream when it's empty next returns a StopIteration, then you break
            try:
                elt=next(IO_generator)
                triplet = [elt['Métier'],elt['Compétence'],elt['Sous-compétences']] 
                job = Job(triplet[0])
                job.addSkills(triplet[1],triplet[2])#Linking the skill and the subskill to the job
                jobset.update({job.name : job}) #keys are the job name (str) and value the pointers towards the objects
                skill_count.update({triplet[1] : 1}) #Counting occurences of the jobs to get their frequences (useful in getFrequency)
            except StopIteration:
                break
    
    def stream_read_json(self,path):
        #creates the stream
        import json
        start_pos = 0
        with open(self.path, 'r', encoding='utf-8') as f:
            obj = list(json.load(f))
            for i in range(len(obj)):
                try:
                    yield obj[i]
    
                except json.JSONDecodeError as e:
                    f.seek(start_pos)
                    json_str = f.read(e.pos)
                    obj = json.loads(json_str)
                    start_pos += e.pos
                    yield obj[i]
            return
    def getFrequency(self):
        skill_count = dict(self.skill_count) #transtyping from counter type to dict type
        sum_of_competency=sum(skill_count.values()) 
        for key in skill_count.keys(): #keys of skillcount are the skills
            skill_count[key]/= sum_of_competency #calculating the frequency
        self.skill_count=skill_count
        return skill_count
    def getJobset(self):
        return self.jobset
    def getClosestJob(self, job :str):
        jobset = self.jobset
        job_object = jobset[job] #pointer towards the job object
        job_distances = dict() # keys are the jobs value are the distances
        for key_job in jobset.keys():
            if key_job == job:
                _=0 #do nothing to avoid 
            else :
                distance = job_object.distance(jobset[key_job],self.skill_count)
                job_distances.update({key_job : distance})
        sorted_job_distances = sorted(job_distances.items(), key= operator.itemgetter(1))
        return sorted_job_distances[-5:] #returns the five closest jobs from the farthest to the closest
                
