from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


username = "d.gonzalez.moreno"
options = Options()
options.add_argument("user-data-dir=C:\\Users\\" + username + "\\AppData\\Local\\Google\\Chrome\\User Data")
chromedriver = "C:\\Users\\d.gonzalez.moreno\\Documents\\ChromeDrivers\\chromedriver.exe"
driver = webdriver.Chrome(chromedriver, options = options)
print("Accediendo a SP")
#driver = webdriver.Chrome(chromedriver)
driver.get("https://ts.accenture.com/sites/BancoDeChile/Operacion/Lists/Vacaciones/AllItems.aspx")
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}")))

#print(elem)
#elem.click()
num_rows = len (driver.find_elements_by_xpath("//*[@id='{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}']/tbody/tr"))
num_cols = len (driver.find_elements_by_xpath("//*[@id='{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}']/tbody/tr[2]/td"))
#print(num_rows)
#print(num_cols)
before_XPath="//*[@id='{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}']/tbody/tr["
aftertd_XPath="]/td["
aftertr_XPath="]"

before_XPath_H="//*[@id='{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}']/thead/tr/th["
after_XPath_H="]"

lista_aux=list()
lista_all=list()
lista_ap=list()
print("Obteniendo cabeceras")

for x in range(1,(num_cols+1)):
	h_text=before_XPath_H + str(x) + after_XPath_H
	head_text = driver.find_element_by_xpath(h_text).text
	lista_aux.append(head_text)

print("Obteniendo Aprobados")

for t_row in range(1,(num_rows+1)):
	lista_aux=list()
	for t_column in range(1, (num_cols + 1)):
		FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
		cell_text = driver.find_element_by_xpath(FinalXPath).text
		#print(cell_text)
		lista_aux.append(cell_text)
	lista_all.append(lista_aux)
	if lista_aux[-1]=='Approved':
		lista_ap.append(lista_aux)
	



flag=num_rows
while flag==30:
	try:
		elem = driver.find_element_by_xpath("//*[@id='pagingWPQ1next']")
		elem.click()
		print("esperar para obtener datos")
		wait = WebDriverWait(driver, 10)#Obtenemos numero de filas y columnas
		WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "pagingWPQ1prev")))
		num_rows = len (driver.find_elements_by_xpath("//*[@id='{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}']/tbody/tr"))
		num_cols = len (driver.find_elements_by_xpath("//*[@id='{ADBA8E93-DF74-47FB-9245-D69632D2BF14}-{F17244E0-B3A6-40A4-BE78-4B8810116BD4}']/tbody/tr[2]/td"))


		flag=num_rows
		for t_row in range(1,(num_rows+1)):
			lista_aux=list()
			for t_column in range(1, (num_cols + 1)):
				FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
				cell_text = driver.find_element_by_xpath(FinalXPath).text
				lista_aux.append(cell_text)
			lista_all.append(lista_aux)
			if lista_aux[-1]=='Approved':
			
				lista_ap.append(lista_aux)

		print("Lista de aprobados: "+lista_ap)
	except Exception as e:
		flag=-1
	

print("Accediendo a ARS")

driver.get("https://ars.accenture.com/index.php?r=site/login")
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BotonEntrar")))
elem.click()


#######################Segunda Parte###########################################
for x in range(0,len(lista_ap)):
	lista_ap[x][1]=(lista_ap[x][1].split(",")[1] +" "+ lista_ap[x][1].split(",")[0])

driver.get("https://ars.accenture.com/index.php?r=buscarRequerimiento/index")
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "BuscarRequerimientosForm_NumeroRequerimiento")))
elem.send_keys("452")
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@value,'Buscar')]")))
elem.click()
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='yt3']")))
elem.click()
elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='yt0']")))
elem.click()

try:
	print("Buscar Tarea de Vacaciones Aotomatización")
	elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Vacaciones - Automatizacion']")))
	elem.click()
