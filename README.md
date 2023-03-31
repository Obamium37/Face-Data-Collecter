# Face-Data-Collecter
The Data collector for the model that we will train for the facial recognition model. All updates to code will be logged to this .README


<br><br/>

**3/14**

  - Added detection for frontal face and profile face

  - Used detection scripts to mask track face and Mask background(As of 3/13/23- Very buggy, needs review)

  - The masked background will help model detect the face with various backgrounds

<br><br/>
  - **Note:**

  - Further on in the day I built a new system, all buggy code comments should be ignored

  - New System: 

    - Will take picture of screen if face detected

    - TODO: Picture includes background, we need to find a way to only take a picture of the face, and not the background
    - TODO: The script only takes one picture, we need it to take multiple pictures



<br><br/>

**3/30**
  - Changed system to set background to black
  - TODO: Need to find way to multiple pictures of face instead of just taking one, as well as a way to save it
  - TODO: See if the model will be able to use data with a black background


