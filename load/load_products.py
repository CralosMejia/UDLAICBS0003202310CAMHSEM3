from util.db_connection import connect
from util.properties import getProperty

import traceback
import pandas as pd


def load_products():
    try:
        #"PROD_ID","PROD_NAME","PROD_DESC","PROD_CATEGORY","PROD_CATEGORY_ID","PROD_CATEGORY_DESC","PROD_WEIGHT_CLASS","SUPPLIER_ID","PROD_STATUS","PROD_LIST_PRICE","PROD_MIN_PRICE"
                
        name_DB_stg = getProperty("DBSTG")
        name_DB_sor = getProperty("DBSOR")
        
        
        ses_db_stg = connect(name_DB_stg);
        ses_db_sor = connect(name_DB_sor);
        
        #Dictionary for values of chanels
        products_dict = {
            "prod_id":[],
            "prod_name":[],
            "prod_desc":[],
            "prod_category":[],
            "prod_category_id":[],
            "prod_category_desc":[],
            "prod_weight_class":[],
            "supplier_id":[],
            "prod_status":[],
            "prod_list_price":[],
            "prod_min_price":[]
        }
        
        #Reading the csv file
        products_tra_table = pd.read_sql('SELECT PROD_ID,PROD_NAME,PROD_DESC,PROD_CATEGORY,PROD_CATEGORY_ID,PROD_CATEGORY_DESC,PROD_WEIGHT_CLASS,SUPPLIER_ID,PROD_STATUS,PROD_LIST_PRICE,PROD_MIN_PRICE FROM products_tra', ses_db_stg)
        
        if not products_tra_table.empty:
            for id,name,prodD,prodCate,prodCateId,prodCateD,prodWeiC,supliId,prodS,prodLiPri,prodMinPri in zip(
                products_tra_table["PROD_ID"],
                products_tra_table["PROD_NAME"],
                products_tra_table["PROD_DESC"],
                products_tra_table["PROD_CATEGORY"],
                products_tra_table["PROD_CATEGORY_ID"],
                products_tra_table["PROD_CATEGORY_DESC"],
                products_tra_table["PROD_WEIGHT_CLASS"],
                products_tra_table["SUPPLIER_ID"],
                products_tra_table["PROD_STATUS"],
                products_tra_table["PROD_LIST_PRICE"],
                products_tra_table["PROD_MIN_PRICE"]
                ):
                
                products_dict["prod_id"].append(id)
                products_dict["prod_name"].append(name)
                products_dict["prod_desc"].append(prodD)
                products_dict["prod_category"].append(prodCate)
                products_dict["prod_category_id"].append(prodCateId)
                products_dict["prod_category_desc"].append(prodCateD)
                products_dict["prod_weight_class"].append(prodWeiC)
                products_dict["supplier_id"].append(supliId)
                products_dict["prod_status"].append(prodS)
                products_dict["prod_list_price"].append(prodLiPri)
                products_dict["prod_min_price"].append(prodMinPri)
                
        if products_dict["prod_id"]:
            df_produtcs_load = pd.DataFrame(products_dict)
            df_produtcs_load.to_sql('products',ses_db_sor,if_exists='append',index=False)
                
    except:
        traceback.print_exc()
    finally:
        pass