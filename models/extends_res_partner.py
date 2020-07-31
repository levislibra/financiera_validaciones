# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	@api.multi
	def ver_partner_validar_identidad(self):
		self.ensure_one()
		view_id = self.env.ref('financiera_validaciones.financiera_partner_validacion_identidad_form', False)
		return {
			'name': 'Validacion identidad del cliente',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'res.partner',
			'res_id': self.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'new',
		}

	@api.one
	def button_validar_identidad_finalizar(self):
		if self.app_datos_personales == 'aprobado' and self.app_datos_dni_frontal == 'aprobado' \
			and self.app_datos_dni_posterior == 'aprobado' and self.app_datos_selfie == 'aprobado':
			self.state = 'validated'
			self.name = self.app_apellido + " " + self.app_nombre
	
	@api.multi
	def ver_partner_validar_domicilio(self):
		self.ensure_one()
		view_id = self.env.ref('financiera_validaciones.financiera_partner_validacion_domicilio_form', False)
		return {
			'name': 'Validar domicilio del cliente',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'res.partner',
			'res_id': self.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'new',
		}

	@api.one
	def button_validar_domicilio_finalizar(self):
		if self.app_datos_domicilio == 'aprobado':
			pass