except Exception as e:
	print("No se encontró Tarea de Vacaciones Aotomatización, creando Tarea")
	elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@value='Asignar Tarea']")))
	elem.click()
	try:
		print("esperando 10 seg")
		elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
	except Exception as e:
		print("fin de espera")
	WebDriverWait(driver, 30)
	elem = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//*[@id='tabla_listado_tar_asign_2']")))
	Guardar=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='boton-crear-tarea']")))
	num_rows = len (driver.find_elements_by_xpath("//*[@id='tabla_listado_tar_asign_2']/tbody/tr"))
	num_cols = len (driver.find_elements_by_xpath("//*[@id='tabla_listado_tar_asign_2']/tbody/tr[2]/td"))
	print(num_rows)
	print(num_cols)

	before_XPath="//*[@id='tabla_listado_tar_asign_2']/tbody/tr["
	aftertd_XPath="]/td["
	aftertr_XPath="]"

	lista_aux=list()
	for t_row in range(1,(num_rows+1)):
		lista_aux=list()
		for t_column in range(1, (num_cols + 1)):
			FinalXPath = before_XPath + str(t_row) + aftertd_XPath + str(t_column) + aftertr_XPath
			cell_text = driver.find_element_by_xpath(FinalXPath).text
			lista_aux.append(FinalXPath)

		

		if driver.find_element_by_xpath(lista_aux[1]).text=="Vacaciones":
			elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, lista_aux[0])))

		
	elem.click()
	Guardar.click()
	print("Tarea Creada, agregando descripción")
	elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/button")))
	elem.click()
	elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='tabla_listado_']/tbody/tr[1]/td[3]/div/a")))
	elem.click()
	elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@name='DesarrolloForm[TareaObservaciones]']")))
	elem.send_keys("Automatizacion")
	elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='boton-guardar-tarea-2']")))
	elem.click()
	elem=WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[3]/div/button")))
	elem.click()
	webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
	elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Vacaciones - Automatizacion']")))
	elem.click()
	
try:
	print("esperando 2 seg")
	elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
except Exception as e:
	print("fin de espera")
listaAgregados=list()



