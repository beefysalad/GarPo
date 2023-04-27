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
