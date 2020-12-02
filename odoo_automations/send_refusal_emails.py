# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
# To return an action, assign: action = {...}

def get_email_body(name, job_name):
  template = env['mail.template'].browse(15)
  body = str(template.body_html).format(name, job_name)
  
  return body
           
  
def send_email(message_id, recipient, subject, body):
  template_data = {'email_from' :'recruitment@davinciderivatives.odoo.com',
                   'subject': subject,
                   'email_to': str(record.email_from),
                   'mail_message_id' : message_id.id,
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
  return env['mail.message'].create(template_data2)
  

yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
data = env['hr.applicant'].search([( 'active', '=' , False), ('write_date', 'like', yesterday + '%')])


for record in data:
  #log(env['hr.applicant'].browse(item.id).partner_name + env['hr.applicant'].browse(item.id).refuse_reason_id.name)
  subject = "Your Job Application: "+ record.job_id[0].display_name
  body = get_email_body(record.partner_name, record.job_id[0].display_name)
  message_id = add_email_to_thread(record.id, subject, body)
  send_email(message_id, record.email_from, subject, body)
