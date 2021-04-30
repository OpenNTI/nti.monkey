"""
A temporary patch to fix the class hierarchy of pickled StripePurchaseError
objects. Without this, these objects cannot be unpickled because
BaseException.__new__ is not called.

Once these objects are unpickled and re-pickled correctly, this can be removed.
"""

def do_patch():
    import copy_reg
    from nti.store.payments.stripe.model import StripePurchaseError
    orig_recon = copy_reg._reconstructor
    def _reconstructor(cls, base, state):
        if cls is StripePurchaseError and base is object:
            base = cls
        return orig_recon(cls, base, state)
    copy_reg._reconstructor = _reconstructor


def patch():
    try:
        do_patch()
    except ImportError:
        pass

