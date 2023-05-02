const express = require('express');
const port = 8080 || process.env.PORT;
const app = express();
const array = [];
const multer = require('multer');
const cloudinary = require('cloudinary').v2;
const { CloudinaryStorage } = require('multer-storage-cloudinary');
const bodyParser = require('body-parser');
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.json());
const nodemailer = require('nodemailer');
const admin = require('firebase-admin');
const serviceAccount = require('./serviceAccount.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
});
const db = admin.firestore();

console.clear();
//Cloudinary and multer config
cloudinary.config({
  cloud_name: 'dhqqwdevm',
  api_key: '472757221256643',
  api_secret: 'aPd_vvuwGdg56jlU_EjBaNSaTa4',
});

const upload = (req, res, class_name) => {
  const storage = new CloudinaryStorage({
    cloudinary: cloudinary,
    params: {
      folder: class_name, // set the folder name based on the class name
    },
  });

  const uploadMiddleware = multer({
    storage: storage,
  }).single('image'); // assume the file field name is "image"

  // call the upload middleware
  uploadMiddleware(req, res, function (err) {
    if (err) {
      // handle error
      console.log(err);
      res.status(500).json({ error: 'Failed to upload file' });
    } else {
      // file uploaded successfully
      console.log(`File uploaded to folder: ${class_name}`);
      res.status(200).json({ message: 'File uploaded successfully' });
    }
  });
};

app.get('/', (req, res) => {
  array.push('GARPO Rest API v1.0.0');
  console.log(' A QR CODE HAS BEEN SCANNED');
  res.send('GARPO Rest API v1.0.0');
});
const transporter = nodemailer.createTransport({
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

app.post('/bin-full', async (req, res) => {
  const { bin_number } = req.body;
  let binType;
  switch (bin_number) {
    case 1:
      binType = 'Plastic';
      break;
    case 2:
      binType = 'Paper';
      break;
    case 3:
      binType = 'Metal';
      break;
    default:
      binType = 'Unknown';
  }

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
          <p style="font-size: 16px; color: #333333;">The trash bin for the ${binType} category is at maximum capacity already.</p>
          <p style="font-size: 16px; color: #333333;">Kindly take the necessary measures to address this matter promptly.</p>
          <p style="font-size: 16px; color: #333333;">Your prompt action will ensure smooth waste management operations and prevent any inconvenience.</p>
          <br>
          <p style="font-size: 16px; color: #333333;"><strong>Team Garpo</strong></p>
        </div>
      </div>
    `,
  };

  transporter.sendMail(mailOption, (error, info) => {
    if (error) {
      console.error('Error sending email notification:', error);
      res.status(500).send('Error sending email notification');
    } else {
      console.log('Email notification sent successfully:', info.response);
      res.send('Email notification sent successfully');
    }
  });
});

app.post('/qr-data', async (req, res) => {
  const { data, points } = req.body;
  try {
    const userRef = db.collection('Users').doc(data);
    const userDoc = await userRef.get();
    if (!userDoc.exists) {
      console.log('NISUD SA ERROR');
      res.status(404).send('User not found');
    } else {
      const userData = userDoc.data();
      const updatedPoints = userData.Points + parseInt(points);
      const updatedTotalPoints = userData['Total Points'] + parseInt(points);
      await userRef.update({
        Points: updatedPoints,
        'Total Points': updatedTotalPoints,
      });
      console.log(updatedPoints, updatedTotalPoints);
      res.send('Points updated successfully');
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Error getting user');
  }
});

app.post('/upload', (req, res) => {
  // console.log('nisud');
  const folderPath = req.query.folder || 'DEV';
  upload(req, res, folderPath);
  // console.log(folderPath);
  // const file = req.file.path;
  // cloudinary.uploader.upload(file, (err, result) => {
  //   if (err) {
  //     res.status(500).send({ error: 'ERROR BRO' });
  //   } else {
  //     res.status(200).send({ message: 'SUCCESS BRO' });
  //   }
  // });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
