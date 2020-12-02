# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
# To return an action, assign: action = {...}

# Available variables:
#  - env: Odoo Environment on which the action is triggered
#  - model: Odoo Model of the record on which the action is triggered; is a void recordset
#  - record: record on which the action is triggered; may be void
#  - records: recordset of all records on which the action is triggered in multi-mode; may be void
#  - time, datetime, dateutil, timezone: useful Python libraries
#  - log: log(message, level='info'): logging function to record debug information in ir.logging table
#  - UserError: Warning Exception to use with raise
# To return an action, assign: action = {...}
#log(str(record.partner_name) + str(record.email_from) + " id: " + str(record.id)+ " job_id: " + str(record.job_id[0].id) +" stage: " + str(record.stage_id[0].id) + " prev stage: " + str(record.last_stage_id[0].id))


CLASSMARKER_QUIZZES = { "Quant Analyst" : ("https://www.classmarker.com/online-test/start/?quiz=4f35fbf8c0a2f432" , "abc123")}
                        
ONLINE_TEST_STAGE = 3
PROGRAMMING_CHALLENGE_STAGE = 8

def get_email_body( name, job_name, classmarker_link, classmarker_pass, deadline):
  template = env['mail.template'].browse(33)
  body = str(template.body_html).format(name, job_name, classmarker_link, classmarker_pass, deadline)
  
  return body
  
def create_classmarker_link(job, name, surname, email, applicant_id ):

    if job not in CLASSMARKER_QUIZZES:
      raise UserError("Job " + job + " does not have classmarker programming challenges")
      
    return CLASSMARKER_QUIZZES[job][0] + "&cm_fn=" + name\
           + "&cm_ln=" + surname.replace(" ", "%20") \
           + "&cm_e=" + email + "&cm_user_id=" + str(applicant_id), None
           
  
def send_email(recipient, subject, body, message_id):
  template_data = {'email_from' :'recruitment@davinciderivatives.odoo.com',
                   'mail_message_id' : message_id.id,
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
  rez= env['mail.message'].create(template_data2)
  
  return rez
  

def send_programming_challenge():
  
  if not record.email_from:
    raise UserError("The candidate has no email address")
    
    
  subject = "Application " + record.job_id[0].display_name + " - Da Vinci Derivatives"
    
  classmarker_link, error = create_classmarker_link(record.job_id[0].display_name,
                                        record.partner_name.split(" ")[0],
                                        " ".join(record.partner_name.split(" ")[1:]),
                                        record.email_from,
                                        record.id)

  email_body = get_email_body(record.partner_name,
                              record.job_id[0].display_name,
                              classmarker_link,
                              CLASSMARKER_QUIZZES[record.job_id[0].display_name][1],
                              (datetime.date.today() + datetime.timedelta(days=7)).strftime(" %d %b %Y"))

  message_id = add_email_to_thread(record.id, subject, email_body )
  send_email(str(record.email_from), subject, email_body, message_id)


def main():
  
  if not record or not record.stage_id or not record.last_stage_id:
    return
    
  if record.stage_id[0].id == PROGRAMMING_CHALLENGE_STAGE and record.last_stage_id[0].id == ONLINE_TEST_STAGE:
    send_programming_challenge()
    
    
    
main()