for x in range(0,len(lista_ap)):
	flagEncontrado=-1	
	optionPath="//*[@id='personasGT']/option[text()='"+lista_ap[x][1].strip(" ")+"']"
	print("intentando agregar a "+lista_ap[x][1].strip(" "))
	try:

		elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, optionPath)))
		elem.click()

		try:
			print("esperando 2 seg")
			elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
		except Exception as e:
			print("fin de espera")

		elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Asignar Persona']")))
		elem.click()
		lista_ap[x][1]=lista_ap[x][1].strip(" ")
		listaAgregados.append(lista_ap[x][1])
		flagEncontrado=1
		print("Agregado: "+lista_ap[x][1].strip(" "))
	except Exception as e:
		print("usuario: "+lista_ap[x][1].strip(" ")+" no encontrado o ya ha sido asignado")
		
		NombreFormato2=lista_ap[x][1].strip(" ").split(" ")[0]+" "+lista_ap[x][1].strip(" ").split(" ")[1]
		print("Buscar por segundo formato: "+ NombreFormato2)
		optionPath="//*[@id='personasGT']/option[text()='"+NombreFormato2+"']"
		try:
			elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, optionPath)))
			elem.click()

			try:
				print("esperando 2 seg")
				elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
			except Exception as e:
				print("fin de espera")

			elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Asignar Persona']")))
			elem.click()
			lista_ap[x][1]=NombreFormato2
			listaAgregados.append(NombreFormato2)
			flagEncontrado=1
			print("Agregado: "+NombreFormato2)
		except Exception as e:
			print("usuario: "+NombreFormato2+" en segundo formato, no encontrado o ya ha sido asignado")
			NombreFormato3=lista_ap[x][1].strip(" ").replace("Á","A").replace("á","a").replace("É","E").replace("é","e").replace("Í","I").replace("í","i").replace("ó","o").replace("Ó","O").replace("ú","u").replace("Ú","U").upper()
			print("Buscar por tercer formato: "+ NombreFormato3)
			largoOpciones=len (driver.find_elements_by_xpath("//*[@id='personasGT']/option"))
			
			for i in range(1,largoOpciones):
				optionPathAux="//*[@id='personasGT']/option["+str(i)+"]"
				optionAux = driver.find_element_by_xpath(optionPathAux).text.strip(" ").replace("Á","A").replace("á","a").replace("É","E").replace("é","e").replace("Í","I").replace("í","i").replace("ó","o").replace("Ó","O").replace("ú","u").replace("Ú","U").upper()
				GuardarNombre=driver.find_element_by_xpath(optionPathAux).text
				
				if(optionAux==NombreFormato3):
					i=largoOpciones
					flagEncontrado=1
					print("Procesando: "+GuardarNombre)
					try:
						elem = driver.find_element_by_xpath(optionPathAux)
						elem.click()

						try:
							print("esperando 2 seg")
							elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
						except Exception as e:
							print("fin de espera")

						elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Asignar Persona']")))
						elem.click()
						lista_ap[x][1]=GuardarNombre					
						listaAgregados.append(GuardarNombre)
						print("Agregado: "+GuardarNombre)

					except Exception as e:
						print("Error en usuario: "+lista_ap[x][1]+" en tercer formato")

			if flagEncontrado==-1:
				NombreFormato2=lista_ap[x][1].strip(" ").split(" ")[0]+" "+lista_ap[x][1].strip(" ").split(" ")[1]
				NombreFormato3=NombreFormato2.replace("Á","A").replace("á","a").replace("É","E").replace("é","e").replace("Í","I").replace("í","i").replace("ó","o").replace("Ó","O").replace("ú","u").replace("Ú","U").upper()
				print("Tercer formato no encontra, buscando por cuarto formato: "+ NombreFormato3)

				for i in range(1,largoOpciones):
					optionPathAux="//*[@id='personasGT']/option["+str(i)+"]"
					optionAux = driver.find_element_by_xpath(optionPathAux).text.strip(" ").replace("Á","A").replace("á","a").replace("É","E").replace("é","e").replace("Í","I").replace("í","i").replace("ó","o").replace("Ó","O").replace("ú","u").replace("Ú","U").upper()
					GuardarNombre=driver.find_element_by_xpath(optionPathAux).text
				
					if(optionAux==NombreFormato3):
						i=largoOpciones
						flagEncontrado=1
						print("Procesando: "+GuardarNombre)
						try:
							elem = driver.find_element_by_xpath(optionPathAux)
							elem.click()

							try:
								print("esperando 2 seg")
								elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
							except Exception as e:
								print("fin de espera")

							elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@title='Asignar Persona']")))
							elem.click()
							lista_ap[x][1]=GuardarNombre					
							listaAgregados.append(GuardarNombre)
							print("Agregado: "+GuardarNombre)
						except Exception as e:
							flagEncontrado=0
							print("Error en usuario: "+lista_ap[x][1]+" en cuarto formato")			

	if flagEncontrado==1:
		print("Usuario: "+lista_ap[x][1]+" Agregado Correctamente")
	if flagEncontrado==0:
		print("Usuario: "+lista_ap[x][1]+" No fue aregado debido a error")
	if flagEncontrado==-1:
		print("Usuario: "+lista_ap[x][1]+" No encontrado o ya ha sido asignado")
	 

try:
	print("esperando 2 seg")
	elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
except Exception as e:
	print("fin de espera")

elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='boton-guardar-tarea-2']")))
elem.click()

print(listaAgregados)
print(lista_ap)

#################Tercera parte#################################################



for x in range(0,len(listaAgregados)):
	driver.get("https://ars.accenture.com/index.php?r=ingresoHoras/index")
	elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='boton_limpiar']")))
	elem.click()
	optionPath="//*[@id='IngresoHorasForm_cuenta']/option[text()='"+listaAgregados[x]+"']"
	elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, optionPath)))
	elem.click()

	try:
		print("esperando 2 seg")
		elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[@value='No existe']")))
	except Exception as e:
		print("fin de espera")

	elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//*[@id='boton_buscar']")))
	elem.click()
	