# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
# To return an action, assign: action = {...}
log(str(record.partner_name) + str(record.email_from) + " id: " + str(record.id)+ " job_id: " + str(record.job_id[0].id) +" stage: " + str(record.stage_id[0].id))



def send_email(recipient, subject, body):
  template_data = {'email_from' :'recruitment@davinciderivatives.odoo.com',
                   'subject': subject,
                   'email_to': str(record.email_from),
                   'body_html': body
                   }
  
  mail_out = env['mail.mail'].create(template_data)
  mail_out.send()
  
  
def add_email_to_thread(applicant_id, subject, body):
  template_data2 = {
                      'add_sign': True,
                      'body': body,
                      'message_type': 'email',
                      'model': 'hr.applicant',
                      'no_auto_thread': False,
                      'res_id': applicant_id,
                      'subject': subject,
                      'subtype_id': 1
                      }
  env['mail.message'].create(template_data2)
  

subject = "Classmarker Online test"
email_body = "Please take the test below"

send_email(str(record.email_from), subject, email_body)
add_email_to_thread(record.id, subject, email_body )
