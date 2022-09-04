import os

from django.template.loader import render_to_string
from django.utils.html import strip_tags
import plotly, base64, ssl, smtplib
from email.mime.base import MIMEBase
from email.utils import make_msgid
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import encoders
from functools import reduce
import pandas as pd
import plotly.graph_objects as go
from plotly.graph_objs import Layout

class Transaction:
    def __init__(self, date, amount) -> None:
        self.date = date
        self.amount = amount

def report(data, df, receiver_email):
    sender_email = os.environ.get('EMAIL_HOST_USER')
    password = os.environ.get('EMAIL_HOST_PASSWORD')

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email
    image_cid = make_msgid()
    # Create the plain-text and HTML version of your message
    #html = f'<html>    <body><img src="cid:{image_cid[1:-1]}">        <a href="http://www.realpython.com">Real Python</a>     </body>    </html>'
    income = list(filter(lambda x:x.amount > 0, data))
    expenses = list(filter(lambda x:x.amount < 0, data))

    
    # Turn these into plain/html MIMEText objects
    filename = "img.jpg"
    df['date'] = pd.to_datetime(df['date'])
    #scatter = plotly.graph_objs.Scatter(x=[1, 2, 3], y=[2, 1, 3])
    #layout = plotly.graph_objs.Layout()
    #fig = plotly.graph_objs.Figure([scatter], layout)
    #print(df.groupby(pd.Grouper(key='date', freq='D')).sum())
    per = df.date.dt.to_period("M")
    df = df.groupby(df.date.dt.date)['amount'].sum().reset_index(name="amount")
    g = df.groupby(per)['amount'].sum().reset_index(name="amount")
    df['cum'] = df['amount'].cumsum()
    layout = Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
    )
    fig = go.Figure(layout=layout)
    fig.add_trace(go.Scatter(x=df['date'], y=df['cum'], name="spline",
                    hoverinfo='text+name',
                    line_shape='spline'))
    #fig.write_image("img.jpg")
    png = plotly.io.to_image(fig)
    part3 = MIMEBase("application", "octet-stream")
    part3.set_payload(png)
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part3)

    # Add header as key/value pair to attachment part
    part3.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    
    part3.add_header('Content-ID', image_cid)
    part3.add_header('X-Attachment-Id', image_cid[1:-1])
    part3.add_header('Content-Type', 'image/jpeg; name="img.jpg"')

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    print(g)
    print([f"{x['date']}, {x['amount']}" for key, x in g.iterrows()])
    html = render_to_string('report/mail/report.html', 
    {
        'data': data,
        'image':image_cid[1:-1],
        'income':reduce(lambda x,y:x+y, [x.amount for x in income]),
        'expense':reduce(lambda x,y:x+y, [x.amount for x in expenses]),
        'balance':reduce(lambda x,y:x+y, [x.amount for x in data]),
        'df':[Transaction(x['date'], x['amount']) for key, x in g.iterrows()]
     })
    text = strip_tags(html)
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)
    message.attach(part3)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(os.environ.get('EMAIL_HOST'), os.environ.get('EMAIL_PORT'), context=context) as server:
        server.login(sender_email, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
    

