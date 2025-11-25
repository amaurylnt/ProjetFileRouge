async function fetchCameras() {
  const errorElement = document.getElementById("error");
  const tbody = document.getElementById("camera-table-body");

  errorElement.textContent = "";
  tbody.innerHTML = "";

  try {
    const response = await fetch("/api/cameras");
    if (!response.ok) {
      throw new Error("Erreur HTTP " + response.status);
    }

    const cameras = await response.json();

    cameras.forEach((cam) => {
      const tr = document.createElement("tr");

      const tdId = document.createElement("td");
      tdId.textContent = cam.id;
      tr.appendChild(tdId);

      const tdName = document.createElement("td");
      tdName.textContent = cam.name;
      tr.appendChild(tdName);

      const tdIp = document.createElement("td");
      tdIp.textContent = cam.ip_address;
      tr.appendChild(tdIp);

      const tdLocation = document.createElement("td");
      tdLocation.textContent = cam.location || "";
      tr.appendChild(tdLocation);

      const tdStatus = document.createElement("td");
      tdStatus.textContent = cam.status;
      tdStatus.className =
        cam.status === "UP" ? "status-up" : "status-down";
      tr.appendChild(tdStatus);

      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
    errorElement.textContent =
      "Impossible de récupérer la liste des caméras. Vérifiez que l'API est démarrée.";
  }
}

fetchCameras();
setInterval(fetchCameras, 30000);
