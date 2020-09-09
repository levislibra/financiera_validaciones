# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError

class FinancieraValidacionConfig(models.Model):
	_name = 'financiera.validacion.config'

	name = fields.Char()
	partner_validar_identidad_activa = fields.Boolean("Crear validacion identidad manual?", default=True)
	partner_datos_personales_dni_probability_pass = fields.Float("Probabilidad para aceptar datos personales en DNI", default=0.35)
	partner_validar_domicilio_activa = fields.Boolean("Crear validacion domicilio manual?", default=True)
	partner_validar_cbu_activa = fields.Boolean("Crear validacion cbu manual?", default=True)
	company_id = fields.Many2one('res.company', 'Empresa', required=False)
