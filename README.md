evolisa
=======

This is an attempt at generating an output image from a source picture by mutating 
a group of semi-transparent polygons.

I wanted to do something similar to this:
http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/

![animated gif of generated image](/img/generated.gif?raw=true "timelapse gif")
![generated image](/img/0000000650.png?raw=true "generated image")

The code is still very thrown together but it produces some acceptable results. 
Generating the image above took a couple of hours though so there's room for 
improvements.

I'd be happy to hear about ideas on how to improve the algorithm/code.

Install requirements
====================

* Create virtualenv

  ```sh
  virtualenv .
  ```

* Install requirements

  ```sh
  bin/pip install -r requirements
  ```

* (optional) PIL might have to be installed like this

  ```sh
  bin/pip install PIL --allow-external PIL --allow-unverified PIL --upgrade
  ```

Usage
=====

* Running the script

  ```sh
  bin/python src/generate.py <path_to_img>
  ```

Use a small source image (e.g. with a maximum size of 512x512 pixels). The 
generated image files will be created in your system's temp directory.


Notes
=====
  
* https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil