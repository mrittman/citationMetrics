=========
Citation Metrics
=========

Overview
=========

This a project to simulate citations and analyse the properties of metrics applied to them. It also includes quite a lot of output data (at least in the initial version).

All the code is written in Python 2.7.

Structure
=========

There are three code sets:

``citationSimulator`` - contains the class ``dataSimulator`` to simulate code from a number of distributions, then calculate various metrics deriving from the code. The distributions avaiable are stochastic normal, log normal, pareto and uniform. Data from stochastic simulations (see below) can also be included.

``metricCalulator`` - encodes various citation metrics. Two ways of calculating are possible: from a list of how many citations each paper receives, or from a list of individual citations (which include the cited date and cited paper).

``stochasticSimulator`` - simulates citation data using the stochastic model in "Uncovering the dynamics of citations of scientific papers" by Michael Golosovsky and Sorin Solomon.

In the bin folder is a folder ``analysisTools`` which contains some scripts to analyse statistical aspects of the merics in ``analysis_0.3``. 

Current progress
=========

All the code is there, but it's currently quite jumbled, so I will be working on making more sense of it, annontating, etc. 

There is a related open science framework project at https://osf.io/wav8q/.

Any questions can be sent to mrittman@phyiscs.org.
