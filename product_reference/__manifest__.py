{
    'name': 'Product Reference',
    'version': '12.0.1.0.0',
    'author': 'DEC, Yann Papouin',
    'website': 'http://www.dec-industrie.com',
    'summary': '''Product reference management''',
    'depends': [
        'base',
        'mrp',
        'dec',
        'product_state',
    ],
    #'force_migration':'12.0.0.0.0',
    'data':
        [
            # 'views/reference_wizard.xml',
            'security/model_security.xml',
            'security/ir.model.access.csv',
            'views/ref_attribute.xml',
            'views/ref_property.xml',
            'views/ref_reference.xml',
            'views/ref_reference_line.xml',
            'views/ref_category.xml',
            'views/ref_category_line.xml',
            'views/ref_version.xml',
            'views/ref_log.xml',
            'views/ref_price.xml',
            'views/ref_pack.xml',
            'views/menu.xml',
        ],
    'installable': True
}
