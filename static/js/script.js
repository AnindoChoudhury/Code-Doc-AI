document.addEventListener("DOMContentLoaded", () => {
  const generateBtn = document.getElementById("generateBtn");
  const codeInput = document.getElementById("codeInput");
  const resultContainer = document.getElementById("resultContainer");
  const documentationOutput = document.getElementById("documentationOutput");

  generateBtn.addEventListener("click", () => {
    const code = codeInput.value;

    if (code.trim() === "") {
      alert("Please enter some C++ code.");
      return;
    }

    documentationOutput.textContent = "Generating...";
    resultContainer.style.display = "block";

    fetch("/generate-docs", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ code: code }),
    })
      .then((response) => response.json()) // 3. Parse the JSON response from the server
      .then((data) => {
        console.log("Data received on frontend:", data);
        if (data.status === "success") {
          documentationOutput.textContent = data.documentation;
        } else {
          documentationOutput.textContent = "Error: " + data.message;
        }
        resultContainer.style.display = "block";
      })
      .catch((error) => {
        console.error("Error:", error);
        documentationOutput.textContent =
          "An error occurred while connecting to the server.";
        resultContainer.style.display = "block";
      });
  });
});
