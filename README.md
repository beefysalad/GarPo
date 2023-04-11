<img src="https://res.cloudinary.com/dhqqwdevm/image/upload/v1678399925/334924936_2574475806033853_7045665737658280683_n_thoo6y.png" width="100%" height="auto" alt="tensorflow-image-detection icon"/>

---

# CpE462 Practice and Design 2

THESIS FINALE GOIS :mortar_board:

---

# **TEAM MEMBERS**

- [Joeje Aika G. Blanes](https://github.com/aikablanes)
- [Armand C. Catubig Jr.](https://github.com/Armand-Catubig)
- [John Patrick Ryan D. Mandal](https://github.com/beefysalad)
- [Edrian James L. Olmedo](https://github.com/CurlyLips)
- [Rose Fe I. Rotersos](https://github.com/rosef48)
- [Ahl Pritz Solon](https://github.com/ahlpritz)
- [Paolo J. Taboso](https://github.com/tabsgage)
- [Keanue Dax Teaño](https://github.com/Daxu010)

### Todos / RoadMap

- [x] Port the model to TensorflowLite
- [ ] Setup DJango/Express.js Backend for REST API on the Raspi
- [ ] Communication between REST API and Flutter Mobile Application

## Installation

Make sure you have [Python 3](https://www.python.org/downloads/) installed, then install [Tensorflow](https://www.tensorflow.org/install/) on your system, and clone this repo.

<br/>

## Usage

### Prepare the image data sets

In order to start the transfer learning process, a folder named `training_dataset` needs to be created in the root of the project folder. This folder will contain the image data sets for all the subjects, for whom the classification is to be performed.

[Download the Datasets here](https://bit.ly/3mcb3aS)

Create the `training_dataset` folder and add the images for all the data sets in the following manner -

```javascript
/
|
|
---- /training_dataset
|    |
|    |
|    ---- /plastics
|    |    plastic1.jpg
|    |    plastic2.jpg
|    |    ...
|    |
|    |
|    ---- /paper
|         paper1.jpg
|         paper2.jpg
|         ...
|
|
```

This enables classification of images between the `plastics` and `paper` data sets. Image Augmentation techniques have also been applied here to increase the dataset

> Make sure to include multiple variants of the subject (side profiles, zoomed in images etc.), the more the images, the better is the result. sa kani diri kay wala pa nako apili og glass

### Initiate transfer learning

Go to the project directory and run -

```javascript
$ bash train.sh
```

This script installs the `Inception` model and initiates the re-training process for the specified image data sets.

Once the process is complete, it will return a training accuracy somewhere between `85% - 100%`.

The `training summaries`, `retrained graphs` and `retrained labels` will be saved in a folder named `tf_files`.

### Classify objects

```javascript
python classify.py
```

### Live Inferencing with Camera

```javascript
python inference.py
```

---

To run the RESTApi server, make sure you have nodejs installed

### Rest API Server

```javascript
node RestAPI.js
```

Big shoutouts to the team behind TrashNet
[TrashNet Dataset](https://github.com/garythung/trashnet)

<br/>

## License

MIT License

Copyright (c) 2017

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
