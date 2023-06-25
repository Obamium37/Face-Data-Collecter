const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');
const preview = document.getElementById('preview');
const recordedVideoContainer = document.getElementById('recordedVideoContainer');
const nextButton = document.getElementById('nextButton');

let mediaStream;
let mediaRecorder;
let recordedChunks = [];

// Check if the browser supports MediaDevices API
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  startButton.disabled = false;

  // Start button click event
  startButton.addEventListener('click', async () => {
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({ video: true });

      // Enable stop button, disable start button
      startButton.disabled = true;
      stopButton.disabled = false;

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
        mediaRecorder.stop();
      });

      // MediaRecorder stop event
      mediaRecorder.addEventListener('stop', () => {
        // Enable next button, disable stop button
        nextButton.disabled = false;
        stopButton.disabled = true;

        // Stop the camera stream
        mediaStream.getVideoTracks()[0].stop();

        // Create a Blob with the recorded chunks
        const videoBlob = new Blob(recordedChunks, { type: 'video/webm' });

        // Generate a download link for the video and automatically trigger the download
        const videoURL = URL.createObjectURL(videoBlob);
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
      });

      // Start recording
      mediaRecorder.start();
    } catch (error) {
      console.error('Error accessing camera:', error);
    }
  });
}

// Next button click event
nextButton.addEventListener('click', () => {
  window.location.href = 'done.html';
});
