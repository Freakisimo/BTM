#encoding:utf-8

#Aplicacion
from graficas.models import *
#Shortcuts
from django.shortcuts import render_to_response
#Db
from django.db.models import Count, Avg, Q, Sum
#Core
from django.core.context_processors import csrf
#Template
from django.template import RequestContext
#Views
from django.views.decorators.csrf import csrf_protect
#utils
from django.utils import simplejson

import json
import numpy as np
import pandas
from collections import OrderedDict
import operator

# Vista principal
@csrf_protect
def Treemap(request):
	template = 'treemap.html'
	filtros = {}

	#########################################################
	###   Generar datos para llenar las tablas de nivel   ###
	###      Utilizar como ejemplo las hojas de excel     ###
	#########################################################

	# filtros

	if request.method == 'POST':
		#pais = request.POST['pais']
		
		mercado = request.POST['mercado']
		espe = request.POST['especialidad']		

		#filtros['pais'] = str(pais)
		filtros['mercado'] = str(mercado)
		filtros['espe'] = str(espe)

		
		pass

	#Limpia datos
	Resultados.objects.all().delete()

	# Asignar los niveles en orden.
	n0 = Niveles.objects.filter(nivel=0)
	n1 = Niveles.objects.filter(nivel=1)
	n2 = Niveles.objects.filter(nivel=2)
	n3 = Niveles.objects.filter(nivel=3)

	# Resultados
	# res = Resultados	

	for r0 in n0:
		inst = Institucion.objects.values('porcentaje').filter(institucion=r0.variable)
		p0 = ObtenTotal(inst)
		res = Resultados(nivel=0,institucion=r0.variable,promedio=p0)
		res.save()
		for r1 in n1:
			if r1.variable == 'Genotipo 1a':
				gen = 'gen1a'
			elif r1.variable == 'Genotipo 1b':
				gen = 'gen1b'
			elif r1.variable == 'Genotipo 2':
				gen = 'gen2'
			geno = Tbl3.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('casos_mono_'+gen))
			p1 = ObtenTotal(geno)
			res = Resultados(nivel=1,institucion=r0.variable,caracteristica='Monoinfectados',genotipo=r1.variable,promedio=p1)
			res.save()
			for r2 in n2:
				if r2.variable == 'Naive':
					tx = 'naive'
				elif r2.variable == 'Retratados':
					tx = 'retratados'
				tratamiento = Tbl4.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('casos_mono_'+tx+'_'+gen))
				p2 = ObtenTotal(tratamiento)
				res = Resultados(nivel=2,institucion=r0.variable,caracteristica='Monoinfectados',genotipo=r2.variable,tipo_paciente=r2.variable,promedio=p2)
				res.save()
				for r3 in n3:
					if r3.variable == u'Mayores de 70 años':
						edad = r3.variable
						h1 = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_h_20_30_'+gen+'_'+tx))
						nh1 = ObtenTotal(hombre)
						h2 = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_h_40_69_'+gen+'_'+tx))
						nh2 = ObtenTotal(hombre)
						h3 = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_h_60_69_'+gen+'_'+tx))
						nh3 = ObtenTotal(hombre)
						nhombre = (nh1+nh2+nh3) / 3
						
						m1 = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_m_20_30_'+gen+'_'+tx))
						nm1 = ObtenTotal(mujer)
						m2 = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_m_40_69_'+gen+'_'+tx))
						nm2 = ObtenTotal(mujer)
						m3 = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_m_60_69_'+gen+'_'+tx))
						nm3 = ObtenTotal(mujer)
						nmujer = (nm1+nm2+nm3) / 3
					else:
						edad = u'Menores de 70 años'
						hombre = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_h_70_'+gen+'_'+tx))
						mujer = Tbl5.objects.values('tipo').filter(institucion=r0.variable).annotate(promedio=Avg('mono_m_70_'+gen+'_'+tx))
						nhombre = ObtenTotal(hombre)
						nmujer = ObtenTotal(mujer)
					p3 = (nhombre + nmujer) / 2
					res = Resultados(nivel=3,institucion=r0.variable,caracteristica='Monoinfectados',genotipo=r2.variable,tipo_paciente=r3.variable,grupo_etario=r3.variable,grupo_etario2=edad,promedio=p3)
					res.save()
					pass
				pass
			pass
		pass

	# Niveles para json
	n0 = Resultados.objects.filter(nivel=0)
	n1 = Resultados.objects.filter(nivel=1)
	n2 = Resultados.objects.filter(nivel=2)
	n3 = Resultados.objects.filter(nivel=3)

	to_json = {"children": [], "data": {"$color": "#ffffff"}, "id": "root", "name": ""}

	# Agregar nivel 0
	for row in n0:
		nivel = {"children": [], "data": {"playcount": "", "$color": "#375623", "$area": row.promedio }, "id": str(row.institucion), "name": row.institucion+' '+"{0:.2f}".format((row.promedio*100))+'%'}
		to_json['children'].append(nivel)
		pass

	# Agregar nivel 1
	for row in n1:
		nivel = {"children": [], "data": {"playcount": "{0:.2f}".format((row.promedio*100)), "$color": "#70ad47", "$area": row.promedio }, "id": str(row.institucion)+' '+str(row.genotipo), "name": row.genotipo+' '+"{0:.2f}".format((row.promedio*100))+'%'}
		for child in to_json['children']:			
			if child['id'] == row.institucion:
				child['children'].append(nivel)
				pass
		pass
	
	# Agregar nivel 2
	for row in n2:
		nivel = {"children": [], "data": {"playcount": "{0:.2f}".format((row.promedio*100)), "$color": "#a9d08e", "$area": row.promedio }, "id": str(row.institucion)+' '+str(row.genotipo)+' '+str(row.tipo_paciente), "name": row.tipo_paciente+' '+"{0:.2f}".format((row.promedio*100))+'%'}
		for child in to_json['children']:			
			if child['id'] == row.institucion:
				for son in child['children']:					
					if son['id'] == row.institucion+" "+row.genotipo:
						son['children'].append(nivel)
						pass
				pass
		pass

	# Agregar nivel 3
	for row in n3:
		nivel = {"children": [], "data": {"playcount": "{0:.2f}".format((row.promedio*100)), "$color": "#D2DBBF", "$area": row.promedio }, "id": str(row.institucion)+' '+str(row.genotipo)+' '+str(row.tipo_paciente)+' '+str(row.grupo_etario2.encode("utf-8")), "name": row.grupo_etario2.encode("utf-8")+' '+"{0:.2f}".format((row.promedio*100))+'%'}
		print nivel
		for child in to_json['children']:
			if child['id'] == row.institucion:
				for son in child['children']:
					if son['id'] == row.institucion+' '+row.genotipo:
						for son2 in son['children']:
							if son2['id'] == row.institucion+' '+row.genotipo+' '+row.tipo_paciente:
								son2['children'].append(nivel)
								pass
						pass
				pass
		pass


	data = simplejson.dumps(to_json)
	filtros = simplejson.dumps(filtros)

	lista = {'lista':data, 'filtros':filtros}
	return render_to_response(template, lista, context_instance=RequestContext(request))



def Menu(request):
	template = "index.html"
	return render_to_response(template, context_instance=RequestContext(request))

def ObtenTotal(res):
	total = 0.0
	for row in res:		
		for val in row.values():
			if val != None and val != 'cuanti':
				total = val
				pass			

	return total