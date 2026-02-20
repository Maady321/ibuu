document.addEventListener("DOMContentLoaded", async () => {
  window.checkAuth();
  const urlParams = new URLSearchParams(window.location.search);
  const serviceId = urlParams.get("service_id") || 1;

  document.getElementById("service_id").value = serviceId;
  try {
    const response = await makeRequest(`/api/services/${serviceId}`);
    if (response.ok) {
      const service = await response.json();
      const finalPrice = Math.floor(service.price / 100) * 100 + 99;
      document.getElementById("display-service-name").textContent =
        service.name;
      document.getElementById("display-service-price").textContent =
        `Starting at ₹${finalPrice}`;
      const icon = window.getServiceIcon(service.name);
      document.querySelector(
        "#selected-service-display .service-icon",
      ).innerHTML = `<i class="fa-solid ${icon}"></i>`;
    }
  } catch (e) {
    console.log("Could not fetch service details");
  }
  // Set minimum date to today
  const dateInput = document.getElementById("date");
  const today = new Date().toISOString().split("T")[0];
  if (dateInput) {
    dateInput.setAttribute("min", today);
  }

  document
    .getElementById("booking-form")
    .addEventListener("submit", async (e) => {
      e.preventDefault();

      const bookingDate = document.getElementById("date").value;

      // Validation check
      if (bookingDate < today) {
        window.HB.showError("date", "Please select a date from today onwards.");
        return;
      }

      const formData = {
        service_id: parseInt(document.getElementById("service_id").value),
        address: document.getElementById("address").value,
        city: document.getElementById("city").value,
        pincode: document.getElementById("zipcode").value,
        date: bookingDate,
        time: document.getElementById("time").value,
        instructions: document.getElementById("notes").value,
      };
      try {
        const response = await makeRequest(`/api/bookings`, {
          method: "POST",
          body: JSON.stringify(formData),
        });
        if (response.ok) {
          const result = await response.json();
          window.HB.showToast("Booking created successfully!");
          setTimeout(() => {
            window.location.href = "my-bookings.html";
          }, 1500);
        } else {
          const errorData = await response.json();
          window.HB.showToast(errorData.detail || "Booking failed", "error");
        }
      } catch (error) {
        console.error("Error booking:", error);
        window.HB.showToast("An error occurred. Please try again.", "error");
      }
    });
});
