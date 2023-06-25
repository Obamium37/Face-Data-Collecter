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

        // Create a Blob with the recorded chunks
        const videoBlob = new Blob(recordedChunks, { type: 'video/webm' });

      
        // Generate a download link for the video and automatically trigger the download
        videoURL = URL.createObjectURL(videoBlob);
        const a = document.createElement('a');
        a.href = videoURL;
        a.download = 'recorded_video.webm';
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);

        // Create a video element to display the recorded video
        const recordedVideo = document.createElement('video');
        recordedVideo.src = videoURL;
        recordedVideo.controls = true;
        recordedVideoContainer.appendChild(recordedVideo);

        // Calculate the video duration
        const videoDurationInSeconds = recordedVideo.duration;
        videoDuration = Math.floor(videoDurationInSeconds);

        // Check if the video duration is less than 30 seconds
        if (videoDuration < 30) {
          nextButton.disabled = true;
        }
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
