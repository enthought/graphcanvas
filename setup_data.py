
# Function to convert simple ETS project names and versions to a requirements
# spec that works for both development builds and stable builds.  Allows
# a caller to specify a max version, which is intended to work along with
# Enthought's standard versioning scheme -- see the following write up:
#    https://svn.enthought.com/enthought/wiki/EnthoughtVersionNumbers
def etsdep(p, min, max=None, literal=False):
    require = '%s >=%s.dev' % (p, min)
    if max is not None:
        if literal is False:
            require = '%s, <%s.a' % (require, max)
        else:
            require = '%s, <%s' % (require, max)
    return require


# Declare our ETS project dependencies.
ENABLE_TRAITS = etsdep('Enable[traits]', '3.1.1')
ENTHOUGHTBASE = etsdep('EnthoughtBase', '3.0.3')
TRAITSBACKENDWX = etsdep('TraitsBackendWX', '3.1.1')
TRAITS_UI = etsdep('Traits[ui]', '3.1.1')


INFO = {
    "extras_require": {
        'wx': [
            TRAITSBACKENDWX,
            ],

        # All non-ets dependencies should be in this extra to ensure users can
        # decide whether to require them or not.
        'nonets': [
            'numpy >= 1.1.0',
            'networkx >= 1.0.1',
            #'PyQt4', -- not really required by everyone.
            #'wxPython', -- not really required by everyone.
            ],
        },
    "install_requires": [
        ENABLE_TRAITS,
        ENTHOUGHTBASE,
        TRAITS_UI,
        ],
    "name": 'GraphCanvas',
    "version": '0.1.1',
    }

