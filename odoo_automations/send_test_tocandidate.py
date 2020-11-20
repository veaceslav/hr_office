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


CLASSMARKER_QUIZZES = { "Quant Analyst" : ("https://www.classmarker.com/online-test/start/?quiz=4rj5fa92fc7a80ee" , "abc123"),
                        "Graduate Trader" : ("https://www.classmarker.com/online-test/start/?quiz=gcd5f9bfed0754e3", "abc123"),
                        "Experienced Trader" : ( "https://www.classmarker.com/online-test/start/?quiz=gqa5fa92f76e1832", "abc123")}

def get_email_body(name, job_name, classmarker_link, classmarker_pass, deadline):
  template = env['mail.template'].browse(14)
  body = str(template.body_html).format(name, job_name, classmarker_link, classmarker_pass, deadline)
  
  return body
  
def create_classmarker_link(job, name, surname, email, applicant_id ):
    if job not in CLASSMARKER_QUIZZES:
        return None, "Job: " + job + " not in the list of classmarker Quizzes"

    return CLASSMARKER_QUIZZES[job][0] + "&cm_fn=" + name\
           + "&cm_ln=" + surname.replace(" ", "%20") \
           + "&cm_e=" + email + "&cm_user_id=" + str(applicant_id), None
           
  
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
  

# only send the test if the candidate was previously in "New/Review CV"
# and was moved to "Ready for online test"
if record.stage_id[0].id == 3 and record.last_stage_id[0].id == 1:

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

  send_email(str(record.email_from), subject, email_body)
  add_email_to_thread(record.id, subject, email_body )
  
  #once we send the email, move the candidate to the "Online Test Sent"
  #next_stage = env['hr.recruitment.stage'].browse(3)
  #record.update( { "stage_id" : next_stage})
