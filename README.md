evolisa - generating images with polygons
=========================================

This is an attempt at generating an output image using semi transparent polygons 
similar to http://rogeralsing.com/2008/12/07/genetic-programming-evolution-of-mona-lisa/.

![animated gif of generated image](/img/generated.gif?raw=true "timelapse gif")
![generated image](/img/0000000650.png?raw=true "generated image")

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

Notes
=====
  
* https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil