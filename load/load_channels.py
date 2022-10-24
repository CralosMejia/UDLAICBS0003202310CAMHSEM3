from util.db_connection import connect
from util.properties import getProperty

import traceback
import pandas as pd


def load_channels(ID):
    try:
        

        
        name_DB_stg = getProperty("DBSTG")
        name_DB_sor = getProperty("DBSOR")
        
        
        ses_db_stg = connect(name_DB_stg);
        ses_db_sor = connect(name_DB_sor);
        
        
        #Dictionary for values of chanels
        cha_dict = {
            "CHANNEL_ID":[],
            "CHANNEL_DESC":[],
            "CHANNEL_CLASS":[],
            "CHANNEL_CLASS_ID":[],
            "PROCESS_ID":[]
        }
        
        #Reading the ext table
        channel_tra_table = pd.read_sql(f"SELECT CHANNEL_ID,CHANNEL_DESC,CHANNEL_CLASS,CHANNEL_CLASS_ID FROM channels_tra WHERE PROCESS_ID = {ID}", ses_db_stg)
        
        if not channel_tra_table.empty:
            for id,desc,cla,cla_id in zip(
                channel_tra_table["CHANNEL_ID"],
                channel_tra_table["CHANNEL_DESC"],
                channel_tra_table["CHANNEL_CLASS"],
                channel_tra_table["CHANNEL_CLASS_ID"]
                ):
                
                cha_dict["CHANNEL_ID"].append(id)
                cha_dict["CHANNEL_DESC"].append(desc)
                cha_dict["CHANNEL_CLASS"].append(cla)
                cha_dict["CHANNEL_CLASS_ID"].append(cla_id)
                cha_dict["PROCESS_ID"].append(ID)
                
                
        if cha_dict["CHANNEL_ID"]:

            table_sor = pd.read_sql("SELECT CHANNEL_ID,CHANNEL_DESC,CHANNEL_CLASS,CHANNEL_CLASS_ID FROM channels", ses_db_sor)
            table_tra = pd.DataFrame(cha_dict)
            print(table_tra)
            print(table_sor)
            if table_sor.empty:
                table_tra.to_sql('channels', ses_db_sor, if_exists='append', index=False)
            else:
                df_channels = pd.concat([table_sor, table_tra]).groupby(["CHANNEL_ID"], as_index=False).last()
                print(df_channels)
                df_channels.to_sql('channels', ses_db_sor, if_exists='replace', index=False)


    except:
        traceback.print_exc()
    finally:
        pass