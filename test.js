const express = require('express');
const app = express();
const port = 3000;
// Import the Firestore library
const admin = require('firebase-admin');
const serviceAccount = require("./serviceAccount.json");
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const db = admin.firestore();

// Define a route for querying a Firestore collection
app.get('/test', async (req, res) => {
	console.log("TEST ROUTE")
  try {
    const snapshot = await db.collection("Users").get();
    const data = snapshot.docs.map(doc => doc.data());
    res.send(data);
  } catch (error) {
    console.error(error);
    res.status(500).send('Error querying collection');
  }
});
app.get('/qr-data', async (req, res) => {
  try {
    const userRef = db.collection('Users').doc("IurTDxjqyYdSfhpvu5T0FRpiTiV2");
    const userDoc = await userRef.get();
    if (!userDoc.exists) {
      res.status(404).send('User not found');
    } else {
      const userData = userDoc.data();
      res.send(userData);
    }
  } catch (error) {
    console.error(error);
    res.status(500).send('Error getting user');
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
