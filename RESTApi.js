const express = require('express');
const port = 8080 || process.env.PORT;
const app = express();
const array = [];
const bodyParser = require('body-parser');
app.use(express.urlencoded({ extended: true }));
app.use(bodyParser.json());

app.get('/', (req, res) => {
  array.push('Hello World');
  console.log(' A QR CODE HAS BEEN SCANNED');
  res.send(array);
});

app.post('/test', (req, res) => {
  console.log(req.body);
  res.send('SUCCESS');
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
