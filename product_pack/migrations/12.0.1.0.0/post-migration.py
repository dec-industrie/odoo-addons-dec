from openupgradelib import openupgrade

columns = [
    'stock_depends',
    'fixed_sale_price',
    'fixed_purchase_price',
]

@openupgrade.migrate()
def migrate(env, version):
    legacy_mapping = [(x, openupgrade.get_legacy_name(x)) for x in columns]

    mapping_str = []
    for item in legacy_mapping:
        mapping_str.append('{0}=pp.{1}'.format(
            item[0], item[1]
        ))

    openupgrade.logged_query(
        env.cr, """
        UPDATE product_template pt SET
            {0}
        FROM product_product pp
        WHERE pt.id = pp.id
        """.format(','.join(mapping_str))
    )