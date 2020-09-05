# -*- coding: utf-8 -*-

from openerp import models, fields, api

class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	app_datos_dni_selfie_validacion = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado')
	], "Datos de DNI y selfie")

	@api.multi
	def ver_partner_validar_identidad(self):
		self.ensure_one()
		self.app_datos_dni_selfie_validacion = False
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

	@api.onchange('app_datos_dni_selfie_validacion')
	def _onchange_datos_dni_selfie(self):
		if self.app_datos_dni_selfie_validacion == 'aprobado':
			self.app_datos_dni_frontal = 'aprobado'
			self.app_datos_dni_posterior = 'aprobado'
			self.app_datos_selfie = 'aprobado'
		else:
			self.app_datos_dni_frontal = 'rechazado'
			self.app_datos_dni_posterior = 'rechazado'
			self.app_datos_selfie = 'rechazado'

	@api.multi
	def button_validar_identidad_finalizar(self):
		if self.app_datos_personales == 'aprobado' and self.app_datos_dni_frontal == 'aprobado' \
			and self.app_datos_dni_posterior == 'aprobado' and self.app_datos_selfie == 'aprobado':
			self.state = 'validated'
			self.name = self.app_apellido + " " + self.app_nombre
			self.image = self.app_selfie
		elif self.state == 'validated':
			self.state = 'confirm'
		if self.app_datos_dni_selfie_validacion == 'rechazado':
			self.app_dni_frontal = None
			self.app_dni_posterior = None
			self.app_selfie = None

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

	@api.multi
	def button_validar_domicilio_finalizar(self):
		if self.app_datos_domicilio == 'aprobado':
			self.street = self.app_direccion + ' ' + self.app_numero
			self.city = self.app_localidad
			self.state_id = self.app_portal_provincia
			self.country_id = self.app_portal_provincia.country_id.id
			self.zip = self.app_cp
	
	@api.multi
	def ver_partner_validar_cbu(self):
		self.ensure_one()
		view_id = self.env.ref('financiera_validaciones.financiera_partner_validacion_cbu_form', False)
		return {
			'name': 'Validar CBU del cliente',
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'res.partner',
			'res_id': self.id,
			'views': [(view_id.id, 'form')],
			'view_id': view_id.id,
			'target': 'new',
		}

	@api.multi
	def button_validar_cbu_finalizar(self):
		if self.app_datos_cbu == 'aprobado':
			self.app_cbu_validado = self.app_cbu
			self.app_alias_validado = self.app_alias


	@api.one
	def button_confirmar_datos_selfie(self):
		super(ExtendsResPartner, self).button_confirmar_datos_selfie()
		if len(self.company_id.validaciones_config_id) > 0:
			if self.company_id.validaciones_config_id.partner_validar_identidad_activa:
				fv_values = {
					'priority': 1,
					'validation_type': 'partner_validar_identidad',
					# 'state': 'pendiente',
					'partner_id': self.id,
					'company_id': self.company_id.id,
				}
				self.env['financiera.validacion'].create(fv_values)

	@api.one
	def button_confirmar_datos_domicilio(self):
		super(ExtendsResPartner, self).button_confirmar_datos_domicilio()
		if len(self.company_id.validaciones_config_id) > 0:
			if self.company_id.validaciones_config_id.partner_validar_domicilio_activa:
				if self.app_portal_state == 'datos_validaciones' and self.app_datos_domicilio == 'manual':
					fv_values = {
						'priority': 1,
						'validation_type': 'partner_validar_domicilio',
						# 'state': 'pendiente',
						'partner_id': self.id,
						'company_id': self.company_id.id,
					}
					self.env['financiera.validacion'].create(fv_values)

	@api.one
	def button_confirmar_datos_cbu(self):
		super(ExtendsResPartner, self).button_confirmar_datos_cbu()
		if len(self.company_id.validaciones_config_id) > 0:
			if self.company_id.validaciones_config_id.partner_validar_cbu_activa:
				if self.app_portal_state == 'datos_validaciones' and self.app_datos_cbu == 'manual':
					fv_values = {
						'priority': 1,
						'validation_type': 'partner_validar_cbu',
						# 'state': 'pendiente',
						'partner_id': self.id,
						'company_id': self.company_id.id,
					}
					self.env['financiera.validacion'].create(fv_values)