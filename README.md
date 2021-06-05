# End of degree project. 

## Abstract
End of degree project. Study of surrogate models, in particular ANN's, for the simulation and optimization of distillation trains.
The computational time required to solve optimization problems in rigorous simulation programs is usually unaffordable, raising the usage of surrogate models.
The development of these approximate models is a challenge that needs to handle computational burden and the risk of over fitting.
In the present work, tools and procedures to build, train, and validate an Artificial Neural Network (ANN) are developed to make the use of surrogate models more
common and straightforward. The proposed tools are tested with a case study addressing the synthesis of separation trains for the products of polyethylene pyrolysis,
focusing in the distillation columns of the process simulated with Aspen HYSYS. Implementing circular economy principles in process synthesis requires the modelling
of valorisation processes upcycling waste from different sources. Hence, two ANN models have been developed to simulate and optimize the behaviour of the column regarding
an objective function in tune with this implementation. Both models fit correctly and show good accuracies with respect the surface studied. Different comparisons of the
models are made, scarcely showing no differences between them.

## GitHub files

### Datasets:
  - "A-BCD_Model15.xlsx": result of the sampling from the "Hysys_Python_Interface.py" script. All the variables required to calculate the objective function are present.
      NT	RR	Distillate_Rate	Column_Diameter	Column_Spacing	TOP_Flow_A	TOP_Flow_B	TOP_Flow_C	TOP_Flow_D	BOTTOM_Flow_A	BOTTOM_Flow_B	BOTTOM_Flow_C	BOTTOM_Flow_D	T_Condenser	T_Reboiler	Duty_Condenser	Duty_Reboiler	Area_Condenser	Area_Reboiler
  
  - "iniHeatMap3D": initial set of data that contains the following information of the 10000 samples
      NT,RR,Distillate_Rate,TOP_Fraction_A,Recovery,Cost/kgTOP
  
  - "Filter": evolution of the iniHeatMap3D, where the 10.000 samples have been filtered by TOP_Fraction_A & Recovery, leading to this 6355 samples.
      NT,RR,Distillate_Rate,TOP_Fraction_A,Recovery,Cost/kgTOP
  
  - The pretreatment of the data leads to the training and testing set that will be fed in the ANN.
    * "x_train", "y_train": used to train and validate the model.
    * "x_test", "y_test": used to check the accuracy of the model.


### Scripts
  - "Hysys_Python_Interface.py": connection Aspen HYSYS - Python which enables the sampling of the "A-BCD_Model15.xlsx" dataset. This connection requires a second script to run the
    simulation when a sample is written in HYSYS ("RunColumnPython.SCP").
    
  - "ANN_A-BCD_opt2.py": from the "A-BCD_Model15.xlsx" dataset this script pretreats the data, creates the optimization model and plots the results (applies the filtering).
  
  - "ANN_A-BCD_sim.py":  from the "A-BCD_Model15.xlsx" dataset this script pretreats the data, creates the simulation   model and plots the results (does not apply the filtering).
  
  - "Rotation": 
  
  - "Rotation1":
