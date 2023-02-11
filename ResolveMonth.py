import pandas as pd
import os

headers_501=['Patente_aduanal', 'Indice', 'Clave_de_seccion_aduanera_de_despacho', 'Clave_de_tipo_de_operacion', 'Clave_de_documento', 'Clave_de_aduana_de_entrada', 
'Tipo_de_cambio', 'Total_de_fletes', 'Total_de_seguros', 'Total_de_embalajes', 'Total_de_otros_incrementales', 'Total_de_otros_deducibles', 'Peso_bruto_de_la_mercancia', 'Clave_de_medio_de_transporte_de_salida', 'Clave_de_medio_de_transporte_de_arribo', 'Clave_de_medio_de_transporte_de_entrada_o_salida', 'Clave_de_destino_de_la_mercancia', 'Clave_de_tipo_de_pedimento', 'Fecha_de_pago_real']


headers_551=['Patente_aduanal', 'Indice', 'Clave_de_seccion_aduanera_de_despacho', 'Fraccion_arancelaria', 'Secuencia_de_la_fracción_arancelaria', 'Subdivision_de_la_fraccion', 'Descripcion_de_la_mercancia', 'Precio_unitario', 'Valor_en_aduana', 'Valor_comercial', 'Valor_en_dolares', 'Cantidad_de_mercancia_en_unidades_de_medida_comercial', 'Clave_de_unidad_de_medida_comercial', 'Cantidad_de_mercancia_en_unidades_de_medida_de_la_tarifa', 'Clave_de_unidad_de_medida_de_la_tarifa', 'Valor_agregado', 'Clave_devinculacion', 'Clave_de_metodo_de_valorizacion', 'Codigo_de_la_mercancia_o_producto', 'Marca_de_la_mercancia_o_producto', 'Modelo_de_la_mercancia_o_producto', 'Clave_de_pais_origen/destino', 'Clave_de_pais_comprador/vendedor', 'Clave_de_entidad_federativa_de_origen', 'Clave_de_entidad_federativa_de_destino', 'Clave_de_entidad_federativa_de_comprador', 'Clave_de_entidad_federativa_de_vendedor', 'Fecha_de_pago_real']

headers_554 = ['Patente_aduanal', 'Indice','Clave_de_seccion_aduanera_de_despacho','Fraccion_arancelaria','Secuencia_de_la_fracción_arancelaria','Clave_de_caso','Identificador_del_caso', 'Fecha_de_pago_real']

headers_552 = ['Patente_aduanal','Indice','Clave_de_seccion_aduanera_de_despacho','Fraccion_arancelaria','Secuencia_de_la_fraccion_arancelaria','Kilometraje_del_vehiculo','Fecha_de_pago_real']



def txtToCsv(file_name):
    if file_name == "t_501":
        headers = headers_501
    elif file_name == "t_551_01" or file_name == "t_551_02":
        headers = headers_551
    elif file_name == "t_554_01" or file_name == "t_554_02":
        headers = headers_554
    elif file_name == "t_552":
        headers = headers_552
    pd.read_csv(file_name+".txt", sep="|", header=None, names=headers+["NUL"], encoding='latin1') \
        .drop("NUL", axis=1) \
        .to_csv(file_name+".csv", index=False)
    return file_name+".csv"


def joinFiles(file1, file2, name):
    df = pd.concat(
    map(pd.read_csv, [file1, file2]), ignore_index=True)
    NewFileName = name + '.csv'
    os.remove(file1)
    os.remove(file2)
    df.to_csv(NewFileName, index=False)
    return NewFileName

def merge(file1, file2, name):
    pd1 = pd.read_csv(file1)
    pd2 = pd.read_csv(file2)

    merged_df = pd.merge(pd1, pd2, how='inner')
    merged_df.to_csv(name, index=False)
    os.remove(file1)
    os.remove(file2)
    return name
 
