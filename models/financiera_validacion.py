# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError

class FinancieraValidacion(models.Model):
	_name = 'financiera.validacion'

	_order = 'priority asc,id desc'
	name = fields.Char()
	priority = fields.Selection([(1, "Alta"), (2, "Media"), (3, "Baja")], 'Prioridad', default=3)
	asigned_id = fields.Many2one('res.users', 'Asignar a')
	active = fields.Boolean("Activo", default=True)
	validation_type = fields.Selection([
		('partner_validar_identidad', 'Validar identidad del cliente'),
		('partner_validar_domicilio', 'Validar domicilio del cliente'),
		('partner_validar_cbu', 'Validar CBU del cliente')
	], 'Tipo de validacion')
	state = fields.Selection([
		('pendiente', 'Pendiente'),
		('en_proceso', 'En proceso'),
		('finalizada', 'Finalizada')
	], 'Estado', default='pendiente')
	# Objeto por validar
	partner_id = fields.Many2one('res.partner', 'Cliente')
	company_id = fields.Many2one('res.company', 'Empresa')

	@api.model
	def create(self, fields):
		rec = super(FinancieraValidacion, self).create(fields)
		rec.update({
			'name': 'VAL ' + str(rec.id).zfill(8),
		})
		return rec

	@api.one
	def button_procesar(self):
		if self.state == 'pendiente':
			self.state = 'en_proceso'
			self.asigned_id = self.env.user.id
		else:
			raise UserError('La validacion no esta disponible.')

	@api.one
	def button_finalizar(self):
		if self.state == 'en_proceso':
			self.state = 'finalizada'
			self.active = False
		else:
			raise UserError('Para finalizar la validacion, la misma debe estar en proceso.')

	# Validar identidad del cliente
	@api.multi
	def ver_partner_validar_identidad(self):
		return self.partner_id.ver_partner_validar_identidad()
	
	# Validar domicilio del cliente
	@api.multi
	def ver_partner_validar_domicilio(self):
		return self.partner_id.ver_partner_validar_domicilio()