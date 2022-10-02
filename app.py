from flask import Flask
from flask import render_template,request,send_file,redirect,url_for
from werkzeug.utils import secure_filename
import pandas as pd#xrld
import json
from pprint import pprint
import urllib.parse
from html2excel import ExcelParser
import os


#parser = ExcelParser("")
result_json = {}
app = Flask(__name__)

@app.route('/', methods=['POST','GET'])

def index():
    # result_json = {}
    
    if request.method == "POST":
        if request.form['submit_button'] == 'Import':
            
            f = request.files['file']
            f.save(secure_filename(f.filename))
            input_df = pd.read_excel(f)

            for index, row in input_df.iterrows():
                row_dict = {}
                row_dict['Suggestion1'] = row['Suggestion1']
                row_dict['Suggestion2'] = row['Suggestion2']
                row_dict['Suggestion3'] = row['Suggestion3']
                row_dict['Selected_model'] = row['Selected_model']
                result_json[int(index)] = row_dict
            #print(row['c1'], row['c2'])

        
        #result_json = {0:{'Suggestion1':'Poland','Suggestion2':'3456','Suggestion3':'Huawei','Selected_model':'test'},1:{'Suggestion1':'Poland','Suggestion2':'3456','Suggestion3':'Huawei','Selected_model':'test'}}
            return render_template('index.html',result_json = result_json)

        # elif request.form['submit_button'] == 'Export':
        #     output = request.get_json()
        #     result = json.loads(output)
        #     table_as_string = result['result']
        #     data_df = pd.read_html(table_as_string,skiprows=0)[0]
        #     data_df.to_excel('dash.xlsx')
        #     return send_file('dash.xlsx', as_attachment=True)

        elif request.form['submit_button'] == 'Export':
            return send_file('new.xlsx', as_attachment=True)


        else:
            return render_template('index.html',result_json = result_json)
            
            #return send_file('res.xlsx', as_attachment=True)
            #return send_file('new.xlsx', as_attachment=True)

        # if request.form['submit_button'] == 'Export':
        #     output = request.get_json()
        #     print(output) # This is the output that was stored in the JSON within the browser
        #     print(type(output))
        #     #result = json.loads(output) #this converts the json output to a python dictionary
        #     #print(result) # Printing the new dictionary
        #     #print(type(result))#this shows the json converted as a python dictionary
        #     return render_template('index.html',result_json = result_json)


        
    else:
        return render_template('index.html',result_json = result_json)


@app.route('/test', methods=['POST'])
def test():
    
    output = request.get_json()
    print(output) # This is the output that was stored in the JSON within the browser
    print(type(output))
    result = json.loads(output) #this converts the json output to a python dictionary
    table_as_string = result['result']
    #print(result['result']) # Printing the new dictionary
    #print(type(result['result']))#this shows the json converted as a python dictionary
    path = os.path.dirname(os.path.abspath(__file__))
    full_path = path + '\new.xlsx'
    data_df = pd.read_html(table_as_string,skiprows=0)[0]
    data_df.to_excel('new.xlsx')
    #return send_file('new.xlsx', as_attachment=True)
    
    return render_template('index.html',result_json = result_json)


    



if __name__ == '__main__':

	app.run()
