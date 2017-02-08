# -*- encoding: UTF-8 -*-
#    type of the change:  Creacion
#    Comments: Creacion del modulo de IDEA
   
{

    'name': 'IDEA',
    'description': '''\

Registrar las ideas y opiniones \n
Calificar una idea. \n
Votaciones con una duracion fija de tiempo\n
Tener estadisticas de las ideas y sus votos\n
Poder agrupar personas con intereses similares.\n

''',
    'author': 'itbetter@gmail.com',
    'category': 'encuentas',
    'data': [
        'views/main_menu.xml',
        'views/idea_view.xml',
        'views/group_view.xml',
        'views/votes_view.xml',
        'views/ir_cron.xml',

        ],

    'depends': ['base'],
    'installable': True,
}