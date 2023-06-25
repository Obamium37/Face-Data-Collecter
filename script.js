const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const redoButton = document.getElementById('redoButton');
const preview = document.getElementById('preview');
const recordedVideoContainer = document.getElementById('recordedVideoContainer');
const nextButton = document.getElementById('nextButton');

let mediaStream;
let mediaRecorder;
let recordedChunks = [];
let videoURL;
let videoDuration = 0;
let timerId;

// Check if the browser supports MediaDevices API
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  startButton.disabled = false;

  // Start button click event
  startButton.addEventListener('click', async () => {
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });

      // Enable stop and redo buttons, disable start button
      startButton.disabled = true;
      stopButton.disabled = false;
      redoButton.disabled = false;

      // Display camera stream in video element
      preview.srcObject = mediaStream;
      preview.play();

      // Create a new MediaRecorder
      recordedChunks = [];
      mediaRecorder = new MediaRecorder(mediaStream);

      // Collect video data in chunks
      mediaRecorder.addEventListener('dataavailable', (event) => {
        if (event.data.size > 0) {
          recordedChunks.push(event.data);
        }
      });

      // Stop button click event
      stopButton.addEventListener('click', () => {
        // Stop recording
        stopRecording();
      });

      // MediaRecorder stop event
      mediaRecorder.addEventListener('stop', () => {
        // Enable next and redo buttons, disable stop button
        nextButton.disabled = false;
        stopButton.disabled = true;
        redoButton.disabled = false;

        // Stop the camera stream
        mediaStream.getVideoTracks()[0].stop();

        const videoBlob = new Blob(recordedChunks, { type: 'video/webm' });

        // Upload video to AWS S3 bucket
        uploadToS3(videoBlob);




        // Create a video element to display the recorded video
        const recordedVideo = document.createElement('video');
        recordedVideo.src = videoURL;
        recordedVideo.controls = true;
        recordedVideoContainer.appendChild(recordedVideo);

        // Calculate the video duration
        recordedVideo.addEventListener('loadedmetadata', () => {
          const videoDurationInSeconds = recordedVideo.duration;
          videoDuration = Math.floor(videoDurationInSeconds);

          // Check if the video duration is less than 30 seconds
          if (videoDuration < 30) {
            nextButton.disabled = true;
          }
        });
      });

      // Start recording
      mediaRecorder.start();

      // Set a timer to stop recording after 30 seconds
      timerId = setTimeout(() => {
        stopRecording();
      }, 30000);
    } catch (error) {
      console.error('Failed to access the camera:', error);
    }
  });

  // Redo button click event
  redoButton.addEventListener('click', () => {
    // Enable start button, disable stop and redo buttons
    startButton.disabled = false;
    stopButton.disabled = true;
    redoButton.disabled = true;
    nextButton.disabled = true;

    // Clear the recorded video container
    recordedVideoContainer.innerHTML = '';

    // Reset the video duration
    videoDuration = 0;

    // Clear the timer if it is active
    if (timerId) {
      clearTimeout(timerId);
    }
  });
}

// Function to stop the recording
function stopRecording() {
  // Clear the timer if it is active
  if (timerId) {
    clearTimeout(timerId);
  }

  // Stop recording
  mediaRecorder.stop();
}

// Function to upload video to AWS S3 bucket
function uploadToS3(videoBlob) {
  // Replace 'your-bucket-name', 'your-access-key-id', and 'your-secret-access-key' with your actual AWS S3 bucket name, access key ID, and secret access key, respectively
  const bucketName = 'polygenceproject';
  const accessKeyId = '';
  const secretAccessKey = '';

  const s3 = new AWS.S3({
    accessKeyId: accessKeyId,
    secretAccessKey: secretAccessKey
  });

  const params = {
    Bucket: bucketName,
    Key: 'recorded_video.webm',
    Body: videoBlob
  };

  s3.upload(params, (err, data) => {
    if (err) {
      console.error('Failed to upload video to S3:', err);
    } else {
      console.log('Video uploaded to S3 successfully:', data.Location);
      videoURL = data.Location; // Set the videoURL variable with the S3 URL
    }
  });
}
