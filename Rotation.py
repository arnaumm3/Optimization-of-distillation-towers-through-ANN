import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.interpolate import griddata

def HeatMap_nrm(Data,var1,var2,var3,nrm_mean,nrm_std):
  ''' Convert from pandas dataframes to numpy arrays '''
  ''' Data: pandas DataFrame '''
  ''' var1,var2: columns from the DataFrame that want to be plot '''
  dt = Data
  X, Y, Z, = np.array([]), np.array([]), np.array([])
  for i in range(len(dt.iloc[:,0])):
          X = np.append(X, dt.iloc[i,var1] * nrm_std[var1] + nrm_mean[var1])
          Y = np.append(Y, dt.iloc[i,var2] * nrm_std[var2] + nrm_mean[var2])
          Z = np.append(Z, dt.iloc[i,var3] * nrm_std[var3] + nrm_mean[var3])

  # create x-y points to be used in heatmap
  xi = np.linspace(X.min(), X.max(), int(len(dt.iloc[:,0])**0.5))
  yi = np.linspace(Y.min(), Y.max(), int(len(dt.iloc[:,0])**0.5))

  # Interpolate for plotting
  zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')

  # I control the range of my colorbar by removing data 
  # outside of my range of interest
  zmin = dt.iloc[:,var3].min()* nrm_std[var3] + nrm_mean[var3]
  zmax = dt.iloc[:,var3].max()* nrm_std[var3] + nrm_mean[var3]
  zi[(zi<zmin) | (zi>zmax)] = None

  # Create the contour plot
  CS = plt.contourf(xi, yi, zi, 30, cmap=plt.cm.rainbow,
                    vmax=zmax, vmin=zmin)
  CS.cmap.set_over('red')
  CS.cmap.set_under('blue')
  CS.changed()
  plt.colorbar()
  """
  names = list(dt)
  CS.set_xlabel(names[var1], fontsize=14)
  CS.set_ylabel(names[var2], fontsize=14)
  CS.set_title('Heat Map 2D normalized', fontsize=20)
  cbar.CS.get_yaxis().labelpad = 10
  cbar.CS.set_ylabel(names[var3], fontsize=14)
  """
  return plt.show()

def HeatMap(Data,var1,var2,var3):
  ''' Convert from pandas dataframes to numpy arrays '''
  ''' Data: pandas DataFrame '''
  ''' var1,var2, var3: columns from the DataFrame that want to be plot '''
  dt = Data
  X, Y, Z, = np.array([]), np.array([]), np.array([])
  for i in range(len(dt.iloc[:,0])):
          X = np.append(X, dt.iloc[i,var1])
          Y = np.append(Y, dt.iloc[i,var2])
          Z = np.append(Z, dt.iloc[i,var3])

  # create x-y points to be used in heatmap
  xi = np.linspace(X.min(), X.max(), 1000)
  yi = np.linspace(Y.min(), Y.max(), 1000)

  # Interpolate for plotting
  zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')

  # I control the range of my colorbar by removing data 
  # outside of my range of interest
  zmin = dt.iloc[:,var3].min()
  zmax = dt.iloc[:,var3].max()
  zi[(zi<zmin) | (zi>zmax)] = None

  # Create the contour plot
  CS = plt.contourf(xi, yi, zi, 30, cmap=plt.cm.rainbow,
                    vmax=zmax, vmin=zmin)
  CS.cmap.set_over('red')
  CS.cmap.set_under('blue')
  CS.changed()
  plt.colorbar()
  """
  names = list(dt)
  CS.xlabel(names[var1], fontsize=14)
  CS.ylabel(names[var2], fontsize=14)
  CS.title('Heat Map 2D', fontsize=20)
  cbar.CS.get_yaxis().labelpad = 10
  cbar.CS.set_ylabel(names[var3], fontsize=14)
  """
  return plt.show()

def HeatMap3D(grip_model):
  ''' 3D plot coloured by a 4th variable'''
  ''' grip_model: DataFrame de 4 columnes que es vol graficar'''
  
  fig = plt.figure(figsize=[5,5])
  ax = fig.add_subplot(111, projection='3d')

  x = grip_model.iloc[:,0]
  y = grip_model.iloc[:,1]
  z = grip_model.iloc[:,2]
  c = grip_model.iloc[:,-1]

  img = ax.scatter(x, y, z, c=c, s=10, cmap=plt.get_cmap('rainbow'))     #Colors: https://matplotlib.org/stable/gallery/color/colormap_reference.html
  cbar = fig.colorbar(img,shrink=0.5, aspect=20)        #Size of the colorbar
  names = list(grip_model)
  
  ax.set_xlabel(names[0], fontsize=14)
  ax.set_ylabel(names[1], fontsize=14)
  ax.set_zlabel(names[2], fontsize=14)
  ax.set_title('Heat Map 3D', fontsize=20)
  cbar.ax.get_yaxis().labelpad = 14
  cbar.ax.set_ylabel(names[-1], fontsize=14)
  
  #return plt.show()

  #return plt.show()
  for angle in range(0, 360):
    ax.view_init(30, angle)
    plt.draw()
    plt.pause(.001)

#%% 
"Data: FILTERING (HeatMap 3D)"
"Color: Cost/kgTOP"

dt = pd.read_csv(r'D:\Documents\UPC\Quatrimestre8\Data\ini_HeatMap3D')
dt = dt.loc[:,['NT', 'RR','Distillate_Rate','Cost/kgTOP']]
HeatMap3D(dt)
