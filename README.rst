********************
Concrete Reliability
********************

:Date: September 2013
:Authors: Jürgen Hackl
:Contact: hackl.j@gmx.at
:Web site: http://github.com/hackl/core
:Documentation: http://hackl.github.io/core/
:Copyright: This document has been placed in the public domain.
:License: CoRe is released under the GNU General Public Licence.
:Version: 1.0.1



Note
----

   If you have any problems, found bugs in the code or have feature request
   comments or questions, please feel free to send a mail to `Jürgen Hackl`_.


.. _`Jürgen Hackl`: hackl.j@gmx.at


Purpose
=======

CoRe (Concrete Reliability) is meant to provide a generic framework for
stochastic modeling of reinforced concrete deterioration caused by
corrosion. Thereby, the combination of structural reliability analysis and
Bayesian networks provides a powerful tool for a computationally efficient and
robust method, computing probabilities of rare events in complex structures,
and also allows Bayesian updating of the model with measurements, monitoring
and inspection results.

.. note::

   The `CoRe`_ modul needs also the `PyRe`_ and the `PyBN`_ modul to work!

.. _`CoRe`: http://github.com/hackl/core

.. _`PyRe`: http://github.com/hackl/pyre

.. _`PyBN`: http://github.com/hackl/pybn


Abstract
========

Reinforced concrete structures constitute an important fraction of the
building infrastructure. This infrastructure is aging and a large number of
structures will exceed the prescribed service period in the next decades. The
aging of concrete structures is often accompanied by correspondent
deterioration mechanisms. One of the major deterioration mechanisms is the
corrosion of the reinforcing steel, caused by chloride ions or carbon dioxide
exposure.

The decisions, made in connection to possible repair or renewals of these
structures, have major implications on safety and cost efficiency in a
societal dimension. Public authorities, entitled to administrate the
infrastructure, are in need of schemes and methodologies that facilitate the
optimal management of the already existing stock of structures, especially in
regard to repair and maintenance planning.

In this work a generic framework for a stochastic modeling of reinforced
concrete deterioration caused by corrosion is presented. This framework
couples existing probabilistic models for chloride and carbonation initiation
with models for the propagation and the effects of corrosion. For this
purpose, a combination of structural reliability analysis and Bayesian
networks is used for the reliability assessment of the reinforced concrete
structure. This approach allows to compute probabilities of rare events for
complex structures in an efficient way to update the model with new
information from measurements, monitoring and inspection results.

This framework enables, for the first time, a holistic view of the current
service life models, with corresponding sensitivity studies and finding
optimal decisions for treating deteriorated reinforced concrete
structures. The temporal evolvement of structures can also be represented and
analyzed within this framework.

.. note::

   Keywords: Bayesian networks, corrosion, degradation, probabilistic
   modeling, probability, reinforced concrete, structural reliability
   analysis;


Literature
==========

CoRe is based on the Master's thesis:

   Hackl Jürgen: "Generic Framework for Stochastic Modeling of Reinforced
   Concrete Deterioration Caused by Corrosion". Master’s thesis, Norwegian
   University of Science and Technology, Trondheim, Norway, 2013.


Getting started
===============

This guide provides all the information needed to install CoRe, code a
probabilistic model, run the sampler, save and visualize the results.
