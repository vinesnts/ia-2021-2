# https://www.annytab.com/bayesian-networks-in-python/
# Import libraries
import pgmpy.models
import pgmpy.inference
import networkx as nx
import pylab as plt

ASSALTO = 'assalto'
ALARME = 'alarme'
TERREMOTO = 'terremoto'
JOAOLIGA = 'joaoliga'
MARIALIGA = 'marialiga'

model = pgmpy.models.BayesianModel([(ASSALTO, ALARME), 
                                    (TERREMOTO, ALARME),
                                    (ALARME, JOAOLIGA), 
                                    (ALARME, MARIALIGA)])

cpd_assalto = pgmpy.factors.discrete.TabularCPD(ASSALTO, 2, [[0.001], [0.999]])

cpd_terromoto = pgmpy.factors.discrete.TabularCPD(TERREMOTO, 2, [[0.002], [0.998]])

cpd_alarme = pgmpy.factors.discrete.TabularCPD(ALARME, 2, [[0.95, 0.94, 0.29, 0.001], 
                                                           [0.05, 0.06, 0.71, 0.999]], 
                                              evidence=[ASSALTO, TERREMOTO], 
                                              evidence_card=[2, 2])

cpd_joao = pgmpy.factors.discrete.TabularCPD(JOAOLIGA, 2, [[0.90, 0.05], 
                                                           [0.10, 0.95]], 
                                              evidence=[ALARME], 
                                              evidence_card=[2])

cpd_maria = pgmpy.factors.discrete.TabularCPD(MARIALIGA, 2, [[0.70, 0.01], 
                                                           [0.30, 0.99]], 
                                              evidence=[ALARME], 
                                              evidence_card=[2])

model.add_cpds(cpd_assalto, cpd_terromoto, cpd_alarme, cpd_joao, cpd_maria)

model.check_model()

print('Distribuição da probabilidade, P(Assalto)')
print(cpd_assalto)
print()
print('Distribuição da probabilidade, P(Terremoto)')
print(cpd_terromoto)
print()
print('Distribuição da probabilidade combinada, P(Alarme | Assalto, Terremoto)')
print(cpd_alarme)
print()
print('Distribuição da probabilidade combinada, P(JoaoLiga | Alarme)')
print(cpd_joao)
print()
print('Distribuição da probabilidade combinada, P(MariaLiga | Alarme)')
print(cpd_maria)
print()

infer = pgmpy.inference.VariableElimination(model)

posterior_probability = infer.query([ASSALTO], evidence={JOAOLIGA: 0, MARIALIGA: 0})

print('Qual a probabilidade do alarme ter tocado sem ocorrência de assalto nem terremoto, mas com ligação de João e Maria?')
print(posterior_probability)
print()