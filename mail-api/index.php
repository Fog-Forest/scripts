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
$mail->Host       = 'smtp.exmail.qq.com';                   //Set the SMTP server to send through
$mail->SMTPAuth   = true;                                   //Enable SMTP authentication
$mail->Username   = 'send@amogu.cn';                        //SMTP username
$mail->Password   = 'Ye8980@Mail';                          //SMTP password
$mail->SMTPSecure = PHPMailer::ENCRYPTION_SMTPS;            //Enable implicit TLS encryption
$mail->Port       = 465;                                    //TCP port to connect to; use 587 if you have set `SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS`

//收件信息
$mail->setFrom('send@amogu.cn', '探针告警');                   //设置发件人信息
$mail->addAddress('ye8980@qq.com');                         //设置收件人邮箱地址
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
$mail->Body    = 'This is the HTML message body <b>in bold!</b>'; 

//发送邮件
if (!$mail->send()) {
    echo '邮件发送失败：' . $mail->ErrorInfo;
} else {
    echo '邮件已送达！';
}
