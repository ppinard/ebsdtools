:mod:`indexation.hough` --- Computation of the Hough Transform
===============================================================

.. note:: Requires Jython and rmlimage

Initialize
----------
.. autoclass:: EBSDTools.indexation.hough.Hough
   :members: __init__

Calculate Hough Transform
-------------------------
.. autoclass:: EBSDTools.indexation.hough.Hough
   :members: calculateHough

.. currentmodule:: EBSDTools.indexation.hough
.. autofunction:: createMaskDisc

Calculations
------------
.. autoclass:: EBSDTools.indexation.hough.Hough
   :members: findPeaks, calculateImageQuality
   
Get information
---------------
.. autoclass:: EBSDTools.indexation.hough.Hough
   :members: getHoughMap, getPeaks, getPeaksCount, getPeakIntensity, getPeakCentroid, getPeakArea, getImageQuality
