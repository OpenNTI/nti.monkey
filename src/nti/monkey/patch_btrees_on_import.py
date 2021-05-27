"""
Patch BTree internal sizes to larger leafs (buckets or nodes) per node as well
as larger bucket sizes. In performance testing, larger bucket sizes improved
throughput, since resolving BTree conflicts can be cheaper than when bucket
splits occur - which requires a transactional retry. We should be careful not
to make these objects too big, since that would entail larger pickling and
caching costs.

For now, we're not concerned about unbalanced BTrees due to these sizes
changing without rebuilding the BTree.

https://btrees.readthedocs.io/en/latest/overview.html?highlight=max_internal_size#btree-node-sizes
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from BTrees import family64

from BTrees.Interfaces import IBTreeFamily
from BTrees.Interfaces import IBTreeModule

logger = __import__('logging').getLogger(__name__)

def _patch():
    for name in IBTreeFamily:
        mod = getattr(family64, name)
        if not IBTreeModule.providedBy(mod):
            continue
        for kind in ('BTree', 'TreeSet'):
            kind = getattr(mod, kind)
            if kind.max_internal_size < 500:
                kind.max_internal_size = 500
            kind.max_leaf_size = kind.max_leaf_size * 4
            #print(kind, kind.max_internal_size, kind.max_leaf_size)

_patch()

def patch():
    pass
