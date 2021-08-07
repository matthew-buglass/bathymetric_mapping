# 3 Dimensional Bathymetric Mapping Software
Bathymetry is the mapping of under water structures, and is very important for monitoring bodies of water. Generally, bathymetric maps are represented on a single plane as a series of circles marking areas of equivalent depth. 	[National Geographic](https://www.nationalgeographic.org/encyclopedia/bathymetry/)

However, using 3D modeling software and 3D printing, we can create a more emersive representation. Using optical character recognition, GPS, and the depth readout from a sonic fish finder, we can create a series of 3-dimesional coordinates representing a disperse point map of underwater structures. Using graph algorythms, that point map can be fed into a free modeling software called [Blender](https://www.blender.org/) using its scripting functionalities to join the point map into faces and 3D geometry.

That 3D model can be scaled, edited, and printned in a 3D printer to create ultra-accurate physical models of underwater structures.

[![Blender Script generating a hyperbolic parabaloid mesh from a disperse point map](https://img.youtube.com/vi/AwUt0oBUfQk/0.jpg)](https://youtu.be/AwUt0oBUfQk)

# Current Stable Functionalities and Completed Milestones
- Re-wiring of fish finder power supply to quick clip into weather proof connectors for both 120V wall outlet or a Marine boat battery
- Storage and serialization of data points
- Transformation of data points into a wireframe mesh in Blender
- Completed code to estimate the square area of a body of water from a Google Maps image

# In Progress Functionalties and Milestones
- Fine tuning Optical Character Recognition pipeline to acurately pull depth readings off of a fish finder screen
- Designing camera mount and plate to keep a webcam consistently placced in from of the fish finder screen while in the field

# Future Functionalities and Milestones
- 3D print the camera mount that will be held between the fish finder base and the boat seat the it is mounted to
- Purchase a RaspberryPi 4 and and Adafruit GPS module to run data collection in the field 
