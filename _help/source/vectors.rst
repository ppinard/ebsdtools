:mod:`mathTools.vectors` --- Vector class
=========================================

Initialize a vector
-------------------------------------------------
.. autoclass:: EBSDTools.mathTools.vectors.vector
   :members: __init__

Arthimetic operations
---------------------
.. autoclass:: EBSDTools.mathTools.vectors.vector
   :members: __add__, __sub__, __mul__, __div__, __neg__

Comparison
----------
.. autoclass:: EBSDTools.mathTools.vectors.vector
   :members: __lt__, __le__, __gt__, __ge__, __eq__, __ne__

Elemental
---------
.. autoclass:: EBSDTools.mathTools.vectors.vector
   :members: __getslice__, __getitem__, __setitem__, __delitem__

Other
-----
.. autoclass:: EBSDTools.mathTools.vectors.vector
   :members: __repr__, __len__


Multiple vectors operations
---------------------------
.. currentmodule:: EBSDTools.mathTools.vectors
.. autofunction:: dot
.. autofunction:: cross
.. autofunction:: tripleProduct
.. autofunction:: angle
.. autofunction:: directionCosine
