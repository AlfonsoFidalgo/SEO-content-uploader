import pandas as pd
import numpy as np
import requests

def get_path(make_model):
    make_model = make_model.replace(' ', '%20')
    url = 'https://api.hey.car/search/count?q=' + make_model
    res = requests.get(url)
    try:
        make = res.json()['searchFilter']['make']
        model = res.json()['searchFilter']['model']
        return 'make=' + make + '&model=' + model
    except:
        print(make_model.replace('%20', ' '), '--> make or model not found')
        return 'PATH NOT FOUND'


if __name__ == "__main__":
    df = pd.read_excel('heycar content tabelle.xlsx')
    ready = df[df['Text ready to deploy'].notnull()]
    ready = ready[ready['live'].isna()]
    all_rows = []
    for i in list(ready.index):
        content = ready.loc[i]['Text ready to deploy']        
        #SEO Tool columns
        try:
            lines = [line.strip() for line in content.splitlines() if len(line) > 0]
            
            title = lines[0].split(':')[1].strip()
            description = lines[1].split(':')[1].strip()
            keywords = '${makeName} ${modelName} Gebrauchtwagen, heycar, Gebrauchtwagen kaufen'
            H1 = '# Wir haben ~~${resultCount}~~<br/>${makeName} ${modelName} für dich gefunden.'
            locale = 'de'
            page_type = 'CLP'
            path = get_path(ready.loc[i]['Automodell + "gebraucht"'])
            H2 = lines[2]
            H3 = lines[3]
            seo_content = ''
            for cont in lines[4:]:
                seo_content += cont
            
            row = [title, description, keywords, H1, locale, page_type, path, H2, H3, seo_content]
            all_rows.append(row)
        except:
            print('something wrong with the content. Might not be in the right format')
    df2 = pd.DataFrame(np.array(all_rows), 
    columns= ['Title', 'Description', 'Keywords', 'H1', 'Locale', 'Page type', 'Path', 'H2', 'H3', 'Content'])

    df2[df2['Path'] != 'PATH NOT FOUND'].to_csv('upload_this.csv')
    df2.to_excel('open_this_to_check.xlsx')

        

