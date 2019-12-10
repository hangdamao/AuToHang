# created 27.06.2019
# author = "hang"

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from base import log_base

logger = log_base.MyLog("mail_base")


class SendMail(object):

    def __init__(self,
                 smtp_server,
                 smtp_port,
                 smtp_sender,
                 smtp_senderpassword,
                 smtp_receiver,
                 smtp_subject,
                 smtp_body,
                 smtp_file=None):
        """
        to init parameter
        :param smtp_server: 邮件服务器
        :param smtp_port:端口号
        :param smtp_sender:发件人
        :param smtp_senderpassword:密码
        :param smtp_receiver:收件人
        :param smtp_subject:邮件主题
        :param smtp_body:邮件内容
        :param smtp_file_path:文件路径
        """
        self.__smtp_server = smtp_server
        self.__smtp_port = smtp_port
        self.__smtp_sender = smtp_sender
        self.__smtp_senderpassword = smtp_senderpassword
        self.__smtp_receiver = smtp_receiver
        self.__smtp_subject = smtp_subject
        self.__smtp_body = smtp_body
        self.__smtp_file = smtp_file
        self.__smtp = smtplib.SMTP()

    def __enter__(self):
        return self

    def mail_content(self):
        """
        to edit mail content
        :param subject: 邮件主题
        :param body:邮件内容
        :return:msg
        """
        if self.__smtp_file != None :
            msg = MIMEMultipart()
            with open(self.__smtp_file, 'rb') as fp:
                mail_body = fp.read()
            att = MIMEText(mail_body, "base64", "utf-8")
            att['Conten-Type'] = "application/octet-stream"
            att["Content-Disposition"] = 'attachment; filename="%s"' % self.__smtp_file
            msg.attach(att)
            msg.attach(MIMEText(self.__smtp_body, "html", "utf-8"))
            msg['from'] = self.__smtp_sender
            msg['to'] = ";".join(self.__smtp_receiver)
            msg['subject'] = self.__smtp_subject
            return msg
        else:
            msg = MIMEText(self.__smtp_body, "html", "utf-8")
            msg['from'] = self.__smtp_sender
            msg['to'] = ";".join(self.__smtp_receiver)
            msg['subject'] = self.__smtp_subject
            return msg

    def send_mail(self):
        """
        send mail
        :return:
        """
        try:
            logger.info("邮件发送中...")
            self.__smtp.connect(self.__smtp_server)
            self.__smtp.login(user=self.__smtp_sender, password=self.__smtp_senderpassword)
        except:
            self.__smtp = smtplib.SMTP_SSL()
            self.__smtp.login(user=self.__smtp_sender, password=self.__smtp_senderpassword)

    def __exit__(self, exc_type, exc_val, exc_tb):
        aaa = self.mail_content()
        if exc_type != None:
            logger.error("邮件发送失败！")
            self.__smtp.quit()
        self.__smtp.sendmail(self.__smtp_sender, self.__smtp_receiver, aaa.as_string())
        logger.info("邮件发送成功----")
        return True


if __name__ =='__main__':
    # 公司邮箱测试
    with SendMail(smtp_server="mail.zcsmart.com",
                 smtp_port=993,
                 smtp_sender="cq154@zcsmart.com",
                 smtp_senderpassword="ai102839.",
                 smtp_receiver="306936010@qq.com",# ,"czk176@zcsmart.com"
                 smtp_subject="hang的邮件！！",
                 smtp_body="<p>我的简书地址：https://www.jianshu.com/u/1f9e71a85238</p>") as s_m:
        s_m.send_mail()

