# -*- encoding: UTF-8 -*-
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
import datetime


class idea(models.Model):

    _name = 'idea.base'
    _description = 'registrar las idea de los usuarios.'

    @api.model
    def idea_close(self):
        search_tto_cloase  = self.search([('date_to', '=', datetime.date.today())])
        search_tto_cloase.write({'state':'closed'})


    @api.multi
    @api.depends('name', 'average')
    def name_get(self):
        result = []
        for idea in self:
            name = (idea.name and (str(idea.average) + '-') or '') + idea.name
            result.append((idea.id, name))
        return result


    @api.depends('vote_ids.score')
    def _average(self):
        for idea in self:
            if self.vote_ids:
                idea.average = sum([int(vote_id.score) for vote_id in self.vote_ids])/ len(self.vote_ids.ids)

    @api.multi
    def active_idea(self):

        return self.write({'state': 'open'})



    @api.onchange('date_from')
    def _onchange_date_from(self):
        if self.date_from:
            self.date_to = datetime.datetime.strptime(self.date_from, DEFAULT_SERVER_DATE_FORMAT)  + relativedelta(months=1)



    @api.multi
    def rate(self):
        for idea in self:
            if self.env.uid not in [i.create_uid.id for i in idea.vote_ids] and self.env.uid != idea.create_uid.id:
                idea.write({'vote_ids': [(0, 0, {'score': idea.score})], 'score': False})
            # idea.write({'vote_ids': [(0, 0, {'score': int(idea.score)})], 'score': False})

    state = fields.Selection([('draft', 'Borrador'), ('open', 'Abierto'), ('closed', 'Cerrado')], 'Status', required=True,
                             copy=False, default='draft',)

    name = fields.Char('nombre', readonly=True, states={'draft': [('readonly', False)]})
    group= fields.Many2one('idea.group', readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Text('Descripcion', readonly=True, states={'draft': [('readonly', False)]})
    vote_ids = fields.One2many('idea.score','idea_id','Voto', readonly=True, states={'draft': [('invisible', True)]})
    score = fields.Selection(string='Calificacíon', selection=lambda self: [(i, i) for i in range(0, 11)], readonly=True, states={'open': [('readonly', False)]})
    average = fields.Integer('Calificacíon', help='promedio de esos votos', compute='_average', readonly=True)
    date_from = fields.Date(string='From', required=True, default=lambda self: datetime.date.today(), readonly=True, states={'draft': [('readonly', False)]})
    date_to = fields.Date(string='End Date', readonly=True, states={'draft': [('readonly', False)]})

    
    
class vote(models.Model):
    """"
    usuario = create_uid
    la fecha = create_date
    modificado = write_uid + write_date

    """

    _name = 'idea.score'
    _description = 'calificar una idea.'

    idea_id = fields.Many2one('idea.base')
    score = fields.Integer(string='Calificacíon')


class groups(models.Model):

    _name = 'idea.group'
    _description = 'grupo representativo'


    @api.multi
    def add_to_group(self):
        return self.write({'user_ids': [(6, 0, [self.env.user.id])]})

    @api.multi
    def del_to_group(self):
        return self.write({'user_ids': [(5, self.env.user.id)]})

    name = fields.Char('nombre')
    description = fields.Text('Descripcion')
    user_ids = fields.Many2many('res.users', readonly=True)