from waflib.TaskGen import feature
import orch.features

# from https://github.com/brettviren/python-ups-utils
try:
    import ups.commands 
except ImportError:
    print 'Failed to import, do you need to install: https://github.com/brettviren/python-ups-utils'
    raise

def configure(cfg):
    orch.features.register_defaults(
        'upsinit',
        ups_products_dir = '',
        ups_version = '5.2.1',
    )
    orch.features.register_defaults(
        'upstable',
        ups_products_dir = '',
        ups_product_subdir = '{package}/{version}', # maybe {package}/v{version_underscore} for some
        ups_subdir = 'ups',                 # take relative to ups_product_subdir
        ups_table_file = '{package}.table', # taken relative to ups_subdir
        ups_qualifiers = '',
    )

    return


# tool interface
def build(bld):
    pass


@feature('upsinit')
def feature_upsinit(tgen):
    '''
    Initialize a UPS products area including installing a UPS package.
    '''
    products_dir = tgen.make_node(tgen.worch.ups_products_dir)
    setups_file = products_dir.make_node('setups')

    def upsinit(task):
        ups.commands.install(tgen.worch.ups_version, products_dir.abspath())

    tgen.step('upsinit', 
              rule = upsinit, 
              update_outputs = True,
              target = setups_file)

    pass

# /bin/bash -c 'source `pwd`/setups && ups declare hello v2_8 -f "Linux64bit+3.13-2.19" -r hello/v2_8 -m hello.table -M Linux64bit+3.13-2.19/ups'
# 

@feature('upstable')
def feature_upstable(tgen):
    '''
    '''
    w = tgen.worch
    print sorted(w._config.keys())

    assert w.ups_products_dir
    assert w.ups_product_subdir

    repo = tgen.make_node(w.ups_products_dir)
    pdir = repo.make_node(w.ups_product_subdir)
    udir = pdir.make_node(w.ups_subdir)
    table_node = udir.make_node(w.ups_table_file)

    def wash_path(path, fromnode, noparent = True):
        'Turn absolute paths into ones relative to fromnode'
        if not path.startswith('/'):
            return 
        pnode = tgen.make_node(path)
        rel = pnode.path_from(fromnode)
        if rel.startswith('..') and noparent:
            return 
        return rel

    def upstable(task):
        preamble = w.format('''\
File    = table
Product = {package}
Group:
  Flavor = {ups_flavor}
  Qualifiers = "{ups_qualifiers}"
  Action = FlavorQualSetup
''')
        postamble = w.format('''
Common:
  Action = setup
    setupenv()
    proddir()
    exeActionRequired(FlavorQualSetup)
End:\n''')

        meat = []

        for mystep, deppkg, deppkgstep in w.dependencies():
            o = w.others[deppkg]
            depquals = ''
            if o.ups_qualifiers:
                depquals = ' -q ' + o.ups_qualifers
            s = w.format('setupRequired( {deppkg} {depver} {depquals} )',
                         deppkg=deppkg, depver='v'+o.version_underscore, depquals=depquals)
            meat.append(s)

        for var, val, oper in tgen.worch.exports():
            relval = wash_path(val, pdir)
            if relval:
                val = '${UPS_PROD_DIR}/' + relval
            if oper == 'set':
                meat.append('envSet(%s,%s)' % (var, val))
            if oper == 'prepend':
                meat.append('pathPrepend(%s,%s)' % (var, val))
            if oper == 'append':
                meat.append('pathAppend(%s,%s)' % (var, val))
        

        meats = '\n'.join(['    %s' % x for x in meat])

        tf = task.outputs[0]
        tf.write(preamble + meats + postamble)

    

    tgen.step('upstable',
              rule = upstable,
              update_outputs = True,
              target = table_node)
