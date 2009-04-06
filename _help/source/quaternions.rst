:mod:`mathTools.quaternions` --- Quaternion
===========================================

Initialize a quaternion
-----------------------
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: __init__

.. currentmodule:: EBSDTools.mathTools.quaternions
.. autofunction:: axisAngleToQuaternion
.. autofunction:: matrixtoQuaternion
.. autofunction:: eulerAnglesToQuaternion

Arithmatic operations
---------------------
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: __add__, __sub__, __mul__, __div__, __invert__, __abs__, conjugate, normalize, isnormalized, positive
   
Representation
--------------
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: __repr__, vector, scalar, toTuple

Slice operations
----------------
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: __getitem__, __setitem__

Comparison
----------
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: __eq__

Back-conversion
---------------
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: toAxisAngle, toMatrix, toEulerAngles

Operations with quaternions
---------------------------
.. currentmodule:: EBSDTools.mathTools.quaternions
.. autofunction:: rotate
.. autofunction:: misorientation
   
Other
-----
.. autoclass:: EBSDTools.mathTools.quaternions.quaternion
   :members: __hash__
