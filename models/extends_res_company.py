# -*- coding: utf-8 -*-

from openerp import models, fields, api


class ExtendsResCompany(models.Model):
	_name = 'res.company'
	_inherit = 'res.company'

	validaciones_config_id = fields.Many2one('financiera.validacion.config', 'Configuracion validaciones')
