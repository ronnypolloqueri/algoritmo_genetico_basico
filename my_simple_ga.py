#!/usr/bin/python2.7
# encoding: utf-8
import math
import random
import sys

class Individuo(object):

    def __init__(self, num_genes):
        self.fitness = 0
        self.cromosoma = self.crear_cromosoma(num_genes)

    def get_fitness(self):
        return self.fitness

    def set_fitness(self, fitness):
        self.fitness = fitness

    def set_cromosoma(self, cromosoma):
        self.cromosoma = cromosoma

    def crear_cromosoma(self, num_genes):
        return [self.crear_gen() for i in range(num_genes)]

    def get_cromosoma(self):
        return self.cromosoma

    def crear_gen(self):
        return random.randint(1, 9) # devuelve numeros entre [1;10]

    def __str__(self):
        return "%s => %s" % (self.cromosoma, self.fitness)

    def __repr__(self):
        return "%s => %s" % (self.cromosoma, self.fitness)

class MySimpleGA(object):
    def __init__(self, num_generaciones, num_individuos):
        super(MySimpleGA, self).__init__()
        self.modelo             = [1,1,1,1,1] # objetivo
        self.num_generaciones   = num_generaciones
        self.num_individuos     = num_individuos
        self.num_seleccionados  = int(math.ceil(self.num_individuos * 0.3))
        self.prob_mutacion      = 0.3
        self.generacion_actual  = 0
        self.num_genes          = len(self.modelo)
        self.poblacion          = None
        self.mejor_individuo    = None
        self.mejor_fitness      = 1 * self.num_genes

        print "Modelo: %s" % self.modelo
        print "Número de generaciones: %d" % self.num_generaciones
        print "Número de Individuos: \t%d" % self.num_individuos
        print "Numero de seleccionados: %d" % self.num_seleccionados
        self.inicializar_poblacion()
        self.ordenar_poblacion()
        print "Población: %s" % self.poblacion
        print "="*40

    def run(self):
        self.mejor_individuo = self.poblacion[0]
        print "Generación %d: \t%s" % ( self.generacion_actual,
                                        self.mejor_individuo )

        while self.generacion_actual <= self.num_generaciones and not self.esta_terminado():

            seleccionados = self.seleccionar_poblacion()
            self.cruzar_poblacion(seleccionados)
            self.mutar_poblacion()
            self.ordenar_poblacion()
            self.mejor_individuo = self.poblacion[0]

            self.generacion_actual += 1
            print "Generación %d: \t%s" % ( self.generacion_actual,
                                            self.mejor_individuo )
        print "Terminado"

    def esta_terminado(self):
        return self.mejor_individuo.get_fitness() == self.mejor_fitness

    def inicializar_poblacion(self):
        self.poblacion = [(Individuo(self.num_genes)) for i in range(self.num_individuos)]


    def seleccionar_poblacion(self):
        return self.poblacion[:self.num_seleccionados]

    def ordenar_poblacion(self):
        self.puntuar_poblacion()
        self.poblacion = sorted( self.poblacion, reverse=True, key=lambda i: i.get_fitness())

    def puntuar_poblacion(self):
        for p in self.poblacion:
            fitness = 0;
            cromosoma = p.get_cromosoma()
            for i in range(len(cromosoma)):
                if self.modelo[i] == cromosoma[i]:
                    fitness += 1
            p.set_fitness(fitness)

    def cruzar_poblacion(self, seleccionados):
        #self.cruce_de_un_punto(seleccionados)
        #self.cruce_de_dos_puntos(seleccionados)
        self.cruce_uniforme(seleccionados)

    def cruce_de_un_punto(self, seleccionados):
        for p in self.poblacion[self.num_seleccionados:]:
            padres = random.sample(seleccionados, 2)
            punto  = random.randint(1, self.num_genes - 1)
            cromosoma = p.get_cromosoma()
            cromosoma[:punto] = padres[0].get_cromosoma()[:punto]
            cromosoma[punto:] = padres[1].get_cromosoma()[punto:]
            p.set_cromosoma(cromosoma)

    def cruce_de_dos_puntos(self, seleccionados):
        for p in self.poblacion[self.num_seleccionados:]:
            padres = random.sample(seleccionados, 2)
            punto1 = random.randint(1, self.num_genes / 2)
            punto2 = random.randint(self.num_genes / 2, self.num_genes -1)
            cromosoma = p.get_cromosoma()
            cromosoma[:punto1] = padres[0].get_cromosoma()[:punto1]
            cromosoma[punto1:punto2] = padres[1].get_cromosoma()[punto1:punto2]
            cromosoma[punto2:] = padres[0].get_cromosoma()[punto2:]
            p.set_cromosoma(cromosoma)

    def cruce_uniforme(self, seleccionados):
        mascara = self.crear_mascara( self.num_genes )
        for p in self.poblacion[self.num_seleccionados:]:
            padres = random.sample(seleccionados, 2)
            punto  = random.randint(1, self.num_genes - 1)
            cromosoma = p.get_cromosoma()
            for i in range( self.num_genes ):
                cromosoma[i] = padres[mascara[i]].get_cromosoma()[i]
            p.set_cromosoma(cromosoma)

    # para cruce uniforme
    def crear_mascara(self, longitud):
        mascara = []
        for i in range(longitud):
            valor = 1 if random.random() > 0.5 else 0
            mascara.append(valor)
        return mascara


    def mutar_poblacion(self):
        for p in self.poblacion[self.num_seleccionados:]:
            if random.random() <= self.prob_mutacion:
                punto  = random.randint(1,self.num_genes - 1)
                cromosoma = p.get_cromosoma()
                nuevo_gen = random.randint(1,self.num_genes - 1)
                while cromosoma[punto] == nuevo_gen:
                    nuevo_gen = random.randint(1,self.num_genes)
                cromosoma[punto] = nuevo_gen
                p.set_cromosoma(cromosoma)

if __name__ == "__main__":
    if len(sys.argv) == 2 and ( sys.argv[1] == "-h" or sys.argv[1] == "--help"):
        print "MySimpleGA (1.0)"
        print "=========="
        print "Uso: ./my_simple_ga.py [numero_de_generaciones] [numero_de_individuos]"
        exit(0)
    try:
        num_generaciones = int(sys.argv[1])
    except Exception:
        num_generaciones = 100

    try:
        num_individuos = int(sys.argv[2])
    except Exception:
        num_individuos = 20

    MySimpleGA(num_generaciones, num_individuos).run()