def filter_551():
    df = pd.read_csv('t_551.csv')
    df.query("Fraccion_arancelaria.astype('str').str.startswith('8704') | Fraccion_arancelaria.astype('str').str.startswith('8703')", inplace=True)
    df.to_csv('t_551.csv', index=False)  

def filter_501():
    df = pd.read_csv('t_501.csv')
    df.query("Clave_de_tipo_de_operacion == 1", inplace=True)
    df.to_csv('t_501.csv', index=False)

def filter_554():
    df = pd.read_csv('t_554.csv')
    df.query("Clave_de_caso == 'ES' & Identificador_del_caso == 'U'", inplace=True)
    df.to_csv('t_554.csv', index=False)

def filter_clean():
    df = pd.read_csv('Final.csv')
    # df.query("not (type.str.startswith('ATV'))", inplace=True)
    # df.query("type != 'Dump Trucks > 30 ton' & type != 'specialty electric (snow mobiles, golf, others)' & not (type.str.startswith('ATV'))", inplace=True)
    df = df[["type","description","make","model","weight","km","producer","exporter","entry","destination","transportation","units","date","Total_de_fletes","Total_de_seguros", "Total_de_embalajes","Total_de_otros_incrementales","Total_de_otros_deducibles",  "Precio_unitario","Valor_en_aduana","Valor_comercial","Valor_en_dolares","Tipo_de_vehiculo"]]
    df.drop_duplicates(inplace=True)
    df.to_csv('Final.csv', index=False)

def translate_values():
    df = pd.read_csv('Final.csv')  
    df2 = pd.read_csv('typeClass.csv')
    df['Tipo_de_vehiculo'] = df['Fraccion_arancelaria'].map(df2.set_index('code')['description'])
    df.to_csv('Final.csv', index=False)

def changeHeaders():
    df = pd.read_csv('Final.csv')
    df = df.rename(columns={'Fraccion_arancelaria': 'type', 'Descripcion_de_la_mercancia': 'description', 'Fecha_de_pago_real': 'date', 'Marca_de_la_mercancia_o_producto': 'make', 'Modelo_de_la_mercancia_o_producto': 'model', 'Peso_bruto_de_la_mercancia': 'weight', 'Kilometraje_del_vehiculo': 'km', 'Valor_en_dolares': 'Valor_en_dolares', 'Clave_de_pais_origen/destino': 'producer', 'Clave_de_pais_comprador/vendedor': 'exporter', 'Clave_de_seccion_aduanera_de_despacho': 'entry', 'Clave_de_destino_de_la_mercancia': 'destination', 'Clave_de_medio_de_transporte_de_arribo': 'transportation', 'Cantidad_de_mercancia_en_unidades_de_medida_comercial': 'units',"Tipo_de_carro": "Tipo_de_vehiculo"})
    df.to_csv('Final.csv', index=False)

def getYears():
    df = pd.read_csv('Final.csv')
    df["year"] = ""
    for index, row in df.iterrows():
        for word in str(row["model"]).split(" "):
            if word.isdigit() and len(word) == 4 and int(word) > 1985 and int(word) < 2023:
                df["year"][index] = word
                break
    
    # for index, ro in df.iterrows();
    df.to_csv('Final.csv', index=False)

if __name__ == '__main__':
    # Process 501
    txtToCsv("t_501")
    filter_501()

    # Process 551
    file1 = txtToCsv("t_551_01")
    file2 = txtToCsv("t_551_02")
    joinFiles(file1, file2, "t_551")
    filter_551()

    # #Join 501 and 551
    current = merge("t_501.csv", "t_551.csv", "clean.csv")

    # #Process 554
    file1 = txtToCsv("t_554_01")
    file2 = txtToCsv("t_554_02")
    joinFiles(file1, file2, "t_554")
    filter_554()
    merge("t_554.csv", current, "t_501-551-554.csv")

    # # #Process 552
    txtToCsv("t_552")
    merge("t_552.csv", "t_501-551-554.csv", "Final.csv")
    translate_values()
    changeHeaders()
    filter_clean()
    getYears()
