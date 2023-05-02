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
  subject: 'Bin Capacity Alert',
  html: `
    <div style="font-family: Arial, sans-serif; background-color: #F5F5F5; padding: 20px;">
      <div style="text-align: center;">
        <h1 style="font-size: 24px; color: #333333;">Bin Capacity Alert</h1>
        <img src="https://res.cloudinary.com/dhqqwdevm/image/upload/v1682526360/horizontal_vxeyqg.png" alt="Sample Image" style="max-width: 400px; margin: 20px auto;">
      </div>
      <div style="background-color: #FFFFFF; padding: 20px; border-radius: 5px;">
        <p style="font-size: 16px; color: #333333;">The trash bin for the 3 category is at maximum capacity already.</p>
        <p style="font-size: 16px; color: #333333;">Kindly take the necessary measures to address this matter promptly.</p>
        <p style="font-size: 16px; color: #333333;">Your prompt action will ensure smooth waste management operations and prevent any inconvenience.</p>
        <br>
        <p style="font-size: 16px; color: #333333;"><strong>Team Garpo</strong></p>
      </div>
    </div>
  `,
};

transporter.sendMail(mailOption, (err, info) => {
  if (err) {
    console.log(err);
  } else {
    console.log('email sent', info.response);
  }
});
