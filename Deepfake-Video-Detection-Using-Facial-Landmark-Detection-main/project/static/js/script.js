document.getElementById("upload-form").addEventListener("submit", async (e) => {
    e.preventDefault();

    const realImageInput = document.getElementById("real-image");
    const videoInput = document.getElementById("video-file");

    // Ensure both the image and video are uploaded
    if (!realImageInput.files[0] || !videoInput.files[0]) {
        alert("Please upload both a real image and a video.");
        return;
    }

    const formData = new FormData();
    formData.append("real_image", realImageInput.files[0]);
    formData.append("video_file", videoInput.files[0]);

    // Show loading state and hide output section
    document.getElementById("loading").style.display = "block";
    document.getElementById("output").style.display = "none";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        // Handle errors if the response is not successful
        if (!response.ok) {
            throw new Error("Failed to process the video and image.");
        }

        // Parse the server response as JSON
        const data = await response.json();

        // Render the chart with the server's data
        renderChart(data.similarities_to_real, data.similarities_to_prev);

        // Display the processed video from the server
        displayProcessedVideo(data.processed_video_url);
    } catch (error) {
        // Display the error message
        alert(error.message);
    } finally {
        // Hide the loading message once processing is done
        document.getElementById("loading").style.display = "none";
    }
});

// Function to render the chart using Chart.js
function renderChart(similaritiesToReal, similaritiesToPrev) {
    const ctx = document.getElementById("result-chart").getContext("2d");
    document.getElementById("output").style.display = "block"; // Show the output section

    new Chart(ctx, {
        type: "line",
        data: {
            labels: Array.from({ length: similaritiesToReal.length }, (_, i) => i + 1),
            datasets: [
                {
                    label: "Similarity to Real Image",
                    data: similaritiesToReal,
                    borderColor: "blue",
                    fill: false,
                },
                {
                    label: "Similarity to Previous Frame",
                    data: similaritiesToPrev,
                    borderColor: "red",
                    fill: false,
                },
            ],
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: "Frame Index" } },
                y: { title: { display: true, text: "Similarity Score" } },
            },
        },
    });
}

// Function to display the processed video from the server
function displayProcessedVideo(videoUrl) {
    const videoElement = document.getElementById("processed-video");
    videoElement.src = videoUrl; // Set the source URL for the video
}
