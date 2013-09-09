.. _chap_model:

************************************************
Probabilistic Models for Degradation of Concrete
************************************************

Designing new structures or accepting existing ones as adequately safe, is
from a probabilistic point of view, the result of a decision making process
based on some optimality criteria. This process links requirements and
expectations of a structure, load and actions, geometry and material
properties and also expectations of society. [JCSS2002]_

Such decision problems are mathematical treated with the so-called decision
theory. An important aspect of the decision theory is the assessment of
consequences and probabilities, which are depict in probabilistic
models. [Faber2009]_

.. note::
   Probabilistic Model (Benjamin and Cornell, 1970) 

   A probabilistic model remains an abstraction until it has been related to
   observations of physical phenomenon.

This requires the collection and progression of input data as well as
determination of statistical distribution, corresponding statistical
parameters and possible correlations.

For the degradation of concrete structures, several models have been developed
to provide methods to estimate the length of time during which RC structures
maintain a desired level of functionality. Service life models such as
[DuraCrete1999]_, [DuraCrete2000]_, [LIFECON2003]_, and [fib2006]_ provide
valuable information about the durability characteristics of concrete structures.
The proposed method of this work is not limited to any of those models. However,
in the remainder of this work only the [DuraCrete2000]_ model is going to be
treated. This chapter provides an overview of this probabilistic model. Hence,
there are no explicit references cited for the assumptions of the
[DuraCrete2000]_ model.


Material Properties
===================

The description of each material property consists of a mathematical model and
random variables. Functional relationships between the variables may be part
of the material model. [JCSS2002]_

Concrete
--------

.. autoclass:: core.concrete.Concrete
   :members:

Reinforcement
-------------

.. autoclass:: core.reinforcement.Reinforcement
   :members:

Environmental Actions
=====================

.. autoclass:: core.environment.Environment
   :members:

Geometric Properties
====================

.. autoclass:: core.geometrie.Geometrie
   :members:

Carbonation Induced Corrosion
=============================

.. autoclass:: core.carbonation.Carbonation
   :members:

Chloride Induced Corrosion
==========================

.. autoclass:: core.chloride.Chloride
   :members:

Propagation of Corrosion
========================

.. autoclass:: core.propagation.Propagation
   :members:

Effects of Corrosion
====================

If corrosion is initiated, the consequences are a reduction in the cross
section of the reinforcement steel, increase in bar diameter resulting from
the volumetric expansion of the corrosion products, and a change in the
mechanical properties of the reinforcement and the concrete. [Cabrera1996]_
These effects do not only involve serviceability, but may also affect its
structural reliability and therefore the safety of the
structure. Correspondingly the corrosion affects the reinforcement itself and
the surrounding concrete.

General Corrosion
-----------------

General or uniform corrosion is caused by very high levels of chlorides or
carbonation of concrete. It is typically associated with “rust” over the
entire steel surface, which occupying a greater volume than the parent
material. This can lead to cracking and spalling of the concrete cover. A loss
of bond strength, caused by reinforcement slip that is initiated by corroded
steel surfaces, and loss of reinforcement cross section may be the
consequences of general corrosion, too. [Osterminski2012]_


Pitting Corrosion
-----------------

.. autoclass:: core.corrosion.Pitting
   :members:

Modeling Structural Reliability
===============================

.. autoclass:: core.resistance.Resistance
   :members:
