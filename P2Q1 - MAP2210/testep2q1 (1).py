# -*- coding: utf-8 -*-
"""testep2q1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nt1VRwnzPcoSJPTyI2i6JB-rWRjb0HVf
"""

#importa bibliotecas necessárias
import numpy as np
from numpy.linalg import solve
import time
import math
from numpy import inf

"""#Implementação Final

$$u(x) = e^{cosx}$$
$$f(x) = (cosx - sen^{2}x)e^{cosx}$$

Contorno de Dirichlet: $u(0) = u(2\pi) = e$
"""

#importa métodos da esparsa do scipy
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

#define u(x) e f(x):
def u(x):
  return (math.e)**math.cos(x)

def f(x):
  return (math.cos(x) - (math.sin(x))**2)*((math.e)**(math.cos(x)))

#função que aproxima a função
def a(n):

  #calcula h
  h = (2*math.pi - 0)/n
  #cria a matriz A esparsa
  A = lil_matrix((n-1,n-1))
  #valores das diagonais
  diag_1 = [0] + [-1]*(n-4)
  lil_matrix.setdiag(A,values = np.array(diag_1), k = 2)

  diag_2 = [1] + [16]*(n-3)
  lil_matrix.setdiag(A,values = np.array(diag_2), k = 1)

  diag_3 = [-2] + [-30]*(n-3) + [-2]
  lil_matrix.setdiag(A,values = np.array(diag_3), k = 0)

  diag_4 = [16]*(n-3) + [1]
  lil_matrix.setdiag(A,values = np.array(diag_4), k = -1)

  diag_5 = [-1]*(n-4) + [0]
  lil_matrix.setdiag(A,values = np.array(diag_5), k = -2)
  #transforma A na forma csr
  A = A.tocsr()

  #incializa  e preenche lado direito
  B = [0]*(n-1)

  for i in range(1,n):

      if i == 1: B[i-1] = -f(h*i)*(h**2) - u(0)
      if i == 2: B[i-1] = -f(h*i)*12*(h**2) + u(0)
      if i == n-2: B[i-1] =  B[i-1] = -f(h*i)*12*(h**2) + u(2*math.pi)
      if i == n-1: B[i-1] = -f(h*i)*(h**2) - u(2*math.pi)
      if i != n-1 and i != 1 and i != n-2 and i != 2: B[i-1] = -f(h*i)*12*(h**2)
  #transforma em array
  B = np.array(B)
  #resolve sistema
  x = spsolve(A,B)

  return x

#solução exata para esses pts
def U(n):
  lista = []
  #calcula h
  h = (2*math.pi - 0)/n

  for i in range(1,n):
    lista.append(u(h*i))
  vetor = np.array(lista)

  return vetor

#vetor de erros
def E(n):
  erros = []
  #calcula h
  h = (2*math.pi - 0)/n
  #apppenda a dif em cada coordenada
  for i in range(1,n):
    erros.append(U(n)[i-1] - a(n)[i-1])
  #transforma em array
  erros = np.array(erros)

  return erros

#lista dos n's para atabela
lista_ns = [128,256,512,1024,2048,4096]
#listas q armazenam as normas
norma_max = []
norma_2 = []

for k in range(len(lista_ns)):
  #appenda normas
  norma_max.append(np.linalg.norm(np.array(E(lista_ns[k])),inf))
  norma_2.append(np.linalg.norm(E(lista_ns[k])))
  
  if k > 0: print('p = ', math.log2(norma_2[k-1]/norma_2[k])) 
  print()
  if k > 0: print('p = ', math.log2(norma_max[k-1]/norma_max[k]))