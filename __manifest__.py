{
    'name': 'Real Estate',
    'description': 'Estate',
    'depends': ['base','web','portal','mail'],
    'author': 'Neeraj M',
    'category': 'Bussiness',
    'data': [
        'security/groups.xml',
        'security/sequence_security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/estate_menus.xml',
        'views/estate_rent_payment_view.xml',
        'views/estate_property_offer.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type.xml',
        'views/estate_property_tags.xml',
        'views/users_view.xml',
        'views/estate_rent_form.xml',
        'views/payment_receit.xml',
        'views/payments_history.xml',
        'views/form_template.xml',
        'views/email_template.xml',
        'views/agent_view.xml',
    ],
    'assets':{
        'web.assets_backend':[
            'Real_Estate/static/src/rent_form_conditions.js',
            'Real_Estate/static/src/css/kanban_styles.scss'
        ],
    },
}
