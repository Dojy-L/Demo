# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AppointmentBooking(models.Model):
    _name = 'appointment.booking'
    _description = 'Appointment Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Adds chatter

    name = fields.Char(string="Appointment Reference", required=True, copy=False, readonly=True, index=True,
                       default='New')
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    service_id = fields.Many2one('product.product', string="Service", domain=[('detailed_type', '=', 'service')], required=True)
    appointment_date = fields.Date(string="Appointment Date", required=True)
    start_time = fields.Float(string="Start Time", required=True)
    end_time = fields.Float(string="End Time", required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], default='draft', string="Status", tracking=True)

    check_in_time = fields.Datetime(string="Check-in Time", readonly=True)
    check_out_time = fields.Datetime(string="Check-out Time", readonly=True)

    # @api.constrains('start_time', 'end_time')
    # def _check_time_validity(self):
    #     """Ensure start_time is before end_time and no overlapping appointments"""
    #     for record in self:
    #         if record.start_time >= record.end_time:
    #             raise ValidationError("Start time must be before end time.")

            # overlapping_appointments = self.search([
            #     ('id', '!=', record.id),  # Exclude the current record
            #     ('appointment_date', '=', record.appointment_date),
            #     ('start_time', '<', record.end_time),
            #     ('end_time', '>', record.start_time),
            #     # ('service_id', '=', record.service_id.id)
            # ])
            # if overlapping_appointments:
            #     raise ValidationError("This time slot is already booked. Please choose another slot.")

    def action_confirm(self):
        """Confirm the appointment"""
        self.write({'state': 'confirmed'})

    def action_check_in(self):
        """Mark the appointment as checked in"""
        self.write({'state': 'checked_in', 'check_in_time': fields.Datetime.now()})

    def action_check_out(self):
        """Mark the appointment as checked out"""
        self.write({'state': 'checked_out', 'check_out_time': fields.Datetime.now()})

    def action_cancel(self):
        self.state = 'cancelled'
