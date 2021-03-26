from flask import Flask
from datetime import datetime
from flask import request
from flask import make_response
##from flask_restful import Api
import re
from flask.json import jsonify
from nt import abort
from werkzeug.routing import BaseConverter
from itertools import accumulate
from re import sub

app = Flask(__name__)

Colheita = [
            {
                "Numero_total_de_macas_coletadas": 0,
                "Indices_K": [],
                "Indices_L": [],
                "Qtd_por_Arvore_K": [],
                "Qtd_por_Arvore_L": []
            }    
        ]


class IntListConverter(BaseConverter):
    regex = r'\d+(?:,\d+)*,?'

    def to_python(self, value):
        return [int(x) for x in value.split(',')]

    def to_url(self, value):
        return ','.join(str(x) for x in value)

class apples():
    
    def get_max_apples(self, A, L: int, M: int) -> int:
        
        Data_struct = [
            {
                "A": []
            }    
        ]

        self.K = -1
        self.L = -1 
        Data_struct[0]['A'] = A
                                                 #():
        if ((L + M) > len(Data_struct[0]['A'])): # Levei em consideração que L e M nunca serão números negativos.
            return -1

        if (L == 0 and M == 0): # Se L e M são iguais a 0, temos 0 maçãs coletadas.
            return 0

        forward = [0]*len(Data_struct[0]['A']) #Inicialização do vetor
        
        self.L = self.search(Data_struct[0]['A'],M,forward)
        vector_index = self.get_positions_in_vector(forward, M)
        self.K = self.search_second(Data_struct[0]['A'],L,vector_index)
        vector_index1 = vector_index
        L1 = self.L
        K1 = self.K
        result1 = self.L + self.K  
        forward = [0]*len(Data_struct[0]['A']) #Inicialização do vetor
        
        self.K = self.search(Data_struct[0]['A'],L,forward)
        vector_index = self.get_positions_in_vector(forward, L)
        self.L = self.search_second(Data_struct[0]['A'],M,vector_index)
        result2 = self.L + self.K
        
        if (result1 >= result2):
            self.L = L1  # Restaura o valor das variáveis globais da classe L e K.
            self.K = K1
            Colheita[0]['Indices_L'] = vector_index1
            Colheita[0]['Indices_K'] = self.get_Marcelo_index_apples(A, L, Colheita[0]['Indices_L'])
            self.set_qtt_tree(A, Colheita[0]['Indices_L'], False)
            return result1
        else:
            Colheita[0]['Indices_K'] = vector_index
            Colheita[0]['Indices_L'] = self.get_Carla_index_apples(A, M, Colheita[0]['Indices_K'])
            self.set_qtt_tree(A, Colheita[0]['Indices_K'], True)
            return result2

    def get_positions_in_vector(self, m_forward, M: int):
        vector_index = [] #Pega as posições dentro do vetor que já foram selecionadas para a primeira soma/intervalo.
        i = 0
        j = 0
        while (i < len(m_forward)):
            if (max(m_forward) == m_forward[i]):
                while (j < M):
                    vector_index.append(i)
                    j+=1
                    i+=1
                break
            i+=1
        return vector_index

    def search(self, s_list, length, record_list): #Procura pela soma máxima de um certo subarray.
        
        if (length == 0):
            return 0
        
        left = 0
        s = sum(s_list[left:left+length])
        record_list[left] = s   # Guarda a soma de todos os subarrays dentro do array => na posição inicial de cada subarray refletido no vetor record_list.
        m = s
        while(left+length<len(s_list)):
            m = max(m,s-s_list[left]+s_list[left+length])
            record_list[left+1] = s-s_list[left]+s_list[left+length]
            s += -s_list[left]+s_list[left+length]
            left+=1

        while(left<len(s_list)-1):
            record_list[left+1] = record_list[left]
            left+=1

        return m

    def search_second(self, s_list, length, record_index_list): #Procura pela soma máxima de um certo subarray.
        left = 0
        s = sum(s_list[left:left+length])
        m = 0
        count = 0

        while(left<length):
            if (left not in record_index_list):
                count+=1
            left+=1
        
        if (count == length):
            m = max(m,s)

        left = 0
        while(left+length<len(s_list)): ##Computa soma do segundo intervalo, com o critério de não sobrepor o primeiro intervalo já computado.
            if (self.check_consecutive_positions(length, record_index_list, left+length) == True):
                m = max(m,s-s_list[left]+s_list[left+length])
            s += -s_list[left]+s_list[left+length]
            left+=1

        return m

    def check_consecutive_positions(self, m_length, m_record_index_list, m_left):
        count=0
        length = m_length
        while (m_length != 0):
            if ((m_left-m_length+1) not in m_record_index_list):  #Verifica as posições anteriores do vetor
                count+=1
            m_length = m_length - 1
        
        m_length = length
        if (count == length):
            return True
        return False

    def get_Carla_index_apples(self, A, N_consec: int, vector):
        i = 0
        j = 0
        length = N_consec
        m_vector = []

        while(i+length-1<len(A)):
            sub_A = A[i:i+length]
            if sum(sub_A) == self.L:
                j = i
                while (j <= i+length-1):
                    if j not in vector:
                        m_vector.append(j)
                        Colheita[0]['Qtd_por_Arvore_L'].append(A[j])
                    else:
                        #m_vector.clear()
                        break
                    j+=1
                if (j > i+length-1):
                    break    
            i+=1
        return m_vector

    def get_Marcelo_index_apples(self, A, N_consec: int, vector):
        i = 0
        j = 0
        length = N_consec
        m_vector = []

        while(i+length-1<len(A)):
            sub_A = A[i:i+length]
            if sum(sub_A) == self.K:
                j = i
                while (j <= i+length-1):
                    if j not in vector:
                        m_vector.append(j)
                        Colheita[0]['Qtd_por_Arvore_K'].append(A[j])
                    else:
                        #m_vector.clear()
                        break
                    j+=1
                if (j > i+length-1):
                    break
            i+=1
        return m_vector

    def set_qtt_tree(self, A, m_vector, id):
        i = 0
        while(i<len(m_vector)):
            if (id == True): #Marcelo
                Colheita[0]['Qtd_por_Arvore_K'].append(A[m_vector[i]])
            else: #Carla
                Colheita[0]['Qtd_por_Arvore_L'].append(A[m_vector[i]])
            i+=1

    

app.url_map.converters['int_list'] = IntListConverter

@app.route("/")
def home():
    return "Hello, Flask!"

#@app.route('/hello/api/v1.0/tasks/GET', methods=['GET'])
#def get_data_struct():
#    return jsonify({'Data_struct': Data_struct})


@app.route('/hello/api/v1.0/tasks/<int:m_K>/<int:m_L>/<int_list:values>', methods=['GET'])
def update_task(m_K, m_L, values):
    
    Colheita[0]['Qtd_por_Arvore_K'] = [] ##Inicializar os vetores para suportar várias requisições seguidas.
    Colheita[0]['Qtd_por_Arvore_L'] = []
    Colheita[0]['Indices_L'] = []
    Colheita[0]['Indices_K'] = []

    obj = apples()
    Colheita[0]['Numero_total_de_macas_coletadas'] = obj.get_max_apples(values, m_K, m_L)

    return jsonify({'Colheita': Colheita})

    if __name__ == '__main__':
        app.run(debug=True)