# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.exceptions import UserError, ValidationError
import tempfile
import base64
import os
from PIL import Image
# import pytesseract
import numpy as np
import cv2
class ExtendsResPartner(models.Model):
	_name = 'res.partner'
	_inherit = 'res.partner'

	app_datos_dni_selfie_validacion = fields.Selection([
		('aprobado', 'Aprobado'),
		('rechazado', 'Rechazado')
	], "Datos de DNI y selfie")
	app_dni_frontal_text = fields.Char('Texto en DNI frontal')
	probability_datos_personales_on_dni = fields.Float('Probabilidad datos personales en DNI')

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

	def image_to_text(self, img):
		ret = None
		if img == None or img == False:
			raise ValidationError("DNI no cargado.")
		# decode the base64 encoded data
		data = base64.decodestring(img)
		# create a temporary file, and save the image
		fobj = tempfile.NamedTemporaryFile(delete=False)
		fname = fobj.name
		fobj.write(data)
		fobj.close()
		# open the image with PIL
		try:
			# image = Image.open(fname)
			image = cv2.imread(fname, 0)
			norm_img = np.zeros((image.shape[1], image.shape[0]))
			image = cv2.normalize(image, norm_img, 0, 255, cv2.NORM_MINMAX)
			image = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)[1]
			image = cv2.GaussianBlur(image, (1, 1), 0)
			# ret = pytesseract.image_to_string(image)
		finally:
			# delete the file when done
			pass
			# os.unlink(fname)
		return ret

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

	@api.multi
	def button_confirmar_datos_dni_frontal(self):
		if len(self.company_id.validaciones_config_id) > 0:
			if self.company_id.validaciones_config_id.partner_validar_identidad_activa:
				self.auto_check_datos_personales_on_dni()
				if self.probability_datos_personales_on_dni < self.company_id.validaciones_config_id.partner_datos_personales_dni_probability_pass:
					self.app_dni_frontal = None
					self.app_datos_dni_frontal_error = "Intente nuevamente. Evite reflejos en la imagen y que sea lo mas nitida posible."
					return self.wizard_datos_dni_frontal()
		return super(ExtendsResPartner, self).button_confirmar_datos_dni_frontal()
		
	@api.one
	def button_confirmar_datos_dni_selfie_upload(self):
		super(ExtendsResPartner, self).button_confirmar_datos_dni_selfie_upload()
		if len(self.company_id.validaciones_config_id) > 0:
			if self.company_id.validaciones_config_id.partner_validar_identidad_activa:
				fv_values = {
					'priority': 1,
					'validation_type': 'partner_validar_identidad',
					'state': 'pendiente',
					'partner_id': self.id,
					'company_id': self.company_id.id,
				}
				self.env['financiera.validacion'].create(fv_values)
				# self.app_dni_frontal_text = self.image_to_text(self.app_dni_frontal)
				# validacion_id.auto_check()

	@api.one
	def button_confirmar_datos_domicilio(self):
		super(ExtendsResPartner, self).button_confirmar_datos_domicilio()
		if len(self.company_id.validaciones_config_id) > 0:
			if self.company_id.validaciones_config_id.partner_validar_domicilio_activa:
				if self.app_portal_state == 'datos_validaciones' and self.app_datos_domicilio == 'manual':
					fv_values = {
						'priority': 1,
						'validation_type': 'partner_validar_domicilio',
						'state': 'pendiente',
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
						'state': 'pendiente',
						'partner_id': self.id,
						'company_id': self.company_id.id,
					}
					self.env['financiera.validacion'].create(fv_values)

	def normalize(self, s):
		replacements = (
				("á", "a"),
				("é", "e"),
				("í", "i"),
				("ó", "o"),
				("ú", "u"),
		)
		for a, b in replacements:
				s = s.replace(a, b).replace(a.upper(), b.upper())
		return s.upper()

	@api.multi
	def button_auto_check_datos_personales_on_dni(self):
		self.auto_check_datos_personales_on_dni()
		return {'type': 'ir.actions.do_nothing'}

	@api.one
	def auto_check_datos_personales_on_dni(self):
		self.app_dni_frontal_text = self.image_to_text(self.app_dni_frontal)
		values_check = self.normalize(self.app_nombre).split(' ')
		values_check.extend(self.normalize(self.app_apellido).split(' '))
		values_check.append(self.app_documento.replace('.', ''))
		for string in values_check:
			i = 0
			while i <= (len(string)-3):
				values_check.append(string[i:i+2])
				i = i + 1
		dni_text = self.app_dni_frontal_text.replace('.', '')
		occurrence = 0.0
		for string in values_check:
			if string in dni_text:
				occurrence += 1.0
		self.probability_datos_personales_on_dni = occurrence/(1.0*len(values_check))
