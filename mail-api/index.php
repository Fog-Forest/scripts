<?php

use PHPMailer\PHPMailer\PHPMailer;

require 'PHPMailer/PHPMailer.php';
require 'PHPMailer/SMTP.php';

//获取参数
$title = $_GET['title'];
$content = $_GET['content'];

$mail = new PHPMailer();
//SMTP配置
$mail->SMTPDebug  = 0;                                      //E//Enable SMTP debugging, SMTP::DEBUG_OFF = off (for production use)
$mail->isSMTP();                                            //Send using SMTP
$mail->Host       = 'smtp.example.com';                     //Set the SMTP server to send through
$mail->SMTPAuth   = true;                                   //Enable SMTP authentication
$mail->Username   = 'user@example.com';                     //SMTP username
$mail->Password   = 'secret';                               //SMTP password
$mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;            //Enable implicit TLS encryption
$mail->Port       = 465;                                    //TCP port to connect to; use 587 if you have set `SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS`

//收件信息
$mail->setFrom('from@example.com', 'Mailer');               //设置发件人信息
$mail->addAddress('ellen@example.com');                     //设置收件人邮箱地址
//$mail->addAddress('joe@example.net', 'Joe User');         //收件人昵称可选
//$mail->addReplyTo('info@example.com', 'Information');     //设置邮件的回复地址

//附件
//$mail->addAttachment('/var/tmp/file.tar.gz');             //添加邮件附件
//$mail->addAttachment('/tmp/image.jpg', 'new.jpg');        //附件名称可选

//正文
$mail->isHTML(true);                                        //是否为HTML格式
//$mail->Subject = 'Here is the subject';                                       // 邮件标题
//$mail->Body    = 'This is the HTML message body <b>in bold!</b>';             // 邮件内容

$mail->Subject = $title;
//邮件模板
$mail->Body    = <<<EOF
<div
    style="border-radius:5px;font-size:13px;width:680px;font-family:微软雅黑,'Helvetica Neue',Arial,sans-serif;margin:10px auto 0px;border:1px solid #eee;max-width:100%;">
    <div style="width:100%;background:#49BDAD;color:#FFFFFF;border-radius:5px 5px 0 0;">
        <p style="font-size:15px;word-break:break-all;padding:20px 32px;margin:0;">⚠️服务器探针告警！</p>
    </div>
    <div style="margin:0px auto;width:90%">
        <p>🐣描述：</p>
        <p style="background:#EFEFEF;margin:15px 0px;padding:20px;border-radius:5px;font-size:14px;color:#333;">$content</p><br>
        <p>请注意：此邮件由 <a style="color:rgb(17, 181, 247);text-decoration:none" href="https://localhost" target='_blank'>探针平台</a> 自动发送，请勿直接回复。</p>
    </div>
</div>
EOF;

//发送邮件
if (!$mail->send()) {
    echo '邮件发送失败：' . $mail->ErrorInfo;
} else {
    echo '邮件已送达！';
}
