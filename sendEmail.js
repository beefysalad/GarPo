const nodemailer = require('nodemailer');

let transporter = nodemailer.createTransport({
  port: 587,
  secure: true,
  service: 'gmail',
  auth: {
    user: '321garpo@gmail.com',
    pass: 'fjmzjtdysrdzvsqa',
  },
  tls: {
    rejectUnauthorized: false,
  },
});

const mailOption = {
  from: '321garpo@gmail.com',
  to: 'jpatrickzephyr@gmail.com',
  subject: 'test nodemailer',
  html: `
    <h1>Welcome to the Raspberry Pi Email</h1>
    <p>This is a test email sent from my Raspberry Pi!</p>
    <img src="https://res.cloudinary.com/dhqqwdevm/image/upload/v1682526360/horizontal_vxeyqg.png" alt="Sample Image">
  `,
};

transporter.sendMail(mailOption, (err, info) => {
  if (err) {
    console.log(err);
  } else {
    console.log('email sent', info.response);
  }
});